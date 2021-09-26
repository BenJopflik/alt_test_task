from app.utils.orderbook_builder import OrderBookBuilder
from app.utils.orderbook import OrderBook
from app.utils.pricelevel import OrderBookUpdate, PriceLevel 

def test_orderbook_builder():
    obb = OrderBookBuilder()

    ts, _, _ = obb.snapshot(3)
    assert ts == 0

    ob = OrderBook()
    ob.update(0, 0, 1, True)

    obb.on_ob(ob)
    ts, _, _ = obb.snapshot(3)
    assert ts == 0

    to_skip = OrderBookUpdate()
    to_skip.begin_ts = 5
    to_skip.end_ts = 10
    to_skip.updates.append(PriceLevel())
    to_skip.updates[-1].price = 100
    to_skip.updates[-1].volume = 100
    to_skip.updates[-1].is_bid = False
    obb.on_update(to_skip)

    obb.on_ob(ob)
    ts, _, _ = obb.snapshot(3)
    assert ts == 0

    to_apply = OrderBookUpdate()
    to_apply.begin_ts = 11
    to_apply.end_ts = 18

    to_apply.updates.append(PriceLevel())
    to_apply.updates[-1].price = 1
    to_apply.updates[-1].volume = 1
    to_apply.updates[-1].is_bid = True

    to_apply.updates.append(PriceLevel())
    to_apply.updates[-1].price = 2
    to_apply.updates[-1].volume = 2
    to_apply.updates[-1].is_bid = True

    to_apply.updates.append(PriceLevel())
    to_apply.updates[-1].price = 3 
    to_apply.updates[-1].volume = 3 
    to_apply.updates[-1].is_bid = False

    obb.on_update(to_apply)

    ob.update(3, 100, 15, False)

    obb.on_ob(ob)
    ts, bids, asks = obb.snapshot(3)
    assert ts == 18
    assert len(bids) == 2
    assert len(asks) == 1
    assert asks[0][0] == 3
    assert asks[0][1] == 3