from client import Client


class Bot(Client):
    def __init__(self, session):
        super().__init__(session)
