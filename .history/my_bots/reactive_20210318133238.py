from .client import Client


class ReactiveBot(Client):
    def __init__(self):
        # Your Initialization Code Here
        self.s = 0.1
        self.e = 0.2
        self.last_bid = {}
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        await super().submit_bid(auction_id, self.s)
        self.last_bid = self.s

    async def receive_bid(self, auction_id, bid_value):
        # Your code for receiving bids
        if bid_value > self.last_bid:
            new_bid = min(
                max(self.last_bid*1.125, self.last_bid+self.e), 1+self.last_bid)
            if new_bid > bid_value:
                super().submit_bid(auction_id, bid_value)
        pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
