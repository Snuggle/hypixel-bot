async def soft_delete(ctx):
    try:
        await ctx.message.delete()
    except:
        pass

def getBedwarsLevel(bedwarsExp):
    # Utility function stolen from https://github.com/Plancke/hypixel-php/blob/master/src/util/GameUtils.php

    # first few levels are different
    if bedwarsExp < 1500:
        return 1
    elif bedwarsExp < 3500:
        return 2
    elif bedwarsExp < 5500:
        return 3
    elif bedwarsExp < 9000:
        return 4

    bedwarsExp -= 9000;
    return (bedwarsExp / 5000) + 4
