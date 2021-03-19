class Client:
    def __init__(self, session):
        self.session = session

    def register(self, id, port):
        self.id = id
        self.port = port
        self.auctions = {}

    def start(self, auction_id):
        self.auctions.add(auction_id)

    def submit_bid(self, auction_id):
