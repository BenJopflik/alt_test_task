import pytest

from app.utils.side import Side

def test_side():
    side = Side()
    arr = side.snapshot(3, False)
    assert len(arr) == 0

    side.update(100, 100)
    side.update(101, 101)
    side.update(102, 102)
    side.update(103, 103)
    side.update(104, 104)
    side.update(104, 71)
    # removing the level
    side.update(100, 0)

    arr = side.snapshot(3, False)
    assert len(arr) == 3
    assert arr[0][0] == 101
    assert arr[1][0] == 102
    assert arr[2][0] == 103

    arr = side.snapshot(3, True)
    assert len(arr) == 3
    assert arr[0][0] == 104
    assert arr[0][1] == 71 
    assert arr[1][0] == 103
    assert arr[2][0] == 102

    side.clear()
    arr = side.snapshot(3, False)
    assert len(arr) == 0