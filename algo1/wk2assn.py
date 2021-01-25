import array


def count_split_inv(x: array.ArrayType) -> tuple:
    raise NotImplementedError


def sort_and_count(x: array.ArrayType) -> tuple:
    n = len(x)
    if n == 1:
        return 0
    b, x = sort_and_count(x[: n // 2])
    c, y = sort_and_count(x[n // 2 :])
    d, z = count_split_inv(a)
    return sum((x, y, z))


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
    parser.add_argument("spec", help="", default="(1, 2, 4, 3)")
    args = parser.parse_args()

    try:
        p = Path(args.spec)
        assert p.exists()
        numbers = p.read_text().splitlines()
    except AssertionError:
        numbers = literal_eval(args.spec)

    print(f"Found {len(numbers)} numbers")

    print(num_inversions(numbers))