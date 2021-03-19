import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
                       1, 2]}), session.post('http://localhost:8080/end_auction', json={'auction_id': 1}))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
