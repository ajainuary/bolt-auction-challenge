class Client:
    def __init__(self, session):
        session.post("http://0.0.0.0:8080/register",
                     json={'name': 'Anurag', 'port': 9090})

    def submit_bid(bid_value):
