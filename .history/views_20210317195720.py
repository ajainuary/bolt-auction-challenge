# views.py
import aiohttp_jinja2
from aiohttp import web
from db import get_logs, insert_player, insert_auction, insert_bid, get_winner
from comm import broadcast


@aiohttp_jinja2.template('index.html')
async def index(request):
    logs = await get_logs(request.config_dict["DB"])
    return {'logs': logs}


async def register(request):
    data = await request.json()
    name = data['name']
    port = data['port']

    id = await insert_player(request.config_dict["DB"], name, port)

    return web.json_response(
        {
            "status": "OK",
            "data": {
                "id": id
            },
        }
    )


async def new_auction(request):
    data = await request.json()
    players = data['players']
    id = await insert_auction(request.config_dict["DB"], players)
    await broadcast(request.config_dict["DB"], request.config_dict["client"], {"type": "START", "Auction_id": id}, id)
    return web.json_response(
        {
            "status": "OK",
            "data": {
                "id": id
            },
        }
    )


async def submit_bid(request):
    data = await request.json()
    bid_value = data['bid']
    auction_id = data['auction_id']
    player_id = data['player_id']
    await insert_bid(request.config_dict["DB"], bid_value, auction_id, player_id)
    await broadcast(request.config_dict["DB"], request.config_dict["client"], {"type": "BID", "Auction_id": auction_id, "bid_value": bid_value}, auction_id)
    return web.json_response(
        {
            "status": "OK"
        }
    )


async def end_auction(request):
    data = await request.json()
    auction_id = data['auction_id']
    result = await get_winner(request.config_dict["DB"], auction_id)
    await broadcast(request.config_dict["DB"], request.config_dict["client"], {"type": "END", "Auction_id": auction_id, "Winner": result[0], "Winning_Value": result[1]})
    return web.json_response(
        {
            "status": "OK"
        }
    )
