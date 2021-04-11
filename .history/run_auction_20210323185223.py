import aiohttp
import asyncio
import sys

if len(sys.argv) != 3:
    print("Incorrect arguments")
    exit(0)

duration = int(sys.argv[1])
key = int(sys.argv[2])
players = ['Batman', 'Superman']  # Select the names of your bots here

if duration <= 0:
    print("Please use a positive duration")


async def end(session):
    await asyncio.sleep(duration)
    await session.post('http://localhost:8080/end_auction', json={'key': key})


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(session.post('http://localhost:8080/new_auction', json={'players': players, 'key': key}), end(session))
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
