from db import get_ports
import aiohttp
import asyncio
from db import get_ports, finish_auction
from numpy.random import normal


async def send(client, port, msg, delay):
    await asyncio.sleep(delay)
    loop = asyncio.get_event_loop()
    loop.create_task(client.post(
        "http://localhost:{}/receive".format(port), json=msg))


async def broadcast(db, client, msg, auction_id):
    ports = await get_ports(db, auction_id)
    delays = normal(5, 2, len(ports)).tolist()
    send_requests = [send(client, port, msg, delay)
                     for port, delay in zip(ports, delays)]
    await asyncio.gather(*send_requests)


async def complete_auction(request, auction):
    result = await finish_auction(request.config_dict["DB"], auction['id'])
    loop = asyncio.get_event_loop()
    loop.create_task(broadcast(request.config_dict["DB"], request.config_dict["client"], {
                     "type": "END", "Auction_id": auction['id'], "Winner": result[0], "Winning_Value": result[1]}, auction['id']))
