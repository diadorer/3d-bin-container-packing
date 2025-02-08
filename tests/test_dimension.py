import pytest
from container_packing.dimension import Dimension

def test_dimension_init():
    dim = Dimension("Name", 10, 20, 30)
    assert dim.name == "Name"
    assert dim.width == 10
    assert dim.depth == 20
    assert dim.height == 30
    assert dim.volume == 10 * 20 * 30

def test_dimension_decode():
    dim = Dimension.decode("5x6x7")
    assert dim.width == 5
    assert dim.depth == 6
    assert dim.height == 7

def test_dimension_encode():
    dim = Dimension("MyDim", 1, 2, 3)
    encoded = dim.encode()
    assert encoded == "1x2x3"

def test_dimension_can_hold_3d():
    dim1 = Dimension("D1", 10, 10, 10)
    dim2 = Dimension("D2", 9, 10, 10)
    assert dim1.can_hold_3d(dim2) is True
    assert dim2.can_hold_3d(dim1) is False  # 9 vs 10, but can it hold 10? No

def test_dimension_can_hold_2d():
    dim1 = Dimension("D1", 10, 5, 100)
    dim2 = Dimension("D2", 5, 5, 10)
    # 2D check -> height of dim2 (10) <= 100 => OK
    # width=5, depth=5 can fit into width=10, depth=5
    assert dim1.can_hold_2d(dim2) is True
