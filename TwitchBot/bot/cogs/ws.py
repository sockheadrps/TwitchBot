from twitchio.ext import commands
from ..bot import Bot

import websockets
import json


class WS(commands.Cog):

	def __init__(self, bot: Bot):
		self.bot = bot
		bot.loop.create_task(self.ws_loop())

	async def ws_loop(self):
		connect_event = {
			"event": "CONNECT",
			"client-type": 'SERVICE',
			"client-name": "Twitch",
		}
		try:
			async with websockets.connect("ws://192.168.1.136:8081/ws/stats") as websocket:
				try:
					await websocket.send(json.dumps(connect_event))
					while True:
						data = await websocket.recv()
						data = json.loads(data)
						if data.get("data"):
							print(data)
							if data['data']['COMMAND'] == "TTS":
								self.bot.tts = data['data']['value']
							if data['data']['COMMAND'] == "STOP-TTS":
								self.bot.interrupt_tts = True

				except Exception as e:
					raise e
				finally:
					await websocket.send('{"event":  "TWITCH_CLOSE"}')
		except ConnectionRefusedError:
			print('WS connection to dashboard has been refused')


def prepare(bot: commands.Bot):
	bot.add_cog(WS(bot))
