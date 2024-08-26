from twitchio.ext import commands
from ..bot import Bot
import json
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
from bot.cogs.models.models import Model, IsSpeaking, SpeakingComplete, ConnectTwitch, ConnectOBS
from pydantic_core._pydantic_core import ValidationError

server_ip = "localhost"
port = 8181
clients = {
    "TWITCHIO_CLIENT": None,
    "OBS_CLIENT": None
}

class Tts_server(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        bot.loop.create_task(self.main())

    async def main(self):
        await serve(self.server, server_ip, port)

    async def server(self, websocket):
        global clients
        try:
            async for message in websocket:
                try:
                    validated_msg = Model(data=json.loads(message)).data
                    match validated_msg:
                        case ConnectTwitch(client=client) | ConnectOBS(client=client):
                            clients[client] = websocket
                            client_name = client

                        case IsSpeaking(user=user):
                            if clients['OBS_CLIENT'] is not None:
                                await clients['OBS_CLIENT'].send(validated_msg.model_dump_json())

                        case SpeakingComplete():
                            if clients['OBS_CLIENT'] is not None:
                                await clients['OBS_CLIENT'].send(validated_msg.model_dump_json())

                except ValidationError:
                    raise

        except (ConnectionClosedOK, ConnectionClosedError):
            clients[client_name] = None

def prepare(bot: commands.Bot):
    bot.add_cog(Tts_server(bot))
