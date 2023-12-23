from pathlib import Path
import twitchio
from twitchio.ext import commands
from bot import config
from dataclasses import dataclass
from aiodesa.utils.table import ForeignKey, UniqueKey, PrimaryKey, set_key


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs) -> None:
        self.modules: list[str] = [p.stem for p in Path("./bot/cogs").glob("*.py")]
        self.db = None
        self.communication = ["test"]
        self.tts = True
        self.interrupt_tts = False
        self.channel = None

        @dataclass
        @set_key(PrimaryKey("username"))
        class UserEcon:
            username: str
            credits: int | None = None
            points: int | None = None
            level: int = 0
            table_name: str = "user_economy"
        self.UserEcon = UserEcon


        super().__init__(
            prefix=config.PREFIX,
            initial_channels=config.INITIAL_CHANNELS,
            nick=config.NICK,
            token=config.ACCESS_TOKEN,
        )

    def setup_cogs(self) -> None:
        p = Path("./bot/cogs")
        for cog in self.modules:
            print(cog)
            self.load_module(f"bot.cogs.{cog}")

    def run(self) -> None:
        self.setup_cogs()
        print("Running bot...")
        super().run()

    async def event_join(self, channel: twitchio.Channel, user: twitchio.User) -> None:
        if user.name == config.NICK:
            await channel.send(f"{config.NICK} is now online!!")
            self.channel = channel

    async def event_ready(self):
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message: twitchio.Message) -> None:
        print(message.content)
        # if not message.author or message.author.name == config.NICK:
        #     return
        await self.handle_commands(message)
    
