# import pytest
# from container_packing.binary_search_iterator import BinarySearchIterator

# def test_binary_search_iterator_basic():
#     iterator = BinarySearchIterator(low=0, high=10)
#     visited = []
#     while iterator.has_next():
#         mid = iterator.next()
#         visited.append(mid)
#         # Decide how to move boundaries
#         if mid < 5:
#             iterator.higher()
#         else:
#             iterator.lower()
#     # Just verify we moved around somewhat correctly
#     assert len(visited) > 0
#     assert all(isinstance(v, int) for v in visited)

# def test_binary_search_iterator_reset():
#     iterator = BinarySearchIterator()
#     iterator.reset(high=20, low=10)
#     assert iterator.high == 20
#     assert iterator.low == 10
#     assert iterator.has_next() is True
