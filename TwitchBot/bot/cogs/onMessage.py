from twitchio.ext import commands, sounds
import websockets
import json
from ..bot import Bot
import re
from gtts import gTTS
import playsound
import os
import time
import asyncio


message_alert_sound_minimum = 20
message_timer_start = time.time()
tts_timer = 0
tts_timer_bool = False
time_tts_used = 0
tts_bool = True
tts_max_chars = 200
obs_ws_server = "ws://localhost:8181/"


def check_for_repeats(message):
    for word in message.split(" "):
        res = None
        for i in range(1, len(word) // 2 + 1):
            if (
                not len(word) % len(word[0:i])
                and word[0:i] * (len(word) // len(word[0:i])) == word
            ):
                res = word[0:i]
        return res


def message_alert():
    path = os.path.join(os.getcwd(), "bot/cogs/message_alert.mp3")
    playsound.playsound(path)


class OnMessage(commands.Cog):
    def __init__(self, bot):
        global message_queue
        self.bot = bot
        self.is_speaking = False
        self.message_queue = []
        self.player = sounds.AudioPlayer(callback=self.player_done)
        self.user_speaking = ""

    async def player_done(self):
        self.is_speaking = False
        self.user_speaking = ""

    @commands.Cog.event()
    async def event_ready(self):
        asyncio.get_event_loop().create_task(self.tts_task())
        asyncio.get_event_loop().create_task(self.obs_tts_loop())

    @commands.Cog.event()
    async def event_message(self, message):
        global message_alert_sound_minimum, message_timer_start

        # Plays an alert upon message if there have been no messages in the sound min
        if time.time() - message_timer_start > message_alert_sound_minimum:
            message_alert()
            message_timer_start = time.time()
        else:
            message_timer_start = time.time()
        try:
            if (
                message.author.name
                and message.content[0] != "-"
                and message.content[0] != "!"
            ):
                if self.bot.tts:
                    self.message_queue.append((message.author.name, self.cleanse_message(message.content)))
        # Can error on bot connection....
        except AttributeError:
            pass

    def tts_speak(self, to_say):
        if tts_bool and int(tts_max_chars) > 0 and not self.is_speaking:
            txt = to_say[: int(tts_max_chars)]
            tts = gTTS(text=txt, lang="en", slow=False)
            filename = "voice.mp3"
            tts.save(filename)
            sound = sounds.Sound(source=f"{filename}")
            self.is_speaking = True
            self.player.play(sound)

    def cleanse_message(self, message):
        to_say = re.sub(r"https?\S+\s?", "some link ", message)
        rx = re.compile(r"(.)\1{9,}")
        lines = to_say.split(" ")
        for line in lines:
            rxx = rx.search(line)
            if rxx:
                to_say = "Im an annoying fuck"
        to_say = re.sub(r"\d{8,}", "a fucking huge number", to_say)

        if check_for_repeats(to_say):
            to_say = "I used to be a really fucking annoying tts"
        # 	Checks to make sure there is actually an alpha numeric char in the string
        # So TTS doesnt freak out and crash
        if re.search(r"[a-zA-Z0-9]", to_say):
            return to_say
        else:
            return "Fuck you"


    # Loop that handles for interrupt from the dashboard front end
    async def tts_task(self):
        while True:
            await asyncio.sleep(0.2)
            if self.bot.interrupt_tts:
                self.bot.interrupt_tts = False
                self.player.stop()

            elif not self.is_speaking and len(self.message_queue) > 0:
                self.tts_speak(self.message_queue[0][1])
                self.user_speaking = self.message_queue[0][0]
                self.message_queue.pop(0)

    

    async def obs_tts_loop(self):
        connect_event = {
            "event": "CONNECT",
            "client": "TWITCHIO_CLIENT"
        }
        try:
            async with websockets.connect(obs_ws_server) as websocket:
                await websocket.send(json.dumps(connect_event))
                while True:
                    # if speaking Send speaking event to OBS
                    if self.is_speaking:
                        speaking_event = {
                            "event": "IS_SPEAKING",
                            "client": "TWITCHIO_CLIENT",
                            "user": self.user_speaking
                        }
                        await websocket.send(json.dumps(speaking_event))

                        # yeild while speaking
                        while self.is_speaking:
                            await asyncio.sleep(0.1)

                        else:
                            speaking_complete_event = {
                                "event": "SPEAKING_COMPLETE",
                                "client": "TWITCHIO_CLIENT",
                            }
                            await websocket.send(json.dumps(speaking_complete_event))
                    else:
                        await asyncio.sleep(0)

        # Can be connection refused error
        except OSError as e:
            for sub_exception in e.args:
                print('WS connection to OBS/TTS server has been refused')


def prepare(bot: Bot):
    bot.add_cog(OnMessage(bot))
