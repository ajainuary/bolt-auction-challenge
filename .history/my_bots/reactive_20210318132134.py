from .client import Client


class ReactiveBot(Client):
    def __init__(self):
        # Your Initialization Code Here
        self.s = 0.1
        self.e = 0.2
        self.last_bid = 0
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        await super().submit_bid(auction_id, self.s)
        self.last_bid = self.s

    async def receive_bid(self, auction_id, bid_value):
        # Your code for receiving bids

        pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
