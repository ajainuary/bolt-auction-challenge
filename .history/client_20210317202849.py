class Client:
    def __init__(self, session):
        self.session = session
        pass

    def register(self, id, port):
        self.id = id
        self.port = port
        self.auctions = set()

    async def start(self, auction_id):
        self.auctions.add(auction_id)
        pass

    async def submit_bid(self, auction_id, bid_value):
        if auction_id in self.auctions:
            await self.session.post('http://localhost:8080/submit_bid', json={
                'bid': bid_value,
                'auction_id': auction_id,
                'player_id': self.id
            })

    async def receive_bid(self, auction_id, bid_value):
        pass

    async def end_auction(self, auction_id):
        self.auctions.remove(auction_id)
        pass
