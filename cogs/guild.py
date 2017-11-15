import discord
from discord.ext import commands
import hypixel
from re import sub, findall
import grequests
from bs4 import BeautifulSoup
from time import strftime, gmtime, time
import traceback
cacheTime = 864000

guildCache = {}

async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

class GuildCog:
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    async def crawlGuildPage(self, guildPageURL):
        urls = [guildPageURL]
        guildBanner = "None"
        if guildPageURL in guildCache and guildCache[guildPageURL]['cacheTime'] > time():
            guildDescription = guildCache[guildPageURL]['description']
            guildBanner = guildCache[guildPageURL]['banner']
        else:
            requests = (grequests.get(u) for u in urls)
            responses = grequests.imap(requests)
            for r in responses:
                response = r.text

            soup = BeautifulSoup(response, "html.parser")
            soup = soup.find_all('blockquote', { "class" : "messageText baseHtml"})
            guildDescription = sub(r'<(.*?)>', '', str(soup)).replace('[', '').replace(']', '').replace('\n\n\n', '')
            guildDescription = sub(r'(.*)Guild Stats(.*)(\n*)([\s\S]*)', '', guildDescription).replace('&lt;', '<').replace('&gt;', '>') # Clean/remove Stats Boxes and add any angled brackets.
            guildDescription = f"\n**Description:** {guildDescription}"
            print(guildDescription)
            for link in findall(r"data/guild_headers/(.*?)'", response):
                guildBanner = f"https://hypixel.net/data/guild_headers/{link}"
                print(guildBanner)

            guildCache[guildPageURL] = {} # TODO: Cache by guild ID instead of URL. Many members in a guild and all of them have seperate atm.
            guildCache[guildPageURL]['banner'] = guildBanner
            guildCache[guildPageURL]['description'] = guildDescription
            guildCache[guildPageURL]['cacheTime'] = time() + cacheTime
            
        return({'guildBanner': guildBanner, 'guildDescription': guildDescription})

    @commands.command(name='guild', aliases=['Guild', 'GUILD'])
    async def cog_guild(self, ctx, player: str):
        await ctx.channel.trigger_typing()
        hypixel.setCacheTime(cacheTime)
        try:
            startTime = time()

            playerObject = hypixel.Player(player)
            playerInfo = playerObject.getPlayerInfo()

            guildID = playerObject.getGuildID()
            if guildID is None:
                print(f" > Guild not found.")
                embedObject = discord.Embed(color=0x800000, description=f"{playerInfo['displayName']} is not in a guild!", url="https://sprinkly.net/hypixelbot")
                embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
                await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
                await soft_delete(ctx)
                return False

            guildObject = hypixel.Guild(guildID)
            guildName = guildObject.JSON['name']

            startMeasure = time()
            if guildID in guildCache:
                guildMembers = guildCache[guildID]
            else:
                guildMembers = guildObject.getMembers() # TODO: Add caching time
                guildCache[guildID] = guildMembers
            stopMeasure = time()
            print("---Measure---")
            print(stopMeasure-startMeasure)

            guildDescription = "None"
            guildPageURL = f"https://hypixel.net/guilds/{guildID}"
            #guildMembers = {'MEMBER': ['Rackals', 'Andyq9433', 'Tezech', 'proweaboo', 'Chrli', 'Yharon', 'MoistySalt', 'lord_dark166', 'BarryK', 'AUNIQUE', 'Liqo', 'xZoomPvp', 'xForced', 'frgjo', 'agentfitz', 'ChillDylanC', 'ValseHoop', 'ISmellLikeBacon', 'iMeap', 'KamerPlant', 'Niicolo', 'TheLapisBlock', '_Childish_', 'OldManCrinkles', 'PedrosTacos', 'QSweet', 'lellort', 'TindinPlayz', 'dcp9', 'xBloodyPanda', 'ZetieTheTeddy', 'hqn', 'Aixe', 'ohDroze', 'Legoblaze_', 'Precisionings', 'Bjorb', 'AwesomeArv', 'Cuty', '512CPS', 'Alegbra', 'Veik', 'WolfKatt', 'Cosru', 'Decrupt', 'Erjan', 'HeLLing', 'skyerzz', 'Sayonara', 'Dont_Ban_Me', 'AFoodEater', 'Zyperiox', 'Tediosito', 'JVSgamer', 'Deesal', 'LonelyRev', 'Birds_wings', '9x8', 'PacifyClove', 'InfectedAlpha', 'Sophie_OGrady', 'DiamondKiwi', 'iDezi', 'DuhGeo', 'Jild', 'oSkywars', 'JaceHerondale', 'Tringo', 'CalOtter', 'PriscillaPS', 'Pixiest', 'Snuggle'], 'OFFICER': ['JakeDaaBud', 'Flafkas', 'Thomas8454', 'MikePlaysMc_', 'Jellycat', 'TheNeonPikachu', 'ToadBunny', 'iPolarr', 'Bembo', 'Dimply'], 'GUILDMASTER': ['Ellxa']}

            crawledData = await self.crawlGuildPage(guildPageURL)
            guildBanner = crawledData['guildBanner']
            guildDescription = crawledData['guildDescription']

            for typeOfMember in guildMembers:
                guildMembers[typeOfMember] = str(guildMembers[typeOfMember]).replace('\'', '').replace('[', '').replace(']', '')
                # Convert each list in guildMembers to a string.

            embedObject = discord.Embed(color=0xCDA040, title=guildName, description=f"\u200B{guildDescription}", url=guildPageURL)
            embedObject.add_field(name="Guild Master", value=f"`\u200B{guildMembers['GUILDMASTER'][:2045]}`", inline=False)
            embedObject.add_field(name="Officers", value=f"`\u200B{guildMembers['OFFICER'][:2045]}`", inline=False)
            embedObject.add_field(name="Members", value=f"`\u200B{guildMembers['MEMBER'][:1021]}`", inline=False)
            if len(guildMembers['MEMBER']) > 1021: # If too many characters to fit in a Discord.field, split into two fields
                embedObject.add_field(name="Members (Cont.)", value=f"`{guildMembers['MEMBER'][1021:]}`", inline=False)
                
            if guildBanner.startswith('https://hypixel.net/data/guild_headers/'):
                embedObject.set_image(url=guildBanner)
                
            embedObject.set_footer(text=f'{self.footerText} | {ctx.author}', icon_url=self.bot.user.avatar_url)
            messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            print(f" > Replied in {round(time()-startTime, 2)}s.")
            await soft_delete(ctx)
        except hypixel.PlayerNotFoundException:
            print(f" > Player not found.")
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await soft_delete(ctx)

def setup(bot):
    bot.add_cog(GuildCog(bot))
