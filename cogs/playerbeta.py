import discord
from discord.ext import commands
import hypixel
from time import strftime, gmtime, time
from math import floor
import asyncio

# CREATE A DICTIONARY OF ALL GETPLAYERINFO() REQUESTS TO CACHE

class PlayerCard:
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    rankColours = {'MVP': 0x55FFFF, 'VIP': 0x55FF55, 'Non': 0xAAAAAA, 'Helper': 0x5555FF, 'Moderator': 0x00AA00, 'Admin': 0xFF5555, 'Youtuber': 0xFFAA00, 'Build Team': 0x00AAAA}
    dataItems = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp', 'displayName', 'rank', 'networkLevel']

    messageObject = None
    playerObject = None


    def __init__(self, bot):
        self.bot = bot

    async def do_buttons(self, messageObject, playerObject, ctx):
        await messageObject.add_reaction("\U00002139")
        await messageObject.add_reaction("\U0001F3AE")
        await messageObject.add_reaction("\U0001F4AC")
        playerInfo = playerObject.getPlayerInfo()
        playerRank = playerInfo['rank']
        playerColour = self.rankColours[playerRank['rank'].replace('+', '')]
        def reaction_info_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U00002139'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await messageObject.clear_reactions()
        else:
            await messageObject.clear_reactions()
            embedObject = embedObject = discord.Embed(color=0xFFAA00, title=f"{playerRank['rank']} {playerInfo['displayName']}", \
            description="\u200B Please select a game from the list below!", url=f"https://hypixel.net/player/{playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.
            embedObject.add_field(name="<:ender_eye:382805951813517312>", value="Skywars")
            embedObject.add_field(name="<:slimeball:382806071137402890>", value="Arcade Games")
            embedObject.add_field(name="Emoji", value="Etc...")
            embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
            embedObject.set_footer(text=f"{self.footerText} | UUID: {playerInfo['uuid']}", icon_url=self.bot.user.avatar_url)

            await messageObject.edit(embed=embedObject)
            await messageObject.add_reaction(":diamond_sword:382807356334931968")
            await messageObject.add_reaction(":slimeball:382806071137402890")
            await messageObject.add_reaction(":ender_eye:382805951813517312")
            await messageObject.add_reaction(":apple_golden:382805390682750976")
            await messageObject.add_reaction(":stone_axe:382806557282402305")

    @commands.command(name='player', aliases=['Player', 'PLAYER'])
    async def cog_player(self, ctx, player: str):
        await ctx.channel.trigger_typing()
        try:
            startTime = time()

            playerObject = hypixel.Player(player)
            playerInfo = playerObject.getPlayerInfo()
            for data in self.dataItems:
                if data not in playerInfo:
                    playerInfo[data] = 'N/A'

            playerRank = playerInfo['rank']
            playerColour = self.rankColours[playerRank['rank'].replace('+', '')]

            embedObject = embedObject = discord.Embed(color=playerColour, title=f"{playerRank['rank']} {playerInfo['displayName']}", \
            description="\u200B", url=f"https://hypixel.net/player/{playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.

            try:
                forumsLink = playerObject.JSON['socialMedia']['links']['HYPIXEL']
            except KeyError:
                forumsLink = "Unlinked"
            try:
                discordName = playerObject.JSON['socialMedia']['links']['DISCORD']
                discordID = discord.utils.get(ctx.channel.members, name=discordName.split('#')[0], discriminator=discordName.split('#')[1]).id
                if discordID is not None:
                    discordName = f'<@{discordID}>'
            except KeyError:
                discordName = "Unlinked"


            if playerRank['wasStaff'] == False:
                embedObject.add_field(name="Rank", value=f"`{playerRank['rank']}`")
            else:
                embedObject.add_field(name="Rank", value=f"`{playerRank['rank']} (Ex-Staff/YouTuber)`")

            GuildID = playerObject.getGuildID()
            if GuildID is not None:
                tempGuild = hypixel.Guild(GuildID)
                GuildID = tempGuild.JSON['name']


            firstLogin = strftime("%Y-%m-%d", gmtime(int(playerInfo['firstLogin']) / 1000.0))
            lastLogin = strftime("%Y-%m-%d", gmtime(int(playerInfo['lastLogin']) / 1000.0))
            try:
                playerInfo['karma'] = f"{int(playerInfo['karma']):,}"
            except:
                pass


            embedObject.add_field(name="Level", value=f"`{floor(playerInfo['networkLevel']*100)/100}`") # Floor the network level to 2dp.
            embedObject.add_field(name="Minecraft Version", value=f"`{playerInfo['mcVersionRp']}`")     # E.g: 368.86864043126684 -> 368.68
            embedObject.add_field(name="Guild", value=f"`{GuildID}`")
            embedObject.add_field(name="Karma", value=f"`{playerInfo['karma']}`")
            embedObject.add_field(name="First / Last Login", value=f"`{firstLogin} / {lastLogin}`")
            embedObject.set_image(url=f"https://visage.surgeplay.com/full/256/{playerInfo['displayName']}")
            embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
            embedObject.set_footer(text=f'{self.footerText} | {ctx.author}', icon_url=self.bot.user.avatar_url)
            messageObject = await ctx.send(content=None, embed=embedObject, delete_after=60.0)
            print(f"hypixel-player {playerInfo['displayName']} took {time()-startTime} seconds to reply.")
            await ctx.message.delete()

            await self.do_buttons(messageObject, playerObject, ctx)
        except hypixel.PlayerNotFoundException:
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject)



def setup(bot):
    bot.add_cog(PlayerCard(bot))
