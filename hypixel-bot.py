#!/usr/bin/env python3
__description__ = """ Unofficial Hypixel Discord Bot, Made by Snuggle. """
__version__ = '0.0.1'

import discord
from discord.ext import commands
import traceback
import sys
import time
import hypixel # Import all the things necessary

keys = open("keys.ini", "r").readlines() # Get keys and set them all from file.
hypixelKeys = [keys[0].replace('\n', '')]
hypixel.setKeys(hypixelKeys) # Set Hypixel-API key.
bot_token = keys[1]

prefix = ['hypixel-', 'Hypixel-']
footerText = 'Hypixel Bot | Made with \u2764 by Snuggle' # \u2764 is a heart symbol.

startup_extensions = ('cogs.player', # These are the extensions that will be loaded.
                      'cogs.owner',
                      'cogs.utility',
                      'cogs.guild')

bot = commands.Bot(command_prefix=prefix, description=__description__) # Create Discord bot.

@bot.event
async def on_command_error(ctx, error):
    embedObject = discord.Embed(color=0x800000, description='An unknown error has occured.\nAn error report has been sent to my creator.', url="https://sprinkly.net/hypixelbot")
    embedObject.set_footer(text=footerText, icon_url=bot.user.avatar_url)
    await ctx.send(content=None, embed=embedObject, delete_after=30.0)

    Snuggle = bot.get_user(201635058405212160)
    errorString = traceback.format_exception(type(error), error, error.__traceback__)
    errorString = '\n'.join(errorString)
    errorString = errorString.split('The above exception was the direct cause of the following exception')[0]
    embedObject = discord.Embed(color=0xFF5555, title=f"{bot.user.name} Error Report", description=f"```{errorString[:2000]}```")
    embedObject.add_field(name="Message Content", value=f"`\u200B{ctx.message.content}`")
    embedObject.add_field(name="Author", value=f"`\u200B{ctx.author}` | <@{ctx.author.id}>")
    if ctx.guild is not None:
        embedObject.add_field(name="Where", value=f"`\u200B{ctx.guild} > #{ctx.channel}`")
        embedObject.add_field(name="Guild ID", value=f"`\u200B{ctx.guild.id}`")
    else:
        embedObject.add_field(name="Where", value=f"`\u200B{ctx.channel}`")
    timeString = time.strftime("%d %b %Y @ %I:%M:%S%p", time.gmtime())
    embedObject.set_footer(text=f"\u200B{footerText} | {timeString}", icon_url=bot.user.avatar_url)
    print(Snuggle)
    await Snuggle.send(content=None, embed=embedObject)

@bot.event
async def on_ready(): # When the bot is ready, do the following...
    print(f"Hello, there! I am {bot.user.name} v{__version__}.")
    await bot.change_presence(game=discord.Game(name='do hypixel-help!', type=1, url='https://twitch.tv/snugglysnuggle')) #Change bot's status to "Streaming"
    print(f"Please wait while I load my extensions: ", end='') # Print to console that the bot is online.

    if __name__ == '__main__': # Load all the extensions.
        bot.remove_command('help')
        print('[', end='')
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
                print('#', end='')
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
    else:
        print("You cannot import me, silly.")
        exit()
    print(']')
    print(f"Using hypixel.py v{hypixel.__version__}.")
    print('Successfully started up and listening for commands...\n')


print("Beep, boop!")
bot.run(bot_token, bot=True, reconnect=True) # Run the bot.
