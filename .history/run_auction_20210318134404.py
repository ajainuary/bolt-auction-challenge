import aiohttp
import asyncio


async def main():

    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:8080/new_auction', json={'players': [1, 2]}) as response:
            data = await resp.json()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
