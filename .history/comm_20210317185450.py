import aiohttp
import asyncio


async def broadcast(client, msg, players):
    send_requests = [client.post(
        "http://localhost:{}/receive".format(port), json=msg) for port in players]
