import aiohttp
import asyncio


async def broadcast(msg, players):
    send_requests = []
