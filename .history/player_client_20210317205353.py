import aiohttp
import asyncio
from aiohttp import web
from my_bots.dummy import DummyBot

bot = DummyBot()


async def init_bot(app: web.Application) -> AsyncIterator[None]:
    client = aiohttp.ClientSession()
    app["bot"] = bot(client)
    yield
    await db.close()


async def receive(request):
    data = {'status': 'OK'}
    data = await request.json()
    print(data)
    return web.json_response(data)

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
app = web.Application()
app.router.add_post("/receive", receive)
web.run_app(app, port=9090)
