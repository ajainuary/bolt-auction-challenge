import aiohttp
import asyncio


async def broadcast(client, msg, players):
    send_requests = []
