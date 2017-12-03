from discord.ext import commands
import discord

from hypixelbot import utility

class LinkCog:
    deleteTime = 60.0
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='link', aliases=['linkdiscord', 'discordlink', 'LINK'])
    async def linkDiscord(self, ctx):
        embedObject = discord.Embed(color=0xCDA040, title=f"Link Your Discord Account!", description=f"Please join the Hypixel Network")


def setup(bot):
    bot.add_cog(LinkCog(bot))
