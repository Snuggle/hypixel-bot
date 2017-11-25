import discord
from discord.ext import commands
import hypixel
from time import strftime, gmtime, time
from math import floor
import asyncio
from lib import database
cacheTime = 172800

async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

class PlayerCard:
    playerObject = None
    playerInfo = None
    ctx = None
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    rankColours = {'MVP': 0x55FFFF, 'VIP': 0x55FF55, 'MVP+': 0x55FFFF, 'VIP+': 0x55FF55, 'Non': 0xAAAAAA, 'Helper': 0x5555FF, 'Moderator': 0x00AA00, 'Admin': 0xFF5555, 'Youtuber': 0xFFAA00, 'Build Team': 0x00AAAA, 'Owner': 0xFF5555, 'None': 0xAAAAAA, 'Mixer': 0x00AAAA}
    dataItems = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp', 'displayName', 'rank', 'networkLevel', 'socialMedia']
    socialLinks = ['YOUTUBE', 'TWITTER', 'HYPIXEL', 'DISCORD', 'MIXER']
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    async def gameStats(self, messageObject, ctx):
        embedObject = embedObject = discord.Embed(color=0xFFAA00, title=f"{self.playerInfo['playerTitle']} {self.playerInfo['displayName']} > Games", \
        description="Please select a game from the list below!", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.
        embedObject.add_field(name="<:ender_eye:382805951813517312>", value="Skywars")
        embedObject.add_field(name="<:slimeball:382806071137402890>", value="Arcade Games")
        embedObject.add_field(name="Emoji", value="Etc...")
        embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
        embedObject.set_footer(text=f"{self.footerText}", icon_url=self.bot.user.avatar_url)

        await messageObject.edit(embed=embedObject)
        await messageObject.add_reaction(":diamond_sword:382807356334931968")
        await messageObject.add_reaction(":slimeball:382806071137402890")
        await messageObject.add_reaction(":ender_eye:382805951813517312")
        await messageObject.add_reaction(":apple_golden:382805390682750976")
        await messageObject.add_reaction(":stone_axe:382806557282402305")

    async def do_buttons(self, messageObject, ctx):
        await messageObject.add_reaction("\U00002139")
        await messageObject.add_reaction("\U0001F3AE")
        await messageObject.add_reaction("\U0001F4AC")
        def reaction_info_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) == '\U0001F3AE'

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await messageObject.clear_reactions()
        else:
            await messageObject.clear_reactions()
            await self.gameStats(messageObject, ctx)


    @commands.command(name='player', aliases=['Player', 'PLAYER'])
    async def PlayerCard(self, ctx, player: str):
        await ctx.channel.trigger_typing()
        hypixel.setCacheTime(cacheTime)
        try:
            startTime = time()

            if "<@" in player:
                mention = ctx.message.mentions[0]
                player = await database.findMinecraftUUID(str(mention.id))
                if player is False:
                    raise hypixel.PlayerNotFoundException

            self.playerObject = hypixel.Player(player)
            self.playerInfo = self.playerObject.getPlayerInfo()
            self.ctx = ctx

            for data in self.dataItems:
                if data == "socialMedia":
                    if 'socialMedia' not in self.playerInfo:
                        self.playerInfo['socialMedia'] = {}
                    if 'links' not in self.playerInfo['socialMedia']:
                        self.playerInfo['socialMedia']['links'] = {}
                    for link in self.socialLinks:
                        if link not in self.playerInfo['socialMedia']['links']:
                            self.playerInfo['socialMedia']['links'][link] = 'N/A'

                if data not in self.playerInfo:
                    self.playerInfo[data] = 'N/A'

            playerRank = self.playerInfo['rank']
            try:
                playerTitle = self.playerInfo['prefix'].title().split('[')[1]
                playerTitle = playerTitle.replace(']', '')
            except KeyError:
                playerTitle = playerRank['rank']

            playerColour = self.rankColours.get(playerTitle, self.rankColours[playerRank['rank']])
            self.playerInfo['playerColour'] = playerColour
            self.playerInfo['playerTitle'] = playerTitle

            embedObject = discord.Embed(color=playerColour, title=f"{playerTitle} {self.playerInfo['displayName']}", \
            description="\u200B", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.

            try:
                forumsLink = self.playerInfo['socialMedia']['links']['HYPIXEL']
            except KeyError:
                forumsLink = "Unlinked"
            try:
                discordName = self.playerInfo['socialMedia']['links']['DISCORD']
                discordID = discord.utils.get(ctx.channel.members, name=discordName.split('#')[0], discriminator=discordName.split('#')[1])
                if discordID is not None:
                    discordID = discordID.id
                    discordName = f'<@{discordID}>'
            except:
                discordName = "`Unlinked`"


            if playerRank['wasStaff'] == False:
                embedObject.add_field(name="Rank", value=f"`{playerRank['rank']}`")
            else:
                embedObject.add_field(name="Rank", value=f"`{playerRank['rank']} (Ex-Staff/YouTuber)`")

            GuildID = self.playerObject.getGuildID()
            if GuildID is not None:
                tempGuild = hypixel.Guild(GuildID)
                GuildID = tempGuild.JSON['name']

            firstLogin = self.playerInfo['firstLogin']
            lastLogin = self.playerInfo['lastLogin']

            try: # Optional formatting
                firstLogin = strftime("%Y-%m-%d", gmtime(int(self.playerInfo['firstLogin']) / 1000.0))
                lastLogin = strftime("%Y-%m-%d", gmtime(int(self.playerInfo['lastLogin']) / 1000.0))
                self.playerInfo['karma'] = f"{int(self.playerInfo['karma']):,}"
            except:
                pass

            embedObject.add_field(name="Level", value=f"`{floor(self.playerInfo['networkLevel']*100)/100}`") # Floor the network level to 2dp.
            embedObject.add_field(name="Minecraft Version", value=f"`{self.playerInfo['mcVersionRp']}`")     # E.g: 368.86864043126684 -> 368.68
            embedObject.add_field(name="Guild", value=f"`{GuildID}`")
            embedObject.add_field(name="Karma", value=f"`{self.playerInfo['karma']}`")
            embedObject.add_field(name="First / Last Login", value=f"`{firstLogin} / {lastLogin}`")
            embedObject.add_field(name="Discord", value=f"{discordName}")
            if forumsLink == "Unlinked":
                embedObject.add_field(name="Forums", value=f"`Unlinked`")
            else:
                embedObject.add_field(name="Forums", value=f"[View]({forumsLink}) forum account.")
            embedObject.set_image(url=f"https://visage.surgeplay.com/full/256/{self.playerInfo['displayName']}")
            embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
            embedObject.set_footer(text=f'{self.footerText} | {ctx.author}', icon_url=self.bot.user.avatar_url)
            messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            playerInfo = self.playerInfo
            await database.populatePlayer(ctx, playerInfo)
            print(f" > Replied in {round(time()-startTime, 2)}s.")
            await soft_delete(ctx)

            await self.do_buttons(messageObject, ctx)
        except hypixel.PlayerNotFoundException:
            print(f" > Player not found.")
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await soft_delete(ctx)



def setup(bot):
    bot.add_cog(PlayerCard(bot))
