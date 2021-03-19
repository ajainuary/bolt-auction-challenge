import aiohttp
import asyncio
from aiohttp import web
from client import Client

session = aiohttp.ClientSession()


async def register(): :
    async with session.post("http://0.0.0.0:8080/register", json={'name': 'Anurag', 'port': 9090}) as resp:
        registration = await resp.json()


async def receive(request):
    data = {'status': 'OK'}
    data = await request.json()
    print(data)
    return web.json_response(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(register())
app = web.Application()
app.router.add_post("/receive", receive)
web.run_app(app, port=9090)
