from .client import Client


class DummyBot(Client):
    def __init__(self):
        super().__init__()
        self.name = "Superman"  # Your Bot's Name
        # Your Initialization Code Here

    async def start(self, auction_id):
        await super().start(auction_id)
        # Your code for starting an auction

    async def receive_bid(self, auction_id, bid_value):
        await super().receive_bid(auction_id, bid_value)
        # Your code for receiving bids

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
