# views.py
import aiohttp_jinja2
import asyncio
from aiohttp import web
from db import get_leaderboard, get_logs, get_player_ids, get_auctions, insert_player, insert_auction, insert_bid, is_open
from comm import broadcast, complete_auction


@aiohttp_jinja2.template('index.html')
async def index(request):
    logs = await get_logs(request.config_dict["DB"])
    return {'logs': logs}


@aiohttp_jinja2.template('leaderboard.html')
async def leaderboard(request):
    board = await get_leaderboard(request.config_dict["DB"])
    return {'leaderboard': board}


async def register(request):
    data = await request.json()
    name = data['name']
    port = data['port']

    id = await insert_player(request.config_dict["DB"], name, port)

    return web.json_response(
        {
            "status": "OK",
            "id": id
        }
    )


async def new_auction(request):
    data = await request.json()
    players = data['players']
    key = data['key']
    player_ids = await get_player_ids(request.config_dict["DB"], players)
    id = await insert_auction(request.config_dict["DB"], player_ids, key)
    loop = asyncio.get_event_loop()
    loop.create_task(broadcast(request.config_dict["DB"], request.config_dict["client"], {
                     "type": "START", "Auction_id": id}, id))
    return web.json_response(
        {
            "id": id
        }
    )


async def submit_bid(request):
    data = await request.json()
    bid_value = data['bid']
    auction_id = data['auction_id']
    player_id = data['player_id']
    await insert_bid(request.config_dict["DB"], bid_value, auction_id, player_id)
    if await is_open(request.config_dict["DB"], auction_id):
        loop = asyncio.get_event_loop()
        loop.create_task(broadcast(request.config_dict["DB"], request.config_dict["client"], {
                         "type": "BID", "Auction_id": auction_id, "bid_value": bid_value, "Player_id": player_id}, auction_id))
    return web.json_response(
        {
            "status": "OK"
        }
    )


async def end_auction(request):
    data = await request.json()
    key = data['key']
    auctions = await get_auctions(request.config_dict["DB"], key)
    asyncio.gather(*[complete_auction(request, a)
                     for a in filter(lambda x: x['open'], auctions)])
    return web.json_response(
        {
            "status": "OK"
        }
    )
