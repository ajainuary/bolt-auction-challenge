import aiohttp
import asyncio
import sys
from numpy.random import exponential

if len(sys.argv) != 2:
    print("Incorrect arguments")

n = int(sys.argv[1])

if duration <= 0:
    print("Please use a positive duration")


async def end(duration, session):
    await asyncio.sleep(duration)
    await session.post('http://localhost:8080/end_auction', json={'key': key})


async def run_auction(key, duration, session):
    await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': [
        'Batman', 'Superman'], 'key': key}), end(duration, session))


async def main():
    ending_times = exponential(15, n).tolist()
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[run_auction(key, duration, session) for key, duration in zip(range(1, n+1), ending_times)])
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
