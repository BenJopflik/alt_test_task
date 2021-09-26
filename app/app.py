from flask import Flask

import sys

from providers.orderbook_provider import OrderBookProvider
from providers.snapshot_provider import BinanceHttpSnapshotProvider
from providers.updates_provider import WsUpdatesProvider

from templates.templates import *

app = Flask(__name__)

sp = None
op = None


def prepare_table(levels):
    res = ""
    for elem in levels:
        res += orderbook_pricelevel_template.format(price=elem[0], volume=elem[1]) + "\n"
    return res


def prepare_page(symbol, ts, bids, asks):
    return orderbook_template.format(
        style=style,
        symbol=symbol,
        ts=ts,
        asks=prepare_table(asks[::-1]),
        bids=prepare_table(bids)
    )


@app.route('/http_orderbook/<symbol>')
def http_orderbook(symbol):
    try:
        arr = sp.get_snapshot(symbol)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "<h2>Symbol not found {}</h2>".format(symbol)

    ts, bids, asks = arr.snapshot(20)
    return prepare_page(symbol, ts, bids, asks)


@app.route('/ws_orderbook/<symbol>')
def ws_orderbook(symbol):
    try:
        ts, bids, asks = op.get_orderbook(symbol, 20)
        return prepare_page(symbol, ts, bids, asks)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return "<h2>Symbol not found {}</h2>".format(symbol)


if __name__ == "__main__":
    up = WsUpdatesProvider("wss://stream.binance.com:9443/ws")
    print("starting WsUpdatesProvider")
    while not up.is_ready():
        continue
    sp = BinanceHttpSnapshotProvider("https://api.binance.me/api/v3")
    op = OrderBookProvider(sp, up)

    app.run(host='0.0.0.0')
    op.close()
