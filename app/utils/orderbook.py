from utils.side import Side


class OrderBook:
    def __init__(self):
        self._bid = Side()
        self._ask = Side()
        self._ts = 0

    def ts(self):
        return self._ts

    def clear(self):
        self._ask.clear()
        self._bid.clear()
        self._ts = 0

    def update(self, price, volume, ts, is_bid):
        self._ts = ts

        if is_bid:
            self._bid.update(price, volume)
        else:
            self._ask.update(price, volume)

    def snapshot(self, depth):
        asks = self._ask.snapshot(depth, False)
        bids = self._bid.snapshot(depth, True)
        return self._ts, bids, asks
