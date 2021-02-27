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
        LOGGER.debug(f"{arr} \t| Placing pivot {p: >3d} at pos {i - 1} ({p-1})")
    swap(arr, l, i - 1)
    return r - l, i - 1


def quicksort_and_count_first(arr: array.ArrayType, start: int, stop: int) -> int:
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Quicksort: arr[{start:>2}:{stop+1: <2}] --> \t| {list(arr[start:stop+1])}"
        )
    if stop - start < 1:
        return 0

    m_p, i_p = partition(arr, start, stop)

    # sort first part
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Partition done:\t| pivot={arr[i_p]} i_p={i_p} m_p={m_p} "
        )
    m_1 = quicksort_and_count_first(arr, start=start, stop=i_p - 1)
    m_2 = quicksort_and_count_first(arr, start=i_p + 1, stop=stop)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f" m_p + m_1 + m_2 = {m_p}+{m_1}+{m_2}={m_p + m_1 + m_2}")
    return m_p + m_1 + m_2


def quicksort_and_count_last(arr: array.ArrayType, start: int, stop: int) -> int:
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Quicksort: arr[{start:>2}:{stop+1: <2}] --> \t| {list(arr[start:stop+1])}"
        )
    if stop - start < 1:
        return 0

    swap(arr, start, stop)
    m_p, i_p = partition(arr, start, stop)

    # sort first part
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Partition done:\t| pivot={arr[i_p]} i_p={i_p} m_p={m_p} "
        )
    m_1 = quicksort_and_count_last(arr, start=start, stop=i_p - 1)
    m_2 = quicksort_and_count_last(arr, start=i_p + 1, stop=stop)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f" m_p + m_1 + m_2 = {m_p}+{m_1}+{m_2}={m_p + m_1 + m_2}")
    return m_p + m_1 + m_2


def get_piv_idx_med(arr, start, stop):
    # idx_mid = start + round((stop - start) / 2 )
    if stop - start % 2 == 1:  # even length array,
        # LOGGER.debug("Even length array")
        idx_mid = int(start + (stop - start + 1) / 2)
    else:  # odd length array
        # LOGGER.debug("Odd  length array")
        idx_mid = int(start + (stop - start) / 2)

    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Pivot cands: 1: arr[{start}, {idx_mid}, {stop}] "  # = {arr[start]}, {arr[idx_mid]}, {arr[stop]} "
        )

    if idx_mid in (start, stop):
        return idx_mid

    median_array = sorted([ (arr[start], start), (arr[idx_mid], idx_mid), (arr[stop], stop)])

    return median_array[1][1]

    # _t = arr[start], arr[stop], arr[idx_mid]
    # for idx in start, stop, idx_mid:
    #     if arr[idx] < max(_t) and arr[idx] > min(_t):
    #         return idx


def quicksort_and_count_med(arr: array.ArrayType, start: int, stop: int) -> int:
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Quicksort: arr[{start:>2}:{stop+1: <2}] --> \t| {list(arr[start:stop+1])}"
        )
    if stop - start < 1:
        return 0

    # set pivot (1st el) as median of right left and middle element
    _idx_piv = get_piv_idx_med(arr, start, stop)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"{arr} \t| Pivot el arr[{_idx_piv}]={arr[_idx_piv]}")
    swap(arr, start, _idx_piv)

    m_p, i_p = partition(arr, start, stop)

    # sort first part
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Partition done:\t| pivot={arr[i_p]} i_p={i_p} m_p={m_p} "
        )
    m_1 = quicksort_and_count_med(arr, start=start, stop=i_p - 1)
    m_2 = quicksort_and_count_med(arr, start=i_p + 1, stop=stop)
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(
            f"{arr} \t| Quicksort: arr[{start:>2}:{stop+1: <2}] -->  \t| m_p + m_1 + m_2 = {m_p}+{m_1}+{m_2}={m_p + m_1 + m_2}"
        )
    return m_p + m_1 + m_2


if __name__ == "__main__":
    from pathlib import Path
    from ast import literal_eval
    import argparse
    import sys
    from copy import deepcopy
    sys.setrecursionlimit(10000000) # TODO: comment away ifneed

    LOGGER.critical("Recursion limit:  " + str(sys.getrecursionlimit()))


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
    ans_first = quicksort_and_count_first(deepcopy(arr), start=0, stop=len(arr) - 1)
    ans_last = quicksort_and_count_last(deepcopy(arr), start=0, stop=len(arr) - 1)
    ans_med = quicksort_and_count_med(deepcopy(arr), start=0, stop=len(arr) - 1)

    LOGGER.critical("ANSWER:")
    LOGGER.critical(f"FIRST : {ans_first}")
    LOGGER.critical(f"LAST  : {ans_last}")
    LOGGER.critical(f"MEDIAN: {ans_med}")

