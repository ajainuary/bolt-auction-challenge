import aiohttp
import asyncio
from aiohttp import web
from my_bots.dummy import DummyBot

bot = DummyBot()


async def init_bot(app: web.Application) -> AsyncIterator[None]:
    session = aiohttp.ClientSession()
    async with session.post("http://0.0.0.0:8080/register", json={'name': 'Anurag', 'port': 9090}) as resp:
        print(resp)
    app["bot"] = bot.setuo(client)
    yield
    await client.close()


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
