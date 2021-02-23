import os
import logging
import array
from typing import Tuple, AnyStr
from itertools import repeat
import math

log_level = os.getenv("LOG_LEVEL", "INFO")
log_level = {"INFO": logging.INFO, "DEBUG": logging.DEBUG}.get(log_level)

LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)3s - %(funcName)25s() ] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(log_level)


def swap(arr, i, j):
    _temp = arr[i]
    arr[i] = arr[j]
    arr[j] = _temp
    LOGGER.debug(f"{arr} \t swapped i={i}<-->j={j}: ")


def partition(arr: array.ArrayType, l: int, r: int) -> Tuple[int, int]:
    p = arr[l]
    i = l + 1
    for j in range(l + 1, r + 1):
        if arr[j] < p:
            # swap i and j index
            swap(arr, i, j)
            i += 1
    # final pivot swap
    swap(arr, l, i - 1)

    return r - l, i - 1


def quicksort_and_count(arr: array.ArrayType, start: int, stop: int) -> int:
    LOGGER.debug(f"{arr} \t start: {str(start):2s} \t stop: {str(stop):2s} \t  subarr: {arr[start:stop+1]}")#\t arr id: {id(arr)}")
    if stop-start <= 1:
        return 0
    m_p, i_p = partition(arr, start, stop)
    # sort first part
    LOGGER.debug(f"{arr} \t Partition done: pivot={arr[i_p]} i_p={i_p} m_p={m_p} ")
    # LOGGER.debug(f"Partition returned: m_p={m_p}, i_p={i_p}")
    m_1 = quicksort_and_count(arr, start=start, stop=i_p)
    m_2 = quicksort_and_count(arr, start=i_p + 1, stop=stop)
    # LOGGER.debug(f" m_p + m_1 + m_2 = {m_p}+{m_1}+{m_2}={m_p + m_1 + m_2}")
    return m_p + m_1 + m_2


if __name__ == "__main__":
    from pathlib import Path
    from ast import literal_eval
    import argparse

    parser = argparse.ArgumentParser(
        prog="Number of comparisons in quicksort",
    )
    parser.add_argument("--spec", help="", default="(4, 5, 2, 3, 1)")
    # parser.add_argument("--spec", help="", default="(3, 2, 0, 4, 1, 7, 6, 5)")
    args = parser.parse_args()

    if Path(args.spec).exists():
        numbers = Path(args.spec).read_text().splitlines()
    else:
        numbers = literal_eval(args.spec)

    LOGGER.info(f"Found {len(numbers)} numbers in array")

    arr = array.array("I", map(int, numbers))

    LOGGER.debug(str(arr) + " <-- original")
    LOGGER.info(quicksort_and_count(arr, 0, len(arr) - 1))
    LOGGER.debug(str(arr) + " <-- sorted")
