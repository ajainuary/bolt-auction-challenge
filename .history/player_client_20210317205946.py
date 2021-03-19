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
        app["bot"] = bot.register(client, data['id'])
    yield
    await session.close()


async def receive(request):
    data = {'status': 'OK'}
    data = await request.json()
    print(data)
    return web.json_response(data)
app = web.Application()
app.cleanup_ctx.append(init_bot)
app.router.add_post("/receive", receive)
web.run_app(app, port=9090)
