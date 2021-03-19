from ...client import Client


class Bot(Client):
    def __init__(self, session):
        super().__init__(session)
        # Your Initialization Code Here

    async def start(self, auction_id):
        await super().start(auction_id)
        # Your code for starting auction

    async def receive_bid(self, auction_id, bid_value):
        # Your code for receiving bids
        pass

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        # Your code for ending auction
