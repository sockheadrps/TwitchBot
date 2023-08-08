from pathlib import Path

import aiosqlite
from apscheduler.triggers.cron import CronTrigger
from twitchio.ext import commands
from Terrace import DATA_PATH
import os
import sqlite3

ORIGINAL_DATA_PATH = DATA_PATH
DB_PATH = DATA_PATH / "database.sqlite3"
BUILD_PATH = DB_PATH / "build.sql"
path = os.path.join(os.getcwd(), "/data/database.sqlite3")


class Database:
	__slots__ = ("bot", "cxn")

	def __init__(self, bot: commands.bot) -> None:
		self.bot = bot
		bot.scheduler.add_job(self.commit, CronTrigger(second=0))

	async def connect(self) -> None:
		await self.create_db()
		self.cxn = await aiosqlite.connect('./data/database.sqlite3')
		await self.cxn.commit()

	async def commit(self) -> None:
		await self.cxn.commit()

	async def close(self) -> None:
		await self.cxn.commit()
		await self.cxn.close()

	async def field(self, sql, *values):
		cur = await self.cxn.execute(sql, tuple(values))
		if (row := await cur.fetchone()) is not None:
			return row[0]

	async def record(self, sql, *values):
		cur = await self.cxn.execute(sql, tuple(values))
		return await cur.fetchall()

	async def column(self, sql, *values):
		cur = await self.cxn.execute(sql, tuple(values))
		return [row[0] for row in await cur.fetchall()]

	async def execute(self, sql, *values):
		cur = await self.cxn.execute(sql, tuple(values))
		return cur.rowcount

	async def executemany(self, sql, valueset):
		cur = await self.cxn.executemany(sql, valueset)
		return cur.rowcount

	async def executescript(self, path):
		with open(path, "r", encoding="utf-8") as script:
			await self.cxn.executescript(script.read())

	async def create_db(self):
		schema = """
		CREATE TABLE IF NOT EXISTS economy (
  	  	UserID INTERGER PRIMARY KEY,
    	Credits INTERGER DEFAULT 100,
   		Lock NUMERIC DEFAULT CURRENT_TIMESTAMP
		);
		"""
		path = os.path.join(os.getcwd(), "/data/database.sqlite3")

		if not os.path.exists(path):
			Path("./data/database.sqlite3").touch()

			with sqlite3.connect("./data/database.sqlite3") as db:
				db.execute(schema)
				db.commit()




