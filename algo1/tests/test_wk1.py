import pytest

from algo1.wk1assn import karatsuba


@pytest.mark.parametrize(
    "x,y",
    [
        ("1", "2"),
        ("15", "6"),
        ("15", "10"),
        ("10", "21"),
        ("12", "11"),
        ("150", "862"),
        ("1000", "2563"),
        ("12346", "98765"),
        (
            "3141592653589793238462643383279502884197169399375105820974944592",
            "2718281828459045235360287471352662497757247093699959574966967627",
        ),
    ],
)
def test_karatsuba(x: str, y: str):
    real_ans = int(x) * int(y)
    kara_ans = karatsuba(x, y)
    assert real_ans == kara_ans
