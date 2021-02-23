import logging
import array
from typing import Tuple, AnyStr
from itertools import repeat


LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)25s() ] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.INFO)


def sort_and_count(arr: array.ArrayType, n: int) -> Tuple[array.ArrayType, int]:
    LOGGER.debug(f"N: {n:3d}   A: {arr} ")
    if n == 1:
        return arr, 0

    arr_l = arr[: n // 2]
    arr_r = arr[n // 2 :]
    b, x = sort_and_count(arr_l, n // 2)
    c, y = sort_and_count(arr_r, n - n // 2)
    d, z = merge_and_count_split(b, c)
    LOGGER.debug(f"X={x:2d} | Y={y:2d} | Z={z:2d}")
    return d, (x + y + z)


def merge_and_count_split(
    b: array.ArrayType, c: array.ArrayType
) -> Tuple[array.ArrayType, int]:
    d = array.array("I", repeat(0, len(b) + len(c)))
    LOGGER.debug(f"Initialized D with length {len(d)}")
    splits = 0
    i, j = 0, 0
    for k in range(len(d)):
        # edge case 1: empty b, add rest of cs and quit
        # No inverted elements remain
        if i >= len(b):
            LOGGER.debug(f"Edge case 1 for k={k}: rest of c: {c[j:]}")
            d[k:] = c[j:]
            break
        # edge case 2: empty c, add rest of bs and ADD number of bs to split
        # All remaining elements of b are inverted with ALL elements of c
        elif j >= len(c):
            LOGGER.debug(f"Edge case 2 for k={k}: rest of b: {b[i:]}")
            d[k:] = b[i:]
            break
        elif b[i] < c[j]:
            # everything normal. Increment i.
            d[k] = b[i]
            i += 1
        elif b[i] > c[j]:
            # inversion! c[j] is inverted with all elements left in b 
            LOGGER.debug(f"Found inversion: B[{i}]={b[i]} > C[{j}]={c[j]}")
            d[k] = c[j]
            splits += len(b[i:]) 
            j += 1

    assert len(d) == len(b) + len(c)
    LOGGER.debug(f"Returning splits={splits}, D: {d}")
    return d, splits


def num_inversions(arr: array.ArrayType) -> Tuple[array.ArrayType, int]:
    if not isinstance(arr, array.ArrayType):
        arr = array.array("I", arr)
    arr_sorted, n_invs = sort_and_count(arr, len(arr))
    return n_invs


if __name__ == "__main__":
    from pathlib import Path
    from ast import literal_eval
    import argparse

    parser = argparse.ArgumentParser(
        prog="Number of inversions",
    )
    parser.add_argument("--spec", help="", default="(1, 2, 4, 3)")
    args = parser.parse_args()

    if Path(args.spec).exists():
        p = Path(args.spec)
        assert p.exists()
        numbers = p.read_text().splitlines()
    else:
        numbers = literal_eval(args.spec)

    LOGGER.info(f"Found {len(numbers)} numbers")

    arr = array.array("I", map(int, numbers))

    LOGGER.info(num_inversions(arr))
    LOGGER.debug(str(arr) + " <-- original")
