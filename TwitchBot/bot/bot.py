from pathlib import Path

import twitchio
from twitchio.ext import commands, sounds
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pytz import utc

from bot import config

# from ..Terrace.db import Database
import websockets


class Bot(commands.Bot):
    def __init__(self) -> None:
        self.modules: list[str] = [p.stem for p in Path("./bot/cogs").glob("*.py")]
        self.scheduler = AsyncIOScheduler()
        self.scheduler.configure(timezone=utc)
        # self.db = Database(self)
        self.communication = ["test"]
        self.tts = True
        self.interrupt_tts = False

        super().__init__(
            prefix=config.PREFIX,
            initial_channels=config.INITIAL_CHANNELS,
            irc_token=config.IRC_TOKEN,
            nick=config.NICK,
            token=config.ACCESS_TOKEN,
        )

    def setup(self) -> None:
        print("Running setup....")
        print(self.modules)
        
        p = Path("./bot/cogs")
        print(p.is_dir)

        for cog in self.modules:
            print(cog)
            self.load_module(f"bot.cogs.{cog}")

    def run(self) -> None:
        self.setup()
        print("Running bot...")
        super().run()

    async def event_join(self, channel: twitchio.Channel, user: twitchio.User) -> None:
        if user.name == config.NICK:
            await channel.send(f"{config.NICK} is now online!!")

    async def event_ready(self):
        # await self.db.connect()
        print("Connected to database")
        self.scheduler.start()
        print(f"Scheduler started ({len(self.scheduler.get_jobs()):,} job(s))")
        print(f"Logged in as | {self.nick}")
        print(f"User id is | {self.user_id}")

    async def event_message(self, message: twitchio.Message) -> None:
        print(message.content)
        if not message.author or message.author.name == config.NICK:
            return
        await self.handle_commands(message)
