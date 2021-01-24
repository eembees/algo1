# integer multiplication kats. algorithm
def karatsuba(x: str, y: str) -> int:
    # new cases: 0 leading string
    # base case
    if len(x) == 1 or len(y) == 1:
        return int(x) * int(y)

    # 0. find a,b,c,d
    ndiv2 = max(len(x), len(y)) // 2

    a, b = x[:-ndiv2], x[-ndiv2:]
    c, d = y[:-ndiv2], x[-ndiv2:]

    # 1. multiply ac
    ac = karatsuba(a, c)
    # 2. compute bd
    bd = karatsuba(b, d)
    # 3. compute (a + b)(c + d)
    abcd = karatsuba(str(sum((int(a), int(b)))), str(sum((int(c), int(d)))))
    # 3.5 compute (ad + bc) = 3.-1.-2.
    adbc = abcd - ac - bd
    # 4. return 10^n ac + 10^(n/2)(ad+bc) + bd

    return 10 ** (ndiv2 * 2) * ac + 10 ** ndiv2 * adbc + bd


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        prog="Karatsuba Multiplication",
    )
    parser.add_argument("x", help="1st number", default="10")
    parser.add_argument("y", help="2nd number", default="21")
    args = parser.parse_args()

    print(karatsuba(args.x, args.y))
