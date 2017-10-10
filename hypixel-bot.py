#!/usr/bin/env python3
__description__ = """ Unofficial Hypixel Discord Bot, Made by Snuggle. """
__version__ = '0.0.1'

import discord
from discord.ext import commands

def prefix(bot, message):    
    mainPrefix = 'hypixel-'

    return commands.when_mentioned_or(prefix)(bot, message)

startup_extensions = None

bot = commands.Bot(command_prefix=prefix, description=__description__)

@bot.event
async def on_ready():
    print("Starting up...")
    await bot.change_presence(game=discord.Game(name='Cogs Example', type=1, url='twitch.tv/snugglysnuggle'))
    print("{bot.user.name} is now online! Version: {__version__}")