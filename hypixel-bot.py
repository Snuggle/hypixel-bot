#!/usr/bin/env python3
__description__ = """ Unofficial Hypixel Discord Bot, Made by Snuggle. """
__version__ = '0.0.1'

import discord
from discord.ext import commands
import traceback
import sys
import hypixel

keys = open("keys.ini", "r").readlines() # Get keys and set them all
hypixelKeys = [keys[0].replace('\n', '')]
hypixel.setKeys(hypixelKeys)
bot_token = keys[1]

prefix = ['hypixel-', 'Hypixel-']

startup_extensions = ('cogs.player',
                      'cogs.owner',
                      'cogs.utility')

bot = commands.Bot(command_prefix=prefix, description=__description__)

@bot.event
async def on_ready():
    print("Starting up...")
    await bot.change_presence(game=discord.Game(name='do hypixel-help!', type=1, url='https://twitch.tv/snugglysnuggle'))
    print(f"{bot.user.name} is now online! Version: {__version__}")
    

    if __name__ == '__main__':
        bot.remove_command('help')
        for extension in startup_extensions:
            try:
                bot.load_extension(extension)
            except Exception as e:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()
    print(f'Successfully logged in and booted...!')


    
bot.run(bot_token, bot=True, reconnect=True)
