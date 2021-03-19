class Client:

    def register(self, id, port):
        self.id = id
        self.port = port
        self.auctions = {}
        self.session = session

    async def start(self, auction_id):
        self.auctions[auction_id] = 0
        pass

    async def submit_bid(self, auction_id, bid_value):
        if auction_id in self.auctions and bid_value >= 1.125*self.auctions[auction_id]:
            self.auctions[auction_id] = bid_value
            await self.session.post('http://localhost:8080/submit_bid', json={
                'bid': bid_value,
                'auction_id': auction_id,
                'player_id': self.id
            })

    async def receive_bid(self, auction_id, bid_value):
        pass

    async def end_auction(self, auction_id):
        self.auctions.pop(auction_id)
        pass
