from .client import Client
import asyncio


class Godzilla(Client):
    def __init__(self):
        super().__init__()
        self.name = "Godzilla"  # Your Bot's Name
        self.pattern = []
        self.auction_progress = {}
        self.auction_other_progress = {}
        self.last_bid = {}
        # Your Initialization Code Here
        pass

    async def start(self, auction_id):
        await super().start(auction_id)
        self.auction_progress[auction_id] = 0
        self.last_bid[auction_id] = 0
        if len(self.pattern) == 0:
            self.last_bid[auction_id] = 0.01
            await super().submit_bid(auction_id, 0.01)
            await asyncio.sleep(5)
        while auction_id in self.auction_progress and self.auction_progress[auction_id] < len(self.pattern):
            if self.pattern[self.auction_progress[auction_id]] < 1 or self.pattern[self.auction_progress[auction_id]] - 1 > self.last_bid[auction_id]:
                self.last_bid[auction_id] = self.pattern[self.auction_progress[auction_id]]+0.01
                bid_event = await super().submit_bid(auction_id, self.pattern[self.auction_progress[auction_id]]+0.01)
                if bid_event:
                    self.auction_progress[auction_id] += 1
                    await asyncio.sleep(5)
                else:
                    await asyncio.sleep(1)
            else:
                return

    async def receive_bid(self, auction_id, bid_value):
        await super().receive_bid(auction_id, bid_value)
        if auction_id not in self.auction_other_progress:
            self.auction_other_progress[auction_id] = 0
        if self.auction_other_progress[auction_id] >= len(self.pattern):
            self.pattern.append(bid_value)
        elif bid_value >= self.pattern[self.auction_other_progress[auction_id]]:
            self.pattern[self.auction_other_progress[auction_id]] = bid_value
            self.auction_other_progress[auction_id] += 1
            self.last_bid[auction_id] = bid_value+0.01
            await super().submit_bid(auction_id, bid_value+0.01)

    async def end_auction(self, auction_id):
        await super().end_auction(auction_id)
        self.auction_progress.pop(auction_id)
        if auction_id in self.auction_other_progress:
            self.auction_other_progress.pop(auction_id)
        if auction_id in self.last_bid:
            self.last_bid.pop(auction_id)
