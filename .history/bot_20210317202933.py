from client import Client


class Bot(Client):
    def __init__(self, session):
        super().__init__(session)
        # Your Initialization Code Here
        pass

    def start(self, auction_id):
        return super().start(auction_id)
