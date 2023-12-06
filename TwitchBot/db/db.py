from pathlib import Path
import aiosqlite
from schemas import schemas
from dataclasses import dataclass, fields

import asyncio

class Database:
	def __init__(self) -> None:
		self.db_path = Path("data/database.sqlite3")
		self._create_db()
		self.conn = None

	def _create_db(self):
		if not self.db_path.exists():
			self.db_path.parent.mkdir(parents=True, exist_ok=True)
			self.db_path.touch()

	
	async def create_tables(self):
		async def table_exists(table_name):
			query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
			cursor = await self.conn.execute(query, (table_name,))
			return await cursor.fetchone() is not None

		name = schemas.economy.table_name
		schema = schemas.economy.sql

		if not await table_exists(name):
			async with self.conn.executescript(schema) as cursor:
				await cursor.fetchall()
			await self.conn.commit()

	
	async def insert_into(self, table_name, econ_user):
		field_names = [field for field in econ_user.__annotations__]
		values = [getattr(econ_user, i) for i in field_names]
		columns = ', '.join(field_names)
		placeholders = ', '.join('?' for _ in values)
		sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
		
		await self.conn.execute(sql, values)
		await self.conn.commit()


	async def update_table(self, table_name, econ_user):
		field_names = [field for field in econ_user.__annotations__]
		values = [getattr(econ_user, i) for i in field_names]

		set_clause = ', '.join(f"{column} = ?" for column in field_names)
		sql = f"UPDATE {table_name} SET {set_clause};"
		
		await self.conn.execute(sql, values)
		await self.conn.commit()


	async def connect(self):
		self.conn = await aiosqlite.connect(self.db_path)
		await self.create_tables()


	async def close(self):
		await self.conn.close()

	@staticmethod
	def economy_user(username, credits):

		@dataclass
		class Econ_user:
			username: str
			points: int
		return Econ_user(username, credits)


async def main():
	db = Database()
	await db.connect()
	await db.insert_into("economy", db.economy_user("sockheadrps", 100))
	await db.update_table("economy", db.economy_user("sockheadrps", 5000))
	await db.close()  

asyncio.run(main())

