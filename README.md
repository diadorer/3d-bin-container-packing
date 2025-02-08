# 3d-bin-container-packing
A variant of the Largest Area Fit First (LAFF) algorithm

This library is imlementation of [this library](https://github.com/skjolber/3d-bin-container-packing) using python.

<a href="https://pypi.org/project/container_packing" target="_blank">
    <img src="https://img.shields.io/pypi/v/container_packing?color=%2334D058&label=pypi%20package" alt="Package version">
</a>

## Installation

You can install it via pip:

``pip install container_packing``

## Usage

You can use shortcut `pack_products_into_restrictions`. It will pack your boxes info given restictions.

```
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

conataner_max_sizes = (60, 60, 70)

container_x, container_y, container_z = pack_products_into_restrictions(
    boxes,
    conataner_max_sizes
)
```


