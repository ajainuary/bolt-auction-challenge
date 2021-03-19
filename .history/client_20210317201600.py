class Client:
    def __init__(self, session):
        self.session = session

    def register(self, id, port):
        self.id = id
        self.port = port
        self.auctions = {}

    def start(auction_id):
