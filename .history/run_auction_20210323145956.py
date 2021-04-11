import aiohttp
import asyncio
import sys

key = int(sys.argv[1])


async def end(session):
    await asyncio.sleep(15)
    await session.post('http://localhost:8080/end_auction', json={'key': key})


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
            'Batman', 'Superman'], 'key': key}), end(session))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
