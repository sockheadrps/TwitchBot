from pydantic import BaseModel, Field
from typing import Literal, Union, Annotated


class ConnectOBS(BaseModel):
    event: Literal['CONNECT']
    client: Literal['OBS_CLIENT']

class ConnectTwitch(BaseModel):
    event: Literal['CONNECT']
    client: Literal['TWITCHIO_CLIENT']

class IsSpeaking(BaseModel):
    event: Literal['IS_SPEAKING']
    user: str
    level: int

class SpeakingComplete(BaseModel):
    event: Literal['SPEAKING_COMPLETE']


Connect = Annotated[Union[ConnectOBS, ConnectTwitch], Field(discriminator='client')]
Event = Annotated[Union[Connect, IsSpeaking, SpeakingComplete], Field(discriminator='event')]


class Model(BaseModel):
    data: Event
