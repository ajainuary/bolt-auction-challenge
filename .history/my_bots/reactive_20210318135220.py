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
        print(auction_id)
        self.last_bid[auction_id] = self.s

    async def receive_bid(self, auction_id, bid_value):
        # Your code for receiving bids
        try:
            last = self.last_bid[auction_id]
            if bid_value > last:
                new_bid = min(max(last*1.125, last+self.e), 1+last)
                if new_bid > bid_value:
                    await super().submit_bid(auction_id, new_bid)
        except:
            pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
