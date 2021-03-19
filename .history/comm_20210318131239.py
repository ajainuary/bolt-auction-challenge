from db import get_ports
import aiohttp
import asyncio
from db import get_ports
from numpy.random import normal


async def send(port, msg, delay):
    await asyncio.sleep(delay)
    await client.post("http://localhost:{}/receive".format(port), json=msg)


async def broadcast(db, client, msg, auction_id):
    ports = await get_ports(db, auction_id)
    delays = normal(5, 2, len(ports)).tolist()
    send_requests = [for port, delay in zip(ports, delays)]
    await asyncio.gather(*send_requests)
