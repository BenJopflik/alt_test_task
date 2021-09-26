import threading


class OrderBookBuilder:
    def __init__(self):
        self._ob = None
        self._updates = []
        self._mutex = threading.Lock()

    def _apply_updates(self, updates):
        ts = updates.end_ts
        for update in updates.updates:
            self._ob.update(update.price, update.volume, ts, update.is_bid)

    def on_ob(self, ob):
        self._mutex.acquire()
        if len(self._updates) == 0:
            self._mutex.release()
            return

        begin_ts = self._updates[0].begin_ts
        if ob.ts() < begin_ts:
            self._mutex.release()
            return

        ob_ts = ob.ts()
        self._ob = ob
        for update in self._updates:
            if update.end_ts < ob_ts:
                continue
            self._apply_updates(update)
        self._updates = []
        self._mutex.release()

    def on_update(self, updates):
        self._mutex.acquire()

        if self._ob is None:
            self._updates.append(updates)
        else:
            self._apply_updates(updates)

        self._mutex.release()

    def snapshot(self, depth):
        self._mutex.acquire()

        if self._ob is None:
            self._mutex.release()
            return -1, [], []
        res = self._ob.snapshot(depth)

        self._mutex.release()

        return res
