async def get_logs(db):
    ret = []
    async with db.execute("SELECT logs.Id, Name, Auction_id, Desc, Severity, datetime(logs.Timestamp, 'localtime') FROM logs LEFT JOIN players ON players.Id = logs.Player_id") as cursor:
        async for row in cursor:
            print(row)
            ret.append(
                {
                    "id": row[0],
                    "log_time": row[5],
                    "player_name": row[1],
                    "auction_id": row[2],
                    "description": row[3],
                    "log_severity": row[4]
                }
            )
    return ret


async def log(db, log_obj):
    async with db.execute(
        "INSERT INTO logs (Player_id, Auction_id, Desc, Severity) VALUES(?, ?, ?, ?)",
        [log_obj["player_id"], log_obj["auction_id"],
            log_obj["Desc"], log_obj["Severity"]],
    ) as cursor:
        log_id = cursor.lastrowid
    await db.commit()
    return log_id


async def insert_player(db, name, port):
    async with db.execute(
        "INSERT INTO players (Name, Port) VALUES(?, ?)",
        [name, port],
    ) as cursor:
        player_id = cursor.lastrowid
    await db.commit()
    await log(db, {
        "player_id": player_id,
        "auction_id": -1,
        "Desc": "Player registered successfully at port {}".format(port),
        "Severity": "Notify"
    })
    return player_id


async def insert_auction(db, players):
    async with db.execute(
        "INSERT INTO auctions DEFAULT VALUES"
    ) as cursor:
        auction_id = cursor.lastrowid
    await db.commit()
    auction_players = [(auction_id, x) for x in players]
    await db.executemany("INSERT INTO auction_players(Auction_id, Player_id) VALUES (?, ?)",
                         auction_players)
    await db.commit()
    await log(db, {
        "player_id": -1,
        "auction_id": auction_id,
        "Desc": "Auction started",
        "Severity": "Notify"
    })
    return auction_id


async def get_ports(db, auction_id)
