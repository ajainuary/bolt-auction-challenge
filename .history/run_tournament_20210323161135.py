import aiohttp
import asyncio
import sys

if len(sys.argv) != 2:
    print("Incorrect arguments")

duration = int(sys.argv[1])
key = int(sys.argv[2])

if duration <= 0:
    print("Please use a positive duration")


async def end(duration, session):
    await asyncio.sleep(duration)
    await session.post('http://localhost:8080/end_auction', json={'key': key})


async def run_auction(key, duration, session):
    await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
        'Batman', 'Superman'], 'key': key}), end(duration, session))


async def main():
    async with aiohttp.ClientSession() as session:

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
