from discord.ext import commands
import discord
import asyncio
import hypixel
import string
from random import choice

from hypixelbot import database, utility

class LinkCog:
    deleteTime = 120.0
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

    def __init__(self, bot):
        self.bot = bot

    async def checkForLink(self, ctx, player):
        hypixel.setCacheTime(0)
        playerObject = hypixel.Player(player)
        playerInfo = playerObject.getPlayerInfo()
        discordLink = playerObject.JSON['socialMedia']['links']['DISCORD']
        hypixel.setCacheTime(60)
        await database.populatePlayer(ctx, playerInfo)
        return discordLink

    async def forceLink(self, ctx, player, verifyString):
        playerObject = hypixel.Player(player)
        playerInfo = playerObject.getPlayerInfo()
        print("BRRRRRRRRRRRRRRRRRRRRRRRRRR")
        await database.forceLink(playerInfo, ctx.author.id, verifyString)

    def generateVerifyString(self, size):
        return ''.join(choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(size))

    @commands.command(name='link', aliases=['linkdiscord', 'discordlink', 'LINK'])
    async def linkDiscord(self, ctx, player: str):
        discordLink = await self.checkForLink(ctx, player)
        verifyString = f"discord.gg/verify{self.generateVerifyString(4)}"
        descriptionString = (f"Please join the Hypixel Network, enter a lobby and click your head in your hotbar.\nClick \"Social Media\" and then Discord. "
                             f"Please type `{verifyString}`.\n\n"
                             f"After you have linked your Discord account in-game, please click the tick button below.\n\n"
                             f"This Minecraft account is currently linked to `{discordLink}`")

        embedObject = discord.Embed(color=0xCDA040, title="Link your Discord Account", description=descriptionString)
        messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
        await ctx.send(content="Here's a small tutorial: https://youtu.be/dHXagBm5M5I", delete_after=self.deleteTime)
        await messageObject.add_reaction("\U00002714")

        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id and reaction.emoji == "\U00002714"

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=120.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            discordLink = await self.checkForLink(ctx, player)
            print(f"Discord Link: {discordLink}")
            if verifyString == discordLink:
                await self.forceLink(ctx, player, verifyString)
                embedObject = discord.Embed(color=0xCDA040, title="Link your Discord Account", description=f"`{player}` has been linked to <@{ctx.author.id}>")
            else:
                embedObject = discord.Embed(color=0xff5555, title="Link your Discord Account", description=f"Your verify code was `{verifyString}` but your Minecraft account showed `{discordLink}` instead.\n\n**Please try linking in-game again.**")

            await messageObject.delete()
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)




def setup(bot):
    bot.add_cog(LinkCog(bot))
