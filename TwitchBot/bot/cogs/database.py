from twitchio.ext import commands
from ..bot import Bot
from aiodesa import Db


def calculate_level(xp):
    base_xp = 10
    xp_multiplier = 1.2

    level = 1

    while xp >= base_xp:
        xp -= base_xp
        base_xp = int(base_xp * xp_multiplier)
        level += 1

    return level - 1

class DataBase(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.event()
	async def event_message(self, message):
		try:
			user = message.author.name
			async with Db("database.sqlite3") as db:
				# Create table from UserEcon class
				await db.read_table_schemas(self.bot.UserEcon)
				find = db.find(self.bot.UserEcon)
				author = await find(user)
				if author == None:
					insert = db.insert(self.bot.UserEcon)
					await insert(user, points=1, credits=100)
				else:
					current_level = calculate_level(author.points)
					points = author.points + 1
					update = db.update(self.bot.UserEcon)
					await update(user, points=points, level=calculate_level(points))
					if calculate_level(points) > current_level:
						await self.bot.channel.send(f"{user} has leveled up to {calculate_level(points)}")
		except Exception as e:
			print(e)

					
					
		except AttributeError:
			pass



def prepare(bot: Bot):
	bot.add_cog(DataBase(bot))
