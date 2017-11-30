import sqlite3
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

async def populatePlayer(ctx, playerInfo):
    discordName = playerInfo['socialMedia']['links']['DISCORD']
    if discordName == "N/A":
        discordName = None
    try:
        discordID = discord.utils.get(ctx.channel.members, name=discordName.split('#')[0], discriminator=discordName.split('#')[1]).id
    except:
        discordID = None
    values_to_insert = [playerInfo['uuid'], playerInfo['displayName'], discordID, discordName, 0]
    values_to_update = [playerInfo['displayName'], discordID, discordName, playerInfo['uuid']]
    values_to_update_noID = [playerInfo['displayName'], discordName, playerInfo['uuid']]
    connection = sqlite3.connect("hypixel.db")
    cursor = connection.cursor()
    try:
        cursor.executemany("""
                            INSERT INTO HypixelPlayers (UUID, Username, DiscordID, DiscordUsername, CommandsDone)
                            VALUES (?, ?, ?, ?, ?)""", (values_to_insert,))
        print(" > inserted to database", end='')
    except sqlite3.IntegrityError:
        if discordID is None:
            cursor.executemany("""
                                UPDATE HypixelPlayers
                                SET Username=?, DiscordUsername=?
                                WHERE UUID=?""", (values_to_update_noID,))
            print(" > updated database", end='')
        else:
            cursor.executemany("""
                                UPDATE HypixelPlayers
                                SET Username=?, DiscordID=?, DiscordUsername=?
                                WHERE UUID=?""", (values_to_update,))
            print(" > updated database", end='')
    connection.commit()
    cursor.close()
    connection.close()
