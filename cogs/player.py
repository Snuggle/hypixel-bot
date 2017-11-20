import discord
from discord.ext import commands
import hypixel
from time import strftime, gmtime, time
from math import floor
import asyncio
import traceback
import sqlite3
cacheTime = 172800

async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

class PlayerCog:
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    rankColours = {'MVP': 0x55FFFF, 'VIP': 0x55FF55, 'MVP+': 0x55FFFF, 'VIP+': 0x55FF55, 'Non': 0xAAAAAA, 'Helper': 0x5555FF, 'Moderator': 0x00AA00, 'Admin': 0xFF5555, 'Youtuber': 0xFFAA00, 'Build Team': 0x00AAAA, 'Owner': 0xFF5555, 'None': 0xAAAAAA, 'Mixer': 0x00AAAA}
    dataItems = ['karma', 'firstLogin', 'lastLogin', 'mcVersionRp', 'networkExp', 'displayName', 'rank', 'networkLevel', 'socialMedia']
    socialLinks = ['YOUTUBE', 'TWITTER', 'HYPIXEL', 'DISCORD', 'MIXER']
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    async def findMinecraftUUID(self, discordID):
        connection = sqlite3.connect("hypixel.db")
        cursor = connection.cursor()
        cursor.execute("""SELECT HypixelPlayers.DiscordID, HypixelPlayers.UUID FROM HypixelPlayers;""")
        results = cursor.fetchall()

        for player in results:
            if player[0] == discordID:
                print(" > found in database", end='')
                return player[1]
        print(" > not in database", end='')
        return False

        cursor.close()
        connection.close()

    async def populatePlayer(self, ctx, playerInfo):
        discordName = playerInfo['socialMedia']['links']['DISCORD']
        if discordName == "N/A":
            discordName = None
        try:
            discordID = discord.utils.get(ctx.channel.members, name=discordName.split('#')[0], discriminator=discordName.split('#')[1]).id
        except:
            discordID = None
        values_to_insert = [playerInfo['uuid'], playerInfo['displayName'], discordID, discordName, 0]
        values_to_update = [playerInfo['displayName'], discordID, discordName, playerInfo['uuid']]
        values_to_update_noID = [playerInfo['displayName'], discordName, playerInfo['uuid']]
        connection = sqlite3.connect("hypixel.db")
        cursor = connection.cursor()
        try:
            cursor.executemany("""
                                INSERT INTO HypixelPlayers (UUID, Username, DiscordID, DiscordUsername, CommandsDone)
                                VALUES (?, ?, ?, ?, ?)""", (values_to_insert,))
            print(" > inserted to database", end='')
        except sqlite3.IntegrityError:
            if discordID is None:
                cursor.executemany("""
                                    UPDATE HypixelPlayers
                                    SET Username=?, DiscordUsername=?
                                    WHERE UUID=?""", (values_to_update_noID,))
                print(" > updated database", end='')
            else:
                cursor.executemany("""
                                    UPDATE HypixelPlayers
                                    SET Username=?, DiscordID=?, DiscordUsername=?
                                    WHERE UUID=?""", (values_to_update,))
                print(" > updated database", end='')
        connection.commit()
        cursor.close()
        connection.close()


    @commands.command(name='player', aliases=['Player', 'PLAYER'])
    async def cog_player(self, ctx, player: str):
        await ctx.channel.trigger_typing()
        hypixel.setCacheTime(cacheTime)
        try:
            startTime = time()

            if "<@" in player:
                mention = ctx.message.mentions[0]
                player = await self.findMinecraftUUID(str(mention.id))
                if player is False:
                    raise hypixel.PlayerNotFoundException

            playerObject = hypixel.Player(player)
            playerInfo = playerObject.getPlayerInfo()

            for data in self.dataItems:
                if data == "socialMedia":
                    if 'socialMedia' not in playerInfo:
                        playerInfo['socialMedia'] = {}
                    if 'links' not in playerInfo['socialMedia']:
                        playerInfo['socialMedia']['links'] = {}
                    for link in self.socialLinks:
                        if link not in playerInfo['socialMedia']['links']:
                            playerInfo['socialMedia']['links'][link] = 'N/A'

                if data not in playerInfo:
                    playerInfo[data] = 'N/A'

            playerRank = playerInfo['rank']
            try:
                playerTitle = playerInfo['prefix'].title().split('[')[1]
                playerTitle = playerTitle.replace(']', '')
            except KeyError:
                playerTitle = playerRank['rank']
            
            playerColour = self.rankColours.get(playerTitle, self.rankColours[playerRank['rank']])

            embedObject = discord.Embed(color=playerColour, title=f"{playerTitle} {playerInfo['displayName']}", \
            description="\u200B", url=f"https://hypixel.net/player/{playerInfo['displayName']}") # \u200B is a zero-width space, to add padding.

            try:
                forumsLink = playerInfo['socialMedia']['links']['HYPIXEL']
            except KeyError:
                forumsLink = "Unlinked"
            try:
                discordName = playerInfo['socialMedia']['links']['DISCORD']
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

            GuildID = playerObject.getGuildID()
            if GuildID is not None:
                tempGuild = hypixel.Guild(GuildID)
                GuildID = tempGuild.JSON['name']

            firstLogin = playerInfo['firstLogin']
            lastLogin = playerInfo['lastLogin']

            try: # Optional formatting
                firstLogin = strftime("%Y-%m-%d", gmtime(int(playerInfo['firstLogin']) / 1000.0))
                lastLogin = strftime("%Y-%m-%d", gmtime(int(playerInfo['lastLogin']) / 1000.0))
                playerInfo['karma'] = f"{int(playerInfo['karma']):,}"
            except:
                pass

            embedObject.add_field(name="Level", value=f"`{floor(playerInfo['networkLevel']*100)/100}`") # Floor the network level to 2dp.
            embedObject.add_field(name="Minecraft Version", value=f"`{playerInfo['mcVersionRp']}`")     # E.g: 368.86864043126684 -> 368.68
            embedObject.add_field(name="Guild", value=f"`{GuildID}`")
            embedObject.add_field(name="Karma", value=f"`{playerInfo['karma']}`")
            embedObject.add_field(name="First / Last Login", value=f"`{firstLogin} / {lastLogin}`")
            embedObject.add_field(name="Discord", value=f"{discordName}")
            if forumsLink == "Unlinked":
                embedObject.add_field(name="Forums", value=f"`Unlinked`")
            else:
                embedObject.add_field(name="Forums", value=f"[View]({forumsLink}) forum account.")
            embedObject.set_image(url=f"https://visage.surgeplay.com/full/256/{playerInfo['displayName']}")
            embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
            embedObject.set_footer(text=f'{self.footerText} | {ctx.author}', icon_url=self.bot.user.avatar_url)
            messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await self.populatePlayer(ctx, playerInfo)
            print(f" > Replied in {round(time()-startTime, 2)}s.")
            await soft_delete(ctx)
        except hypixel.PlayerNotFoundException:
            print(f" > Player not found.")
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await soft_delete(ctx)



def setup(bot):
    bot.add_cog(PlayerCog(bot))
