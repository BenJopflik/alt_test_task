from app.utils.orderbook import OrderBook

def test_orderbook():
    ob = OrderBook()

    ts, bids, asks = ob.snapshot(3)
    assert ts == 0
    assert len(bids) == 0
    assert len(asks) == 0

    ob.update(1, 1, 1, True)
    ob.update(2, 2, 2, True)
    ob.update(3, 3, 3, True)
    ob.update(3, 0, 3, True)

    ob.update(4, 4, 4, False)
    ob.update(5, 5, 5, False)

    ts, bids, asks = ob.snapshot(3)
    assert ts == 5
    assert len(bids) == 2
    assert bids[0][0] == 2
    assert bids[1][0] == 1

    assert len(asks) == 2
    assert asks[0][0] == 4
    assert asks[1][0] == 5

    ob.clear() 

    ts, bids, asks = ob.snapshot(3)
    assert ts == 0
    assert len(bids) == 0
    assert len(asks) == 0

