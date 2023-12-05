from pathlib import Path
import aiosqlite
from twitchio.ext import commands
from schemas import schemas

import asyncio

TEST_SQL = """
	INSERT INTO economy
	(UserName, Credits)
	VALUES('sockheadrps', 100)
"""
class Database:
	def __init__(self) -> None:
		self.db_path = Path("data/database.sqlite3")
		self._create_db()
		self.conn = None

	def _create_db(self):
		if not self.db_path.exists():
			self.db_path.parent.mkdir(parents=True, exist_ok=True)
			self.db_path.touch()
			print(f"Empty database file '{self.db_path}' created successfully.")
		else:
			print(f"Database file '{self.db_path}' already exists.")
	
	async def table_exists(self, table_name):
		if self.conn:
			query = f"SELECT name FROM sqlite_master WHERE type='table' AND name=?;"
			cursor = await self.conn.execute(query, (table_name,))
			return await cursor.fetchone() is not None
		else:
			print("Connection not established.")
			return False
	
	async def create_table(self, schema):
		if not self.conn:
			return
		table_name = schema.get("table_name")
		if not table_name:
			return
		
		if not await self.table_exists(table_name):
			sql = schema.get("sql")
			try:
				async with self.conn.execute_script(sql) as cursor:
					await cursor.fetchall()
				await self.conn.commit()
				print(f"Table '{table_name}' created using schema.")
			except aiosqlite.Error as e:
				print(f"Error creating table: {e}")

		else:
			print(f"Table '{table_name}' already exists.")

	
	async def insert_into(self, table_name, values_dict):
		if self.conn:
			columns = ', '.join(values_dict.keys())
			placeholders = ', '.join('?' for _ in values_dict)
			sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"
			
			try:
				await self.conn.execute(sql, list(values_dict.values()))
				await self.conn.commit()
				print(f"Inserted values into table '{table_name}'.")
			except aiosqlite.Error as e:
				print(f"Error inserting into table: {e}")
			print(f"Inserted values into table '{table_name}'.")
		else:
			print("Connection not established.")

	async def update_table(self, table_name, new_values):
		if self.conn:
			set_clause = ', '.join(f"{column} = ?" for column in new_values.keys())
			values = list(new_values.values())

			sql = f"UPDATE {table_name} SET {set_clause};"
			
			try:
				await self.conn.execute(sql, values)
				await self.conn.commit()
				print(f"Updated values in table '{table_name}'.")
			except aiosqlite.Error as e:
				print(f"Error updating table: {e}")
		else:
			print("Connection not established.")

	async def connect(self):
		self.conn = await aiosqlite.connect(self.db_path)

	async def close(self):
		if self.conn:
			await self.conn.commit()
			await self.conn.close()


async def main():
	db = Database()
	await db.connect()  # Ensure the connection is established before creating the table
	await db.create_table(schemas.schema_econ)
	await db.insert_into("economy", {"UserName": "sockheadrps", "credits": "100"})
	await db.update_table("economy", {"UserName": "sockheadrps", "credits": "300"})
	await db.create_table(schemas.schema_econ)
	await db.update_table("economy", {"UserName": "sockheadrps", "credits": "3020"})
	await db.close()  # Close the connection after creating the table

# Run the event loop to execute the asynchronous code
asyncio.run(main())

