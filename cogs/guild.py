import discord
from discord.ext import commands
import hypixel
import grequests
from time import strftime, gmtime, time
import traceback
cacheTime = 864000

class GuildCog:
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='guild', aliases=['Guild', 'GUILD'])
    async def cog_guild(self, ctx, player: str):
        await ctx.channel.trigger_typing()
        hypixel.setCacheTime(cacheTime)
        try:
            startTime = time()

            playerObject = hypixel.Player(player)
            playerInfo = playerObject.getPlayerInfo()

            guildID = playerObject.getGuildID()

            guildObject = hypixel.Guild(guildID)
            guildName = guildObject.JSON['name']

            #guildMembers = guildObject.getMembers()
            #print(guildMembers)

            #TODO: Get header/description from guild page

            guildInfo = "None"
            guildMembers = {'MEMBER': ['Rackals', 'Andyq9433', 'Tezech', 'proweaboo', 'Chrli', 'Yharon', 'MoistySalt', 'lord_dark166', 'BarryK', 'AUNIQUE', 'Liqo', 'xZoomPvp', 'xForced', 'frgjo', 'agentfitz', 'ChillDylanC', 'ValseHoop', 'ISmellLikeBacon', 'iMeap', 'KamerPlant', 'Niicolo', 'TheLapisBlock', '_Childish_', 'OldManCrinkles', 'PedrosTacos', 'QSweet', 'lellort', 'TindinPlayz', 'dcp9', 'xBloodyPanda', 'ZetieTheTeddy', 'hqn', 'Aixe', 'ohDroze', 'Legoblaze_', 'Precisionings', 'Bjorb', 'AwesomeArv', 'Cuty', '512CPS', 'Alegbra', 'Veik', 'WolfKatt', 'Cosru', 'Decrupt', 'Erjan', 'HeLLing', 'skyerzz', 'Sayonara', 'Dont_Ban_Me', 'AFoodEater', 'Zyperiox', 'Tediosito', 'JVSgamer', 'Deesal', 'LonelyRev', 'Birds_wings', '9x8', 'PacifyClove', 'InfectedAlpha', 'Sophie_OGrady', 'DiamondKiwi', 'iDezi', 'DuhGeo', 'Jild', 'oSkywars', 'JaceHerondale', 'Tringo', 'CalOtter', 'PriscillaPS', 'Pixiest', 'Snuggle'], 'OFFICER': ['JakeDaaBud', 'Flafkas', 'Thomas8454', 'MikePlaysMc_', 'Jellycat', 'TheNeonPikachu', 'ToadBunny', 'iPolarr', 'Bembo', 'Dimply'], 'GUILDMASTER': ['Ellxa']}

            embedObject = discord.Embed(color=0xCDA040, title=f"{guildName}", description="​{}".format(guildInfo), url=f"https://hypixel.net/guilds/{guildID}")
            embedObject.add_field(name="Guild Master", value='`{}`'.format(guildMembers['GUILDMASTER']), inline=False)
            embedObject.add_field(name="Officers", value='`{}`'.format(guildMembers['OFFICER']), inline=False)
            embedObject.add_field(name="Members", value='`{}`'.format(guildMembers['MEMBER']), inline=False) # TODO: Length checking
            messageObject = await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            print(f"{ctx.message.content} took {time()-startTime} seconds to reply.")
            await ctx.message.delete()
        except hypixel.PlayerNotFoundException:
            embedObject = discord.Embed(color=0x800000, description='Player not found.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await ctx.message.delete()
        except Exception as e:
            embedObject = discord.Embed(color=0x800000, description='An unknown error has occured.\nAn error report has been sent to my creator.', url="https://sprinkly.net/hypixelbot")
            embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            await ctx.message.delete()
            Snuggle = discord.User(id="201635058405212160")
            Snuggle.send("{ctx.message.content}")
            traceback.print_exc()
            print("Command: {ctx.message.content}")

def setup(bot):
    bot.add_cog(GuildCog(bot))
