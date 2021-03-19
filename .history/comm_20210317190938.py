from db import get_ports
import aiohttp
import asyncio
from db import get_ports


async def broadcast(db, client, msg, auction_id):
    ports = await get_ports(db, auction_id)
    send_requests = [client.post(
        "http://localhost:{}/receive".format(port), json=msg) for port in ports]
    await asyncio.gather(*send_requests)
