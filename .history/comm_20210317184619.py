import aiohttp
import asyncio


async def broadcast(client, msg, players):
    send_requests = [client.post(
        "http://0.0.0.0:8080/register", json={'name': 'Anurag', 'port': 9090})]
