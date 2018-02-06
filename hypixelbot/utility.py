import datetime
import humanize

def getRunningTime():
    return (humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(1489449600)))

footerText = f'Hypixel Bot | Made with \u2764 by Snuggle, {getRunningTime()}'

async def soft_delete(ctx):
    try:
        if 'command' not in ctx.channel.name:
            await ctx.message.delete()
    except:
        pass

async def soft_clear(messageObject):
    try:
        await messageObject.clear_reactions()
    except:
        pass

def getBedwarsLevel(bedwarsExp):
    # Utility function stolen from https://github.com/Plancke/hypixel-php/blob/master/src/util/GameUtils.php
    BEDWARS_EXP_PER_PRESTIGE = 489000
    BEDWARS_LEVELS_PER_PRESTIGE = 100

    prestige = int(bedwarsExp/BEDWARS_EXP_PER_PRESTIGE)
    bedwarsExp = bedwarsExp % BEDWARS_EXP_PER_PRESTIGE

    if prestige > 5:
        over = prestige % 5
        bedwarsExp += over * BEDWARS_EXP_PER_PRESTIGE
        prestige -= over

    # first few levels are different
    if bedwarsExp < 500:
        return 0 + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)
    elif bedwarsExp < 1500:
        return 1 + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)
    elif bedwarsExp < 3500:
        return 2 + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)
    elif bedwarsExp < 5500:
        return 3 + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)
    elif bedwarsExp < 9000:
        return 4 + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)

    bedwarsExp -= 9000;
    return (bedwarsExp / 5000 + 4) + (prestige * BEDWARS_LEVELS_PER_PRESTIGE)
