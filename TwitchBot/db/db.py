from pathlib import Path
import aiosqlite
from schemas import schemas
from dataclasses import dataclass
from typing import Optional

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

		if not await table_exists(schemas.user.table_name):
			async with self.conn.executescript(schemas.user.sql) as cursor:
				await cursor.fetchall()
			await self.conn.commit()

	
	async def insert_into(self, table_name, user):
		field_names = [field for field in user.__annotations__]
		values = [getattr(user, i) for i in field_names if getattr(user, i) is not None]
		print(values)
		non_none_columns = [
			(field, value) for field, value in zip(field_names, values) if value is not None
			]
		columns, filtered_values = zip(*non_none_columns)
		columns_str = ', '.join(columns)
		placeholders = ', '.join('?' for _ in filtered_values)
		sql = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
		
		await self.conn.execute(sql, values)
		await self.conn.commit()


	async def update_table(self, table_name, user):
		field_names = [field for field in user.__annotations__]
		values = [getattr(user, i) for i in field_names]

		# Filter out None values and their corresponding columns
		non_none_columns_with_values = [(field, value) for field, value in zip(field_names, values) if value is not None]

		columns, filtered_values = zip(*non_none_columns_with_values)
		set_clause = ', '.join(f"{column} = ?" for column in columns)
		sql = f"UPDATE {table_name} SET {set_clause};"

		await self.conn.execute(sql, filtered_values)
		await self.conn.commit()


	async def connect(self):
		self.conn = await aiosqlite.connect(self.db_path)
		await self.create_tables()


	async def close(self):
		await self.conn.close()

	@staticmethod
	def user(username, credits=None, points=None):

		@dataclass
		class User:
			username: str
			credits: Optional[int] 
			points: Optional[int] 
		return User(username, credits, points)


async def main():
	db = Database()
	await db.connect()
	await db.insert_into("users", db.user("sockheadrps"))
	await db.update_table("users", db.user(username="sockheadrps", credits=5000))
	await db.close()  

asyncio.run(main())

