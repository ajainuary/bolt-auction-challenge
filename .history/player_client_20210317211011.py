import aiohttp
import asyncio
from aiohttp import web
from my_bots.dummy import DummyBot
from typing import AsyncIterator

bot = DummyBot()
PORT = 9090


async def init_bot(app: web.Application) -> AsyncIterator[None]:
    session = aiohttp.ClientSession()
    async with session.post("http://0.0.0.0:8080/register", json={'name': 'Anurag', 'port': PORT}) as resp:
        data = await resp.json()
        app["bot"] = bot.register(session, data['id'])
    yield
    await session.close()


async def receive(request):
    data = {'status': 'OK'}
    data = await request.json()
    print(request.config_dict["bot"])
    if data['type'] == 'START':
        await request.config_dict["bot"].start(data['Auction_id'])
    elif data['type'] == 'BID' and data['Player_id'] != request.config_dict["bot"].id:
        await request.config_dict["bot"].receive_bid(data['Auction_id'], data['bid_value'])
    elif data['type'] == 'END':
        await request.config_dict["bot"].end_auction(data['Auction_id'])
    return web.json_response(data)

app = web.Application()
app.cleanup_ctx.append(init_bot)
app.router.add_post("/receive", receive)
web.run_app(app, port=9090)
