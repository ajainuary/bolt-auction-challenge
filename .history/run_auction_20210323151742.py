import aiohttp
import asyncio
import sys

duration = int(sys.argv[1])
key = int(sys.argv[2])


async def end(session):
    await asyncio.sleep(duration)
    print(duration, " Complete")
    await session.post('http://localhost:8080/end_auction', json={'key': key})


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
            'Batman', 'Superman'], 'key': key}), end(session))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
