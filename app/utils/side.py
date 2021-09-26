class Side:
    def __init__(self):
        self._storage = {}

    def clear(self):
        self._storage = {}

    def update(self, price, volume):
        if float(volume) == 0.0:
            self._storage.pop(price, None)
        else:
            self._storage[price] = volume

    def snapshot(self, depth, reverse):
        keys = sorted(self._storage.keys(), reverse=reverse)[:depth]
        res = []
        for key in keys:
            res.append([key, self._storage[key]])
        return res
