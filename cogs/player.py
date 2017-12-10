import discord
from discord.ext import commands
import humanize
import hypixel
import json
from time import strftime, gmtime, time
import datetime
from math import floor
import asyncio
import ago
from hypixelbot import database, utility
cacheTime = 3600

gameStats = json.load(open('./hypixelbot/gameStats.json'))
rankMap = json.load(open('./hypixelbot/rankMap.json'))

class PlayerCard:
    playerObject = None
    playerInfo = None
    ctx = None
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    rankColours = {'MVP': 0x55FFFF, 'VIP': 0x55FF55, 'MVP+': 0x55FFFF, 'VIP+': 0x55FF55, 'Non': 0xAAAAAA, 'Helper': 0x5555FF, 'Moderator': 0x00AA00, 'Admin': 0xFF5555, 'MCProHosting': 0xFF5555, 'Youtuber': 0xFFAA00, 'Build Team': 0x00AAAA, 'Owner': 0xFF5555, 'None': 0xAAAAAA, 'Mixer': 0x00AAAA}
    dataItems = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp', 'displayName', 'rank', 'networkLevel', 'socialMedia']
    socialLinks = ['YOUTUBE', 'TWITTER', 'HYPIXEL', 'DISCORD', 'MIXER']
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    async def generateInfoCard(self, messageObject, ctx):
        embedObject = discord.Embed(color=self.playerInfo['playerColour'], title=f"{self.playerInfo['playerTitle']} {self.playerInfo['displayName']} > Miscellaneous Information", \
        description=f"\u200B", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}")

        i = 1; knownAliases = ""
        for alias in self.playerObject.JSON['knownAliases']:
            knownAliases = knownAliases + f"\n{i} | {alias}"
            i += 1

        embedObject.add_field(name=f"Minecraft UUID", value=f"`{self.playerObject.UUID}`", inline=True)
        embedObject.add_field(name=f"Network Experience", value=f"`{humanize.intword(self.playerInfo['networkExp'])}`", inline=True)
        embedObject.add_field(name=f"Known Usernames", value=f"```python\n{knownAliases[:1024]}```", inline=True)

        embedObject.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{self.playerObject.UUID}")
        embedObject.set_footer(text=f"{self.footerText}", icon_url=self.bot.user.avatar_url)
        await messageObject.edit(embed=embedObject)
        await messageObject.add_reaction("\U00002B05")

        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            if reaction.emoji == '\U00002B05':
                await self.PlayerProfile.callback(self=self, ctx=ctx, player=self.playerObject.UUID, edit=True, messageObject=messageObject)

    async def generateSocialCard(self, messageObject, ctx):
        embedObject = discord.Embed(color=self.playerInfo['playerColour'], title=f"{self.playerInfo['playerTitle']} {self.playerInfo['displayName']} > Social Media", \
        description=f"\u200B\nThis player has linked the following social media accounts:", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}")
        socialMedia = self.playerInfo['socialMedia']['links']
        for social in self.socialLinks:
            if 'http' in socialMedia[social] or 'https' in socialMedia[social]:
                embedObject.add_field(name=f"{social.title()}", value=f"[Click me!]({socialMedia[social]})", inline=True)
            else:
                embedObject.add_field(name=f"{social.title()}", value=f"`{socialMedia[social]}`", inline=True)

        embedObject.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{self.playerObject.UUID}")
        embedObject.set_footer(text=f"{self.footerText}", icon_url=self.bot.user.avatar_url)
        await messageObject.edit(embed=embedObject)
        await messageObject.add_reaction("\U00002B05")

        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            if reaction.emoji == '\U00002B05':
                await self.PlayerProfile.callback(self=self, ctx=ctx, player=self.playerObject.UUID, edit=True, messageObject=messageObject)

    async def generateGameCard(self, messageObject, ctx, reaction):
        for game in gameStats:
            if type(reaction.emoji) is 'str':
                emojiID = reaction.emoji
            else:
                emojiID = reaction.emoji.id
            if gameStats[game]['icon_id'] == reaction.emoji.id: # If true, correct game found.
                embedObject = discord.Embed(color=self.playerInfo['playerColour'], title=f"{self.playerInfo['playerTitle']} {self.playerInfo['displayName']} > {game}", \
                description=f"\u200B\n{gameStats[game]['description']}\n\u200B", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}")

                apiname = gameStats[game]['APIname']
                stats = self.playerObject.JSON['stats'][apiname]

                for statistic in gameStats[game]['statsToDisplay']:
                    try:
                        statisticValue = eval(statistic[1])
                        try:
                            statisticValue = int(statisticValue)
                            statisticValue = '{:,}'.format(statisticValue)
                        except ValueError:
                            pass
                        inlineVar = True
                        if "Coins" in statistic[0] or "Level" in statistic[0]:
                            inlineVar = False
                        embedObject.add_field(name=f"{statistic[0]}", value=f"`{statisticValue}`", inline=inlineVar)
                    except KeyError:
                        embedObject.add_field(name=f"{statistic[0]}", value=f"`·0`")

                embedObject.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{self.playerObject.UUID}")
                embedObject.set_image(url=reaction.emoji.url)
                embedObject.set_footer(text=f"{self.footerText}", icon_url=self.bot.user.avatar_url)
                await messageObject.edit(embed=embedObject)
                await messageObject.add_reaction("\U00002B05")

                def reaction_info_check(reaction, user):
                    return user == ctx.author and reaction.message.id == messageObject.id

                try:
                    reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
                except asyncio.TimeoutError:
                    await utility.soft_clear(messageObject)
                else:
                    await utility.soft_clear(messageObject)
                    await self.gameStats(messageObject, ctx)
                    if reaction.emoji == '\U00002B05':
                        await self.gameStats(messageObject, ctx)

    async def gameStats(self, messageObject, ctx):
        embedObject = embedObject = discord.Embed(color=self.playerInfo['playerColour'], title=f"{self.playerInfo['playerTitle']} {self.playerInfo['displayName']} > Games", \
        description="Please select a game from the list below!", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}")
        for game in gameStats:
            print(game)
            print(gameStats[game]['icon_uri'])
            embedObject.add_field(name=f"{gameStats[game]['icon_uri']}", value=game)
        embedObject.set_thumbnail(url=f"https://visage.surgeplay.com/bust/{self.playerObject.UUID}")
        embedObject.set_footer(text=f"{self.footerText}", icon_url=self.bot.user.avatar_url)

        await messageObject.edit(embed=embedObject)


        await messageObject.add_reaction("\U00002B05")
        for game in gameStats:
            await messageObject.add_reaction(gameStats[game]['icon_uri'].replace('<', '').replace('>', ''))

        def reaction_info_check(reaction, user):
            return user == ctx.author and reaction.message.id == messageObject.id

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
        except asyncio.TimeoutError:
            await utility.soft_clear(messageObject)
        else:
            await utility.soft_clear(messageObject)
            if reaction.emoji == '\U00002B05':
                await self.PlayerProfile.callback(self=self, ctx=ctx, player=self.playerObject.UUID, edit=True, messageObject=messageObject)
            else:
                await self.generateGameCard(messageObject, ctx, reaction)


    async def do_buttons(self, messageObject, ctx):
        try:
            unusedVariable = messageObject.channel.guild # If errors, this is is a direct message.
            await messageObject.add_reaction("\U00002139")
            await messageObject.add_reaction("\U0001F3AE")
            await messageObject.add_reaction("\U0001F4AC")
            def reaction_info_check(reaction, user):
                return user == ctx.author and reaction.message.id == messageObject.id

            try:
                reaction, user = await self.bot.wait_for('reaction_add', timeout=30.0, check=reaction_info_check)
            except asyncio.TimeoutError:
                await utility.soft_clear(messageObject)
            else:
                await utility.soft_clear(messageObject)
                if str(reaction.emoji) == '\U00002139':
                    await self.generateInfoCard(messageObject, ctx)
                elif str(reaction.emoji) == '\U0001F3AE':
                    await self.gameStats(messageObject, ctx)
                elif str(reaction.emoji) == '\U0001F4AC':
                    await self.generateSocialCard(messageObject, ctx)
        except AttributeError:
            await ctx.send("Due to Discord's limitations on bots, I cannot use buttons/reactions in `Direct Messages`. Sorry! :heart:")


    @commands.command(name='player', aliases=['Player', 'PLAYER', 'stats'])
    async def PlayerProfile(self, ctx, player: str, edit=False, messageObject=None):
        if edit is False:
            await ctx.channel.trigger_typing()
        hypixel.setCacheTime(cacheTime)
        try:
            startTime = time()

            if "<@" in player:
                mention = ctx.message.mentions[0]
                player = await database.findMinecraftUUID(str(mention.id))
                if player is False:
                    raise hypixel.PlayerNotFoundException

            if edit is False:
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
                playerTitle = playerTitle.replace('§Amc§Fprohosting§C', 'MCProHosting')
            except KeyError:
                playerTitle = playerRank['rank']

            playerColour = self.rankColours.get(playerTitle, self.rankColours[playerRank['rank']])
            self.playerInfo['playerColour'] = playerColour
            self.playerInfo['playerTitle'] = playerTitle
            self.playerInfo['displayName'] = self.playerInfo['displayName'].replace('_', '\_') # Fix https://github.com/Snuggle/hypixel-bot/issues/1

            embedObject = discord.Embed(color=playerColour, title=f"{playerTitle} {self.playerInfo['displayName']}", \
            description="\u200B", url=f"https://hypixel.net/player/{self.playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.

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
            forumsLink = self.playerInfo['socialMedia']['links']['HYPIXEL']
            karma = 0

            try: # Optional formatting
                timeAgo = ''
                beforeTime = datetime.datetime.fromtimestamp(int(lastLogin/1000))
                timeAgo = f"({ago.human(datetime.datetime.now() - beforeTime, precision=1)})"
                firstLogin = strftime("%Y-%m-%d", gmtime(int(self.playerInfo['firstLogin']) / 1000.0))
                lastLogin = strftime("%Y-%m-%d", gmtime(int(self.playerInfo['lastLogin']) / 1000.0))
                karma = self.playerInfo['karma']
                if karma >= 1000000:
                    karma = humanize.intword(karma)
                elif karma >= 1000:
                    karma = f"{int(karma/1000)} thousand"
                karma = str(karma)
            except:
                pass

            embedObject.add_field(name="Level", value=f"`{floor(self.playerInfo['networkLevel']*100)/100}`") # Floor the network level to 2dp.
            embedObject.add_field(name="Minecraft Version", value=f"`{self.playerInfo['mcVersionRp']}`")     # E.g: 368.86864043126684 -> 368.68
            embedObject.add_field(name="Guild", value=f"`{GuildID}`")
            embedObject.add_field(name="Karma", value=f"`{karma}`")
            embedObject.add_field(name="First / Last Login", value=f"`{firstLogin} / {lastLogin}\n{timeAgo}`")
            DiscordID = await database.getDiscordID(self.playerObject.UUID)
            embedObject.add_field(name="Discord", value=f"{DiscordID}")
            if forumsLink == "N/A":
                embedObject.add_field(name="Forums", value=f"`Unlinked`")
            else:
                embedObject.add_field(name="Forums", value=f"[View]({forumsLink}) forum account.")
            embedObject.set_image(url=f"https://visage.surgeplay.com/full/256/{self.playerInfo['displayName']}") # TODO: Random number for caching

            if playerTitle in rankMap:
                if playerTitle == "MVP+":
                    if 'rankPlusColor' in self.playerObject.JSON:
                        rankPlusColor = self.playerObject.JSON['rankPlusColor']
                    else:
                        rankPlusColor = 'RED'
                    print(rankPlusColor)
                    thumbnailURL = rankMap["MVP+"][rankPlusColor]
                else:
                    thumbnailURL = rankMap[playerTitle]
                    if thumbnailURL is None:
                        thumbnailURL = rankMap[playerRank]

            displayName = self.playerInfo['displayName'].replace('\\', '')
            if displayName == "Snuggle" or displayName == "Pixiest":
                thumbnailURL = rankMap[displayName]

            embedObject.set_thumbnail(url=thumbnailURL)
            embedObject.set_footer(text=f'{self.footerText} | {ctx.author}', icon_url=self.bot.user.avatar_url)
            if edit is True:
                print("Trying to edit")
                await messageObject.edit(content=None, embed=embedObject, delete_after=self.deleteTime)
            else:
                print("Trying to send")
                messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
                print(messageObject)
            playerInfo = self.playerInfo
            await database.populatePlayer(ctx, playerInfo)
            print(f" > Replied in {round(time()-startTime, 2)}s.")


            print(messageObject)
            await self.do_buttons(messageObject, ctx)
        except hypixel.PlayerNotFoundException:
            print(f" > Player not found.")
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)




def setup(bot):
    bot.add_cog(PlayerCard(bot))
