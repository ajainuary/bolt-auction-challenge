from .client import Client


class ReactiveBot(Client):
    def __init__(self):
        super().__init__()
        # Your Initialization Code Here
        self.s = 0.1
        self.e = 0.2
        self.last_bid = {}
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        self.last_bid[auction_id] = self.s
        await super().submit_bid(auction_id, self.s)

    async def receive_bid(self, auction_id, bid_value):
        await super().receive_bid(auction_id, bid_value)
        # Your code for receiving bids
        last = self.last_bid[auction_id]
        if bid_value >= last:
            new_bid = min(max(last*1.125, last+self.e), 1)
            if new_bid > bid_value:
                self.last_bid[auction_id] = new_bid
                await super().submit_bid(auction_id, new_bid)

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
