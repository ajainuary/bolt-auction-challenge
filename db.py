import random
import asyncio

db_write = asyncio.Lock()


async def get_logs(db):
    async with db.execute("SELECT logs.Id, Name, Auction_id, Desc, Severity, datetime(logs.Timestamp, 'localtime') FROM logs LEFT JOIN players ON players.Id = logs.Player_id") as cursor:
        return list(map(lambda row: {
            "id": row[0],
            "log_time": row[5],
            "player_name": row[1],
            "auction_id": row[2],
            "description": row[3],
            "log_severity": row[4]
        }, await cursor.fetchall()))


async def get_leaderboard(db):
    async with db.execute("SELECT Name, SUM(value) FROM transactions, players WHERE players.Id = transactions.Player_id GROUP BY transactions.Player_id ORDER BY SUM(value) DESC") as cursor:
        return list(map(lambda row: {
                    "name": row[0],
                    "profit": row[1]
                    }, await cursor.fetchall()))


async def get_player_ids(db, player_list):
    async with db.execute('SELECT Id FROM players WHERE name IN ({0})'.format(', '.join(map(lambda x: "\"{0}\"".format(x), player_list)))) as cursor:
        return list(map(lambda x: x[0], await cursor.fetchall()))


async def get_auctions(db, key):
    async with db.execute('SELECT Id, Open FROM auctions WHERE Key = ?', (key,)) as cursor:
        return list(map(lambda x: {"id": x[0], "open": True if x[1] == 1 else False}, await cursor.fetchall()))


async def is_open(db, auction_id):
    async with db.execute('SELECT Open FROM auctions WHERE Id = ?', (auction_id,)) as cursor:
        return True if await cursor.fetchone() == (1,) else False


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
    async with db_write:
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


async def insert_auction(db, players, key):
    async with db_write:
        async with db.execute(
            "INSERT INTO auctions (Key, Open) VALUES (?, 1)", (key,)
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


async def get_ports(db, auction_id):
    ret = []
    async with db.execute("SELECT Port FROM players, auction_players WHERE auction_players.Auction_id = ? AND auction_players.Player_id = players.Id", [auction_id]) as cursor:
        async for row in cursor:
            ret.append(row[0])
    return ret


async def insert_bid(db, bid_value, auction_id, player_id):
    async with db_write:
        await db.execute(
            "INSERT INTO bids (Auction_id, Player_id, bid_value) VALUES(?, ?, ?)",
            [auction_id, player_id, bid_value],
        )
        await db.commit()
        await log(db, {
            "player_id": player_id,
            "auction_id": auction_id,
            "Desc": "Bid received for {}".format(bid_value),
            "Severity": "Notify"
        })
    return player_id


async def finish_auction(db, auction_id):
    async with db_write:
        ret = []
        async with db.execute("SELECT Player_id, bid_value, Id FROM bids WHERE Auction_id = ? AND bid_value = (SELECT MAX(bid_value) FROM bids WHERE Auction_id = ?)", [auction_id, auction_id]) as cursor:
            async for row in cursor:
                ret.append((row[0], row[1], row[2]))
        try:
            result = random.choice(ret)
            await db.execute(
                "INSERT INTO  logs (Player_id, Auction_id, Desc, Severity) SELECT bids.Player_id, bids.Auction_id, printf(\"Paid %f\",MAX(bids.bid_value)), \"Notify\" FROM bids WHERE bids.Auction_id = ? AND bids.Timestamp <= (SELECT bids2.Timestamp FROM bids AS bids2 WHERE bids2.Id = ?) GROUP BY bids.Player_id",
                [auction_id, result[2]]
            )
            await db.commit()
            await db.execute(
                "INSERT INTO  transactions (Player_id, value) SELECT bids.Player_id, -MAX(bids.bid_value) FROM bids WHERE bids.Auction_id = ? AND bids.Timestamp <= (SELECT bids2.Timestamp FROM bids AS bids2 WHERE bids2.Id = ?) GROUP BY bids.Player_id",
                [auction_id, result[2]]
            )
            await db.commit()
            await db.execute("INSERT INTO transactions (Player_id, value) VALUES (?, ?)", [result[0], 1])
            await db.commit()
            await log(db, {
                "player_id": result[0],
                "auction_id": auction_id,
                "Desc": "Won by bidding {}".format(result[1]),
                "Severity": "Notify"
            })
        except IndexError:
            await log(db, {
                "player_id": -1,
                "auction_id": auction_id,
                "Desc": "Auction closed uncompeted",
                "Severity": "Notify"
            })
            result = (-1, 0, -1)
        await db.execute("UPDATE auctions SET Open = 0 WHERE Id = ?", (auction_id,))
        await db.commit()
    return result
