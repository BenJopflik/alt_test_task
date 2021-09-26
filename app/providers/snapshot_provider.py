import requests

from utils.orderbook import OrderBook


def json_to_orderbook(data):
    ts = int(data['lastUpdateId'])
    bids = data['bids']
    asks = data['asks']

    ob = OrderBook()
    for elem in bids:
        ob.update(float(elem[0]), float(elem[1]), ts, True)

    for elem in asks:
        ob.update(float(elem[0]), float(elem[1]), ts, False)

    return ob


class BinanceHttpSnapshotProvider:
    def __init__(self, url):
        self._url = url

    def _make_request(self, symbol):
        return "{}/depth?symbol={}".format(self._url, symbol)

    def get_snapshot(self, symbol):
        print(self._make_request(symbol))
        response = requests.get(self._make_request(symbol)) 
        if response.status_code != 200:
            print("invalid symbol")
            return None
        print(response)
        return json_to_orderbook(response.json()) 

    def close(self):
        pass
