import websocket
import threading
import json

from utils.pricelevel import OrderBookUpdate, PriceLevel


def make_request(action, params, id):
    request = {
        "method": action,
        "params": params,
        "id": id
    }

    return json.dumps(request)


def get_order_book_updates(msg):
    parsed = json.loads(msg)
    event = parsed["e"] if "e" in parsed else ""
    if event != "depthUpdate":
        print("Error: {} not supported".format(msg))
        return "", []
    symbol = parsed["s"]
    res = OrderBookUpdate()
    res.begin_ts = int(parsed["U"])
    res.end_ts = int(parsed["u"])

    # TODO make a func
    for elem in parsed["b"]:
        pl = PriceLevel()
        pl.price = float(elem[0])
        pl.volume = float(elem[1])
        pl.is_bid = True
        res.updates.append(pl)

    for elem in parsed["a"]:
        pl = PriceLevel()
        pl.price = float(elem[0])
        pl.volume = float(elem[1])
        pl.is_bid = False
        res.updates.append(pl)

    return symbol, res


class WsUpdatesProvider:
    def __init__(self, url):
        websocket.enableTrace(True)
        self._ws = websocket.WebSocketApp(url,
                                          on_message=self._on_message,
                                          on_open=self._on_open,
                                          on_error=self._on_error,
                                          on_close=self._on_close)

        self._sinks = {}
        self._mutex = threading.Lock()
        self._is_ready = False

        self._thread = threading.Thread(target=self._ws.run_forever)
        self._thread.start()

    def is_ready(self):
        return self._is_ready

    def subscribe(self, symbol, sink):
        self._mutex.acquire()
        if symbol not in self._sinks:
            self._sinks[symbol] = []
        self._sinks[symbol].append(sink)
        self._mutex.release()

        # TODO proper ids
        req = make_request("SUBSCRIBE", ["{}@depth".format(symbol.lower())], 1)
        print("request = ", req)
        self._ws.send(req)

    def close(self):
        self._ws.close()
        # TODO sometimes the thread can't be joined for some reason.
        self._thread.join()

    # callbacks
    def _on_error(self, error):
        print("WsUpdatesProvider Error: ", error)
        self.close()

    def _on_close(self):
        print("WsUpdatesProvider closing")

    def _on_open(self):
        print("WsUpdatesProvider Ready")
        self._is_ready = True

    def _on_message(self, message):
        symbol, updates = get_order_book_updates(message)
        if len(symbol) == 0:
            print("unsupported message: ", message)
            return

        if symbol not in self._sinks:
            return

        self._mutex.acquire()
        for s in self._sinks[symbol]:
            s.on_update(symbol, updates)
        self._mutex.release()
