from discord.ext import commands


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
        ctx.send("Goodbye!")
        exit()

    @commands.command(name='test')
    async def cog_test(self, ctx):
        ctx.send("Tested!")



def setup(bot):
    bot.add_cog(OwnerCog(bot))