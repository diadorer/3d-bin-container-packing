import pytest
from container_packing.box import Box
from container_packing.dimension import Dimension

def test_box_init():
    box = Box("test_box", 10, 20, 30)
    assert box.name == "test_box"
    assert box.width == 10
    assert box.depth == 20
    assert box.height == 30
    assert box.volume == 10 * 20 * 30

def test_box_rotate_3d():
    box = Box("test_box", 1, 2, 3)
    box.rotate_3d()
    # Original: w=1, d=2, h=3
    # After rotate_3d: height=old_width=1, width=old_depth=2, depth=old_height=3
    assert (box.width, box.depth, box.height) == (2, 3, 1)

def test_box_rotate_2d():
    box = Box("test_box", 3, 4, 5)
    box.rotate_2d()
    # Original: w=3, d=4, h=5
    # After 2D rotation: depth=3, width=4, height stays the same
    assert (box.width, box.depth, box.height) == (4, 3, 5)

def test_box_clone():
    box1 = Box("box", 10, 20, 30)
    box2 = box1.clone()
    assert box1.name == box2.name
    assert box1.width == box2.width
    assert box1.depth == box2.depth
    assert box1.height == box2.height
    assert box1 is not box2  # different instances
