from discord.ext import commands
import discord
import asyncio
import hypixel

from hypixelbot import database, utility

class LinkCog:
    deleteTime = 60.0
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

    def __init__(self, bot):
        self.bot = bot

    async def checkForLink(self, player):
        hypixel.setCacheTime(0)
        playerObject = hypixel.Player(player)
        playerInfo = playerObject.getPlayerInfo()
        discordLink = playerObject.JSON['socialMedia']['links']['DISCORD']
        hypixel.setCacheTime(60)
        return discordLink

    @commands.command(name='link', aliases=['linkdiscord', 'discordlink', 'LINK'])
    async def linkDiscord(self, ctx, player: str):
        discordLink = await self.checkForLink(player)
        descriptionString = (f"Please join the Hypixel Network, enter a lobby and click your head in your hotbar. Click \"Social Media\" and then Discord.\n"
                             f"In the chat, please type `Snuggle#1234`.\n"
                             f"After you have linked your Discord account in-game, please click the refresh button below.\n"
                             f"This Minecraft account is currently linked to `{discordLink}`")

        embedObject = discord.Embed(color=0xCDA040, title="Link your Discord Account!", description=descriptionString)
        messageObject = await ctx.send(content='None', embed=embedObject, delete_after=self.deleteTime)
        await ctx.send(content='https://youtu.be/dHXagBm5M5I')
        await messageObject.add_reaction("\U0001F504")

        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id and reaction.emoji == "\U0001F504"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            discordLink = await self.checkForLink(player)
            print(f"Discord Link: {DiscordLink}")
            if discordLink is None:
                pass
            else:
                embedObject = discord.Embed(color=0xCDA040, title="Link your Discord Account!", description=f"Your Discord Account has been linked to `{discordLink}`")
                await database.populatePlayer()




def setup(bot):
    bot.add_cog(LinkCog(bot))
