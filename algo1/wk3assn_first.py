import os
import logging
import array
from typing import Tuple, AnyStr
from itertools import repeat
import math

log_level = os.getenv("LOG_LEVEL", "INFO")  # TODO: make fix wrt this in some nice way
log_level = {
    "CRITICAL": logging.CRITICAL,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}.get(log_level)

LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)3s - %(funcName)25s() ] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(log_level)


def swap(arr, i, j):
    if i != j:
        _temp = arr[i]
        arr[i] = arr[j]
        arr[j] = _temp
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                f"{arr} \t| swapped arr[{i}]={arr[j]} <--> arr[{j}]={arr[i]}: "
            )


def partition(arr: array.ArrayType, l: int, r: int) -> Tuple[int, int]:
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"{arr} \t| l={l}, r={r} \t\t| size of subarr: {str(r-l):2s}")
    p = arr[l]
    i = l + 1
    for j in range(l + 1, r + 1):
        if arr[j] < p:
            # swap i and j index
            swap(arr, i, j)
            i += 1
    # final pivot swap
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"{arr} \t| Before placing pivot at pos {i - 1}")
    swap(arr, l, i - 1)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"{arr} \t| After  placing pivot at pos {i - 1}")
    return r - l, i - 1


def quicksort_and_count(arr: array.ArrayType, start: int, stop: int) -> int:
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Idxs: arr[{start:>2}:{stop+1: <2}] --> \t| {list(arr[start:stop+1])}"
        )  # \t arr id: {id(arr)}")
    if stop - start < 1:
        return 0

    m_p, i_p = partition(arr, start, stop)

    # sort first part
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Partition done:\t| pivot={arr[i_p]} i_p={i_p} m_p={m_p} "
        )
    m_1 = quicksort_and_count(arr, start=start, stop=i_p - 1)
    m_2 = quicksort_and_count(arr, start=i_p + 1, stop=stop)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f" m_p + m_1 + m_2 = {m_p}+{m_1}+{m_2}={m_p + m_1 + m_2}")
    return m_p + m_1 + m_2


if __name__ == "__main__":
    from pathlib import Path
    from ast import literal_eval
    import argparse

    parser = argparse.ArgumentParser(
        prog="Number of comparisons in quicksort",
    )
    parser.add_argument("--spec", help="", default="(4, 5, 2, 3, 1)")  # should give 7
    # parser.add_argument("--spec", help="", default="(3, 2, 0, 4, 1, 7, 6, 5)")
    args = parser.parse_args()

    if Path(args.spec).exists():
        numbers = Path(args.spec).read_text().splitlines()
    else:
        numbers = literal_eval(args.spec)

    LOGGER.info(f"Found {len(numbers)} numbers in array")

    arr = array.array("I", map(int, numbers))

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(str(arr) + " <-- original")
    ans = quicksort_and_count(arr, start=0, stop=len(arr) - 1)
    LOGGER.info(ans)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(str(arr) + " <-- sorted")
    print(ans)