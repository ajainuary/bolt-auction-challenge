class Auction:
    participants = []
    bids = {}
    start = INT_MAX

    def __init__(self, id):
        super().__init__()
        self.id = id

    def attach(self, player):
        self.participants.append(player)
        player.announce(self.id)

    def broadcast(self, player_id, bid):
        for p in self.participants:
            p.listen(player_id, bid)

    def submit(self, player_id, bid):
        if bid > 1.125*self.bids[player_id]:
            self.bids[player_id] = bid
            self.broadcast(player_id, bid)

    def judge(self):
        winning_bid = 0
        winning_player = -1
        for p in self.participants:
            if self.bids[p.id] > winning_bid:
                winning_bid = self.bids[p.id]
                winning_player = p.id
        return winning_player, winning_bid
