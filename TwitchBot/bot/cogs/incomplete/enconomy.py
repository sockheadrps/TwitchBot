from twitchio.ext import commands, sounds
from ..bot import Bot
import asyncio


class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.event()
    async def event_ready(self):
        pass

    @commands.Cog.event()
    async def event_message(self, message):
        print(f"{message.author.name}, {message.content}")
        await self.save_message(message.author.name, message.content)
        user = await self.bot.db.record(
            """
            SELECT * FROM economy where UserName = ?
            """
            , message.author.name)
        if len(user) > 0:
            user_name = user[0][0]
            credits = user[0][1] + 5
            print(f"{user_name}, has {credits} credits")
            await self.bot.db.execute(
                '''
                UPDATE economy SET Credits = ?
                WHERE UserName = ?
                ''',
                credits,
                user_name
            )
            await self.bot.db.commit()
        else:
            sql = """
                INSERT INTO economy
                (UserName, Credits)
                VALUES(?, ?)
            """
            await self.bot.db.execute(sql, message.author.name, 100)
            await self.bot.db.commit()
            # Create user, init with 100 credits
        
    
    async def save_message(self, user, message):
        # TODO change to messages table, add username, userid field
        users_schema = f"""
		CREATE TABLE IF NOT EXISTS {user} (
		Message TEXT,
        Timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		);
		"""
        sql = f"""
        INSERT INTO {user} (Message, Timestamp)
        VALUES (?, CURRENT_TIMESTAMP);
        """
        await self.bot.db.execute(users_schema)
        await self.bot.db.execute(sql, message)
        await self.bot.db.commit()


def prepare(bot: Bot):
    bot.add_cog(Economy(bot))
