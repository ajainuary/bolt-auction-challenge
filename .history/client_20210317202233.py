class Client:
    def __init__(self, session):
        self.session = session

    def register(self, id, port):
        self.id = id
        self.port = port
        self.auctions = {}

    def start(self, auction_id):
        self.auctions.add(auction_id)

    async def submit_bid(self, auction_id, bid_value):
        if auction_id in self.auctions:
            self.session.post('http://localhost:8080/submit_bid', json={
                'bid': bid_value,
                'auction_id': auction_id,
                'player_id': self.id
            })
