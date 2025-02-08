import pytest
from container_packing.shortcuts import pack_products_into_restrictions

def test_pack_products_into_restrictions_success():
    products = [
        # Each is (width, depth, height)
        (2, 2, 2),
        (3, 3, 3)
    ]
    restrictions = (10, 10, 10)
    result = pack_products_into_restrictions(products, restrictions)
    assert result is not None
    # e.g. we might get minimal used (somewhere up to 5 in width or so),
    # but we only know that it must not exceed 10
    assert result[0] <= 10
    assert result[1] <= 10
    assert result[2] <= 10

def test_pack_products_into_restrictions_no_fit():
    products = [
        (10, 10, 10),
        (1, 1, 20)  # height 20 => won't fit into height=10 container
    ]
    restrictions = (10, 10, 10)
    result = pack_products_into_restrictions(products, restrictions)
    assert result is None
