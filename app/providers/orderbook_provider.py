import time

from utils.orderbook_builder import OrderBookBuilder


class OrderBookProvider:
    def __init__(self, snapshot_provider, updates_provider):
        self._snapshot_provider = snapshot_provider
        self._updates_provider = updates_provider
        self._obs = {}
        self._updates = {}

    def get_orderbook(self, symbol, depth):
        if symbol not in self._obs:
            self._updates_provider.subscribe(symbol, self)
            self._obs[symbol] = OrderBookBuilder()

        while True:
            ts, asks, bids = self._obs[symbol].snapshot(depth)
            if ts != -1:
                return ts, asks, bids
            ob = self._snapshot_provider.get_snapshot(symbol)
            if ob is None:
                print("invalid symbol {}".format(symbol))
                return None
            self._obs[symbol].on_ob(ob)
            # XXX not the best idea
            time.sleep(1)

    def on_update(self, symbol, updates):
        if symbol not in self._obs:
            print("symbol not found ", symbol)
            return
        self._obs[symbol].on_update(updates)

    def close(self):
        self._snapshot_provider.close()
        self._updates_provider.close()
