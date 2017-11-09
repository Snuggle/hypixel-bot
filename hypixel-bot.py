#!/usr/bin/env python3
__description__ = """ Unofficial Hypixel Discord Bot, Made by Snuggle. """
__version__ = '0.0.1'

import discord
from discord.ext import commands
import traceback
import sys
import hypixel # Import all the things necessary

keys = open("keys.ini", "r").readlines() # Get keys and set them all from file.
hypixelKeys = [keys[0].replace('\n', '')]
hypixel.setKeys(hypixelKeys) # Set Hypixel-API key.
bot_token = keys[1]

prefix = ['hypixel-', 'Hypixel-']

startup_extensions = ('cogs.player', # These are the extensions that will be loaded.
                      'cogs.owner',
                      'cogs.utility',
                      'cogs.guild')

bot = commands.Bot(command_prefix=prefix, description=__description__) # Create Discord bot.

@bot.event
async def on_ready(): # When the bot is ready, do the following...
    print("Bot ready! Setting game status.")
    await bot.change_presence(game=discord.Game(name='do hypixel-help!', type=1, url='https://twitch.tv/snugglysnuggle')) #Change bot's status to "Streaming"
    print(f"{bot.user.name} v{__version__} is loading extensions!") # Print to console that the bot is online.
    

    if __name__ == '__main__': # Load all the extensions.
        bot.remove_command('help')
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
    print(f'Successfully loaded extensions!')


print("Starting bot...")
bot.run(bot_token, bot=True, reconnect=True) # Run the bot.
