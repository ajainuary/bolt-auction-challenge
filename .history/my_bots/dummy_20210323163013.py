from .client import Client


class DummyBot(Client):
    def __init__(self):
        # Your Initialization Code Here
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        await super().submit_bid(auction_id, 1)

    async def receive_bid(self, auction_id, bid_value):
        await super().start(auction_id)
        # Your code for receiving bids
        pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
