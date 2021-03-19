import aiohttp
import asyncio

id = int(sys.argv[1])


async def end(session):
    await asyncio.sleep(15)
    await session.post('http://localhost:8080/end_auction', json={'auction_id': 1})


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
            1, 2]}), end(session))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
