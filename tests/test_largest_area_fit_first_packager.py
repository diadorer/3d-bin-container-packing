import pytest
from container_packing.largest_area_fit_first_packager import LargestAreaFitFirstPackager
from container_packing.dimension import Dimension
from container_packing.box_item import BoxItem
from container_packing.box import Box

def test_laff_packager_single_box():
    containers = [Dimension("C1", 10, 10, 10)]
    packager = LargestAreaFitFirstPackager(containers, rotate_3d=True, footprint_first=True)
    items = [BoxItem(Box("B1", 5, 5, 5), 1)]
    result = packager.pack(items)
    assert result is not None
    assert len(result.levels) > 0
    assert result.get_box_count() == 1

def test_laff_packager_multiple_boxes_fit():
    containers = [Dimension("C1", 10, 10, 10)]
    packager = LargestAreaFitFirstPackager(containers)
    items = [
        BoxItem(Box("B1", 3, 3, 3), 1),
        BoxItem(Box("B2", 3, 3, 3), 1),
        BoxItem(Box("B3", 3, 3, 3), 1)
    ]
    result = packager.pack(items)
    assert result is not None
    # Check how many boxes got placed
    assert result.get_box_count() == 3

def test_laff_packager_multiple_boxes_no_fit():
    containers = [Dimension("C1", 6, 6, 6)]
    packager = LargestAreaFitFirstPackager(containers)
    items = [
        BoxItem(Box("B1", 6, 6, 6), 1),
        BoxItem(Box("B2", 3, 3, 4), 1),
    ]
    # The second box won't fit after the first is placed, 
    # because container is exactly 6x6x6 for each dimension
    result = packager.pack(items)

    assert result is None

def test_multiple_boxes_somewhat_tight_fit():
    """
    Multiple boxes that fit snugly if oriented correctly.
    LAFF should pick largest footprint first and attempt to place them.
    """
    containers = [Dimension("ContainerB", 10, 10, 10)]
    packager = LargestAreaFitFirstPackager(
        containers,
        rotate_3d=True,
        footprint_first=True
    )

    items = [
        BoxItem(Box("Box1", 5, 5, 5), 1),
        BoxItem(Box("Box2", 5, 5, 5), 1),
        BoxItem(Box("Box3", 10, 5, 5), 1)  # This one has a 10x5 footprint
    ]
    result = packager.pack(items)
    if result is not None:
        # We expect that all can fit side by side on the bottom
        assert result.get_box_count() == 3
        assert len(result.get_levels()) == 1
    else:
        pytest.fail("Expected a snug fit, but packing returned None.")

def test_time_based_deadline_for_large_number_of_boxes():
    """
    Provide a short deadline for a large set of boxes to test 
    if the LAFF packager bails out early (returns None or partial) if time is exceeded.
    
    Note: This test might need to be adjusted based on your actual time-check logic
    and how quickly your system can handle it.
    """
    containers = [Dimension("BigContainer", 1_000, 1_000, 1_000)]
    packager = LargestAreaFitFirstPackager(
        containers, 
        rotate_3d=True, 
        footprint_first=True,
        binary_search=True
    )

    # Let's create many boxes. The code is likely to take a bit but not too long.
    # We'll impose a very short deadline to see if it times out.
    items = [BoxItem(Box(f"Box_{i}", 2, 2, 2), 1) for i in range(10_000)]

    import time
    short_deadline = round(time.time() * 1000) + 1  # 1 ms from now
    result = packager.pack(items, short_deadline)

    # The LAFF code uses `current_time_in_ms()` checks.
    # If it can't place them all within the deadline, we expect None.
    if result is not None and result.get_box_count() == len(items):
        pytest.fail("Expected time-based packing to fail or partially abort, but it succeeded.")
    else:
        # We confirm that it's None because the time likely expired.
        assert result is None, "Expected None due to time constraint."