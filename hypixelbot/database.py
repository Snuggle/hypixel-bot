import sqlite3
import discord
from discord.ext import commands
async def findMinecraftUUID(discordID):
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT HypixelPlayers.DiscordID, HypixelPlayers.UUID FROM HypixelPlayers;""")
    results = cursor.fetchall()

    for player in results:
        if player[0] == discordID:
            print(" > found in database", end='')
            return player[1]
    print(" > not in database", end='')
    return False

    cursor.close()
    connection.close()

def getValue(UUID):
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT HypixelPlayers.UUID, HypixelPlayers.CommandsDone, HypixelPlayers.TimesViewed FROM HypixelPlayers;""")
    results = cursor.fetchall()

    for player in results:
        if player[0] == UUID:
            print(" > found in database", end='')
            return {"CommandsDone": int(player[1]), "TimesViewed": int(player[2])}
    print(" > not in database", end='')
    return {"CommandsDone": 0, "TimesViewed": 0}

    cursor.close()
    connection.close()

async def getDiscordID(UUID):
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    cursor.execute("""SELECT HypixelPlayers.UUID, HypixelPlayers.DiscordID FROM HypixelPlayers;""")
    results = cursor.fetchall()

    for player in results:
        if player[0] == UUID:
            print(" > found in database", end='')
            if player[1] is None:
                continue
            discordID = f"<@{player[1]}>"
            return discordID
    print(" > not in database", end='')
    return '`Unlinked`'

    cursor.close()
    connection.close()

async def forceLink(playerInfo, discordID, discordCode):
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    values_to_update = [playerInfo['displayName'], 1, discordID, discordCode, playerInfo['uuid']]
    cursor.executemany("""
                        UPDATE HypixelPlayers
                        SET Username=?, VerifyMode=?, DiscordID=?, DiscordUsername=?
                        WHERE UUID=?""", (values_to_update,))
    print(" > injected into database", end='')

    connection.commit()
    cursor.close()
    connection.close()

async def populatePlayer(ctx, playerInfo):
    discordName = playerInfo['socialMedia']['links']['DISCORD']
    if discordName == "N/A":
        discordName = None
    try:
        discordID = discord.utils.get(ctx.channel.members, name=discordName.split('#')[0], discriminator=discordName.split('#')[1]).id
    except:
        discordID = None
    print(discordID)
    timesViewed = getValue(playerInfo['uuid'])['TimesViewed']
    print(timesViewed)
    timesViewed += 1
    print(timesViewed)
    values_to_insert = [playerInfo['uuid'], playerInfo['displayName'], 0, discordID, discordName, 0, 0]
    values_to_update = [playerInfo['displayName'], 0, discordID, discordName, timesViewed, playerInfo['uuid']]
    values_to_update_noID = [playerInfo['displayName'], discordName,  timesViewed, playerInfo['uuid']]
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    try:
        cursor.executemany("""
                            INSERT INTO HypixelPlayers (UUID, Username, VerifyMode, DiscordID, DiscordUsername, CommandsDone, TimesViewed)
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (values_to_insert,))
        print(" > inserted to database", end='')
    except sqlite3.IntegrityError:
        print(discordID)
        if discordID is None:
            cursor.executemany("""
                                UPDATE HypixelPlayers
                                SET Username=?, DiscordUsername=?, TimesViewed=?
                                WHERE UUID=?""", (values_to_update_noID,))
            print(" > updated database", end='')
        else:
            cursor.executemany("""
                                UPDATE HypixelPlayers
                                SET Username=?, VerifyMode=?, DiscordID=?, DiscordUsername=?, TimesViewed=?
                                WHERE UUID=?""", (values_to_update,))
            print(" > updated database", end='')
    connection.commit()
    cursor.close()
    connection.close()
