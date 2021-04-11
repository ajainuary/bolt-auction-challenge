from .client import Client
import asyncio


class FixedBot(Client):
    def __init__(self):
        # Your Initialization Code Here
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        await super().submit_bid(auction_id, 0.1)
        for i in range(3):
            await asyncio.sleep(1)
            print("Time to submit a bid")
            await super().submit_bid(auction_id, 0.4+0.3*i)

    async def receive_bid(self, auction_id, bid_value):
        # Your code for receiving bids
        pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
