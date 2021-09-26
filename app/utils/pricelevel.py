class PriceLevel:
    def __init__(self):
        self.price = 0
        self.volume = 0
        self.is_bid = False


class OrderBookUpdate:
    def __init__(self):
        self.begin_ts = 0
        self.end_ts = 0

        self.updates = []
