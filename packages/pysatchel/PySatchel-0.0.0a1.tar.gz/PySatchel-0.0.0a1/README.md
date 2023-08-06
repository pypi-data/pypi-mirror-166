# Satchel

Satchel is a compendium of pure python functions to carry with you and get things done.

## Installation

```
pip install PySatchel
```

## Usage

```python
>>> import satchel.iterable import chunk

>>> some_list = [1, 2, 3, 4, 5]
>>> chunk(some_list, 2, "length", True)
# [[1, 2], [3, 4], [5]]

>>> chunk(some_list, 2, "count", True)
# [[1, 2, 3], [3, 5]]
```
