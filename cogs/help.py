__version__ = '2018-02-06'
from discord.ext import commands
import discord
import os
from hypixelbot import utility

class HelpCog:
    deleteTime = 60.0

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def cog_help(self, ctx):
        description = ('Hey, there! This is a small unofficial Hypixel Discord bot made by Snuggle, a moderator for the server. `hypixel-player Snuggle`\n\nYou might see the occasional bug or broken features. '
                        'If you experience any issues, please message me on [Twitter](https://twitter.com/SprinkIy).\n\n'
                        'To use this bot on your own Discord server, please visit https://sprinkly.net/hypixelbot.\n\n'
                        f'I am currently a member of `{len(self.bot.guilds)}` servers in total and I was last updated on `{__version__}`.') #I have also recieved `{}` commands since 2017-06-30.')

        embedObject = discord.Embed(color=0xCDA040, title='Snuggle\'s Unofficial Hypixel Bot', description=description, url="https://sprinkly.net/hypixelbot")
        embedObject.set_image(url="https://i.imgur.com/xe5AjV0.png")
        try:
            await ctx.author.send(content=None, embed=embedObject)
        except:
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)

        embedObject = discord.Embed(color=0xCDA040, description='**Current Commands List**', url="https://sprinkly.net/hypixelbot")
        embedObject.add_field(name="hypixel-help", value="Shows usage information.")
        embedObject.add_field(name="hypixel-invite", value="Invite me to your own server!")
        embedObject.add_field(name="hypixel-player `username`", value="Show information about a player.") #You can also @username#1234 them.")
        embedObject.add_field(name="hypixel-guild `username`", value="Show detailed information about a player's guild.") #You can also @username#1234 them.")
        #embedObject.add_field(name="hypixel-settings", value="Change the bot's settings. You can set your own bio and toggle message self-destruct here.")

        changeEmbedObject = discord.Embed(color=0xCDA040, description='**Changelog**\nAn archive of changes made is available here: https://pastebin.com/TxaNuAWA', url="https://sprinkly.net/hypixelbot")
        changeEmbedObject.add_field(name="Coming soon...", value="‣ Minecraft account linking (again)\n‣ Clean up code & open-source on my GitHub.\n‣ More gamemodes added!\n‣ Bug fixes! 🐛")
        changeEmbedObject.add_field(name=f"Most recent update ({__version__})", value="• Fixed bug that stopped several users from viewing their own profile.\n• Added `hypixel-invite` command to make it easier for people to add me!\n• Created a snazzy banner.\n• Gave `hypixel-help` a new look. I hope you like it! c:\n• Fixed image art for game statistics. Before it was only showing Murder Mystery's art. Woopsies! 😞")
        changeEmbedObject.set_footer(text=utility.footerText, icon_url=self.bot.user.avatar_url)
        try:
            secondEmbedObject = discord.Embed(color=0xCDA040, description=f"<@!{ctx.author.id}>, please check your direct messages!", url="https://sprinkly.net/hypixelbot")
            await ctx.author.send(content=None, embed=embedObject)
            await ctx.author.send(content=None, embed=changeEmbedObject)
            await ctx.send(content=None, embed=secondEmbedObject, delete_after=self.deleteTime/4)
            print(f" > Sent help to user via DM.")
        except:
            await ctx.send(content=None, embed=embedObject, delete_after=self.deleteTime)
            print(f" > Sent help to server.")

    @commands.command(name='invite')
    async def cog_invite(self, ctx):
        embedObject = discord.Embed(color=0xCDA040, title="How do I get a cool bot on my server?!", description=f"To invite me to your server, please visit: https://sprinkly.net/hypixelbot")
        embedObject.set_footer(text="Hypixel Bot | Hope to see you there soon!", icon_url=self.bot.user.avatar_url)
        await ctx.author.send(content=None, embed=embedObject)

def setup(bot):
    bot.add_cog(HelpCog(bot))
