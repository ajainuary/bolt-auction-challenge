class Client:
    def __init__(self, id, port, session):
        session.post("http://0.0.0.0:8080/register",
                     json={'name': 'Anurag', 'port': 9090})
        self.id = id
        self.session = session
        self.port = port

    def submit_bid(bid_value):
