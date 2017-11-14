from discord.ext import commands
import discord

class OwnerCog:

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='load')
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='unload')
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='reload')
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')

    @commands.command(name='forcestop')
    @commands.is_owner()
    async def cog_forcestop(self, ctx):
        await ctx.send("Goodbye!")
        exit()

    @commands.command(name='setgame')
    @commands.is_owner()
    async def cog_setgame(self, ctx):
        streamingBool = 0
        urlString = None
        message = ctx.message.content.replace('hypixel-setgame ', '').split(', ')
        if 'twitch.tv' in ctx.message.content:
            streamingBool = 1
            urlString = message[2]
        status = getattr(discord.Status, message[0])
        game = discord.Game(name=f"{message[1]}", type=streamingBool, url=urlString)

        await self.bot.change_presence(game=game, status=status, afk=False)
        print(f" > Changed presence to {message[1]}.")

    @commands.command(name='test')
    async def cog_test(self, ctx):
        embedObject = discord.Embed(color=0xCDA040, title="Hypixel-bot Ping", description=f"A ping took {round(self.bot.latency*1000, 2)} milliseconds.")
        await ctx.send(content=None, embed=embedObject, delete_after=10.0)



def setup(bot):
    bot.add_cog(OwnerCog(bot))