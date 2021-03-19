from db import get_ports
import aiohttp
import asyncio
from db import get_ports


async def send(port, msg):
    await client.post("http://localhost:{}/receive".format(port), json=msg)


async def broadcast(db, client, msg, auction_id):
    ports = await get_ports(db, auction_id)
    send_requests = [for port in ports]
    await asyncio.gather(*send_requests)
