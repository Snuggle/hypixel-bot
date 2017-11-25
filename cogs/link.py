from discord.ext import commands
import discord

async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

class LinkCog:
    deleteTime = 60.0
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='link', aliases=['linkdiscord', 'discordlink', 'LINK'])
    async def cog_link(self, ctx):


def setup(bot):
    bot.add_cog(LinkCog(bot))
