from twitchio.ext import commands
from ..bot import Bot
from aiodesa import Db


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot 
        print('help cog loaded')
    
    @commands.command(aliases='bot')
    async def twitchbot(self, ctx: commands.Context):
        link = 'https://github.com/sockheadrps/TwitchBot'
        await ctx.send(f'twitchbot code: {link}')

    @commands.command(aliases=('gh',))
    async def github(self, ctx: commands.Context):
        link = 'https://github.com/sockheadrps/'
        await ctx.send(f'Github: {link}')
        
    @commands.command()
    async def level(self, ctx: commands.Context) -> None:
        user = ctx.author.name 
        async with Db("database.sqlite3") as db:
            await db.read_table_schemas(self.bot.UserEcon)
            find = db.find(self.bot.UserEcon)
            author = await find(user)
            print(author)
            if author == None:
                pass
            else:
                await ctx.send(f"{user} is level {author.level}")



# Prepare function needed to load the class instance
def prepare(bot: Bot):
    bot.add_cog(Help(bot))
