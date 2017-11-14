from discord.ext import commands
import discord

async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

class UtilityCog:
    deleteTime = 60.0
    footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name='help')
    async def cog_help(self, ctx):
        description = ('Hey, there! This is a small unofficial Hypixel Discord bot made by Snuggle.\n\nIt can be pretty buggy at times. ' 
                        'If you experience any, please message me on [Twitter](https://twitter.com/SprinkIy).\n' 
                        'To use this bot on your own Discord server, [click here](https://sprinkly.net/hypixelbot).\n\n')
                        #'I am currently a member of `{}` servers which in total have `{}` members. I have also recieved `{}` commands since 2017-06-30.')

        embedObject = discord.Embed(color=0xCDA040, title='Snuggle\'s Unofficial Hypixel Bot', description=description, url="https://sprinkly.net/hypixelbot")
        embedObject.set_image(url="http://i.imgur.com/OdU9KJM.png")
        try:
            await ctx.author.send(content=None, embed=embedObject)
        except:
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
        
        embedObject = discord.Embed(color=0xCDA040, description='**Current commands list:**', url="https://sprinkly.net/hypixelbot")
        embedObject.add_field(name="hypixel-help", value="Shows usage information.")
        embedObject.add_field(name="hypixel-player `username`", value="Show information about a player.") #You can also @username#1234 them.")
        embedObject.add_field(name="hypixel-guild `username`", value="Show detailed information about a player's guild.") #You can also @username#1234 them.")
        #embedObject.add_field(name="hypixel-settings", value="Change the bot's settings. You can set your own bio and toggle message self-destruct here.")
        embedObject.set_footer(text=self.footerText, icon_url=self.bot.user.avatar_url)
        embedObject.set_thumbnail(url="http://i.imgur.com/te3hSIG.png")
        try:
            await ctx.author.send(content=None, embed=embedObject)
            print(f" > Sent help to user via DM.")
        except:
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            print(f" > Sent help to server.")

def setup(bot):
    bot.add_cog(UtilityCog(bot))