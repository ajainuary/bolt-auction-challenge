import aiohttp
import asyncio


async def broadcast(client, msg, auction_id):
    send_requests = [client.post(
        "http://localhost:{}/receive".format(port), json=msg) for port in ports]
    await asyncio.gather(*send_requests)
