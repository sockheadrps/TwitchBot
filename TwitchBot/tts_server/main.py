import asyncio
from websockets.server import serve
from websockets.exceptions import ConnectionClosedOK, ConnectionClosedError
import json
from models import Model, IsSpeaking, SpeakingComplete, ConnectTwitch, ConnectOBS
from pydantic_core._pydantic_core import ValidationError


server_ip = "localhost"
port = 8181
clients = {
    "TWITCHIO_CLIENT": None,
    "OBS_CLIENT": None
}


async def server(websocket):
    global clients
    client_name: str 
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


async def main():
    async with serve(server, server_ip, port):
        await asyncio.Future()


asyncio.run(main())

