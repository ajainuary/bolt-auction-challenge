import aiohttp
import asyncio
from aiohttp import web
from strategy import Client


async def receive(request):
    data = {'status': 'OK'}
    data = await request.json()
    print(data)
    return web.json_response(data)

app = web.Application()
app.router.add_post("/receive", receive)
web.run_app(app, port=9090)
