import time


class Client:

    def register(self, session, id):
        self.id = id
        self.auctions = {}
        self.session = session
        self.name = "Untitled Bot"

    async def start(self, auction_id):
        self.auctions[auction_id] = (0, 0)
        pass

    async def submit_bid(self, auction_id, bid_value):
        T = time.time()
        if auction_id in self.auctions and bid_value >= 1.125*self.auctions[auction_id][0] and T - self.auctions[auction_id][1] >= 5:
            self.auctions[auction_id] = (bid_value, T)
            await self.session.post('http://localhost:8080/submit_bid', json={
                'bid': bid_value,
                'auction_id': auction_id,
                'player_id': self.id
            })
            return True
        return False

    async def receive_bid(self, auction_id, bid_value):
        if auction_id not in self.auctions:
            await self.start(auction_id)

    async def end_auction(self, auction_id):
        if auction_id not in self.auctions:
            await self.start(auction_id)
        self.auctions.pop(auction_id)
        pass
