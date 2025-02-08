# 3D Bin Container Packing

**3D Bin Container Packing** solves the NP-hard 3D box packing problem using heuristic methods. It leverages the **Largest Area Fit First (LAFF) algorithm** to optimize container space efficiently—ideal for logistics, warehousing, and shipping.

<a href="https://pypi.org/project/container_packing" target="_blank">
    <img src="https://img.shields.io/pypi/v/container_packing?color=%2334D058&label=pypi%20package" alt="Package version">
</a>


## Installation

You can install it via pip:

<div class="termy">

```console
$ pip install container_packing

---> 100%
```

</div>


## Usage

Use the shortcut `pack_products_into_restrictions` to pack boxes:

```Python
from container_packing.shortcuts import pack_products_into_restrictions


boxes = [{
  'x': 10,
  'y': 20,
  'z': 30,
  'quantity': 2
}, {
  'x': 20,
  'y': 30,
  'z': 50,
  'quantity': 4
}]

container_max_sizes = (60, 60, 70)

container_x, container_y, container_z = pack_products_into_restrictions(
    boxes,
    container_max_sizes
)
```

## Largest Area Fit First Algorithm

The LAFF algorithm is a heuristic that optimizes box packing by always targeting the largest available free area in the container. It works as follows:

* **Identify Free Areas**: Continuously track and update the container’s largest contiguous free spaces.
* **Evaluate Candidates**: For each box, check all valid orientations and potential placements within these spaces.
* **Score and Select**: Assign scores based on how well a placement utilizes the free area and choose the best candidate.
* **Update and Repeat**: After placing a box, recalculate free spaces and repeat until all boxes are placed or no valid placements remain.

This approach minimizes wasted space by filling the largest gaps first, providing efficient and robust packing even when box sizes and shapes vary.

