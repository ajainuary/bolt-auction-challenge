import aiohttp
import asyncio


async def main():
    auction_id = -1
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/new_auction', json={'players': [1, 2]}) as response:
            data = await response.json()
            auction_id = data['id']

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
