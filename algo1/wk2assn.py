import logging
import array

LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)25s() ] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(logging.DEBUG)


def merge_and_count_splits(arr1, arr2):
    LOGGER.debug(f"arr1 : {arr1}")
    LOGGER.debug(f"arr2 : {arr2}")
    arr1_l = len(arr1)
    arr2_l = len(arr2)
    n = sum((arr1_l, arr2_l))
    i, j, invs = 0, 0, 0
    arr_sorted = array.array("I", [0] * n)

    for k in range(n):
        # end case 1: no more items in arr1, append all remaining items in arr2
        if i >= arr1_l:
            arr_sorted[k:] = arr2[j:]
            break
        # end case 2: no more items in arr2
        if j >= arr2_l:
            arr_sorted[k:] = arr1[i:]
            invs += n - i
            break

        l, r = arr1[i], arr2[j]
        if l < r:
            arr_sorted[k] = l
            i += 1
        else:
            arr_sorted[k] = r
            j += 1
            invs += 1
    return arr_sorted, invs


def count_split_inv(x: array.ArrayType) -> tuple:
    raise NotImplementedError


def sort_and_count(x: array.ArrayType) -> tuple:
    LOGGER.debug(f"x    : {type(x)} --> {x}")
    n = len(x)
    if n <= 1:
        return x, 0
    xl = x[: n // 2]
    xr = x[n // 2 :]
    b, x = sort_and_count(xl)
    c, y = sort_and_count(xr)
    d, z = merge_and_count_splits(b, c)
    return d, sum((x, y, z))


def num_inversions(x) -> int:
    x = array.array("b", x)
    if len(x) < 2:
        return 0
    return None


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

    LOGGER.info(sort_and_count(x=array.array("I", numbers)))
