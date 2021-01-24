import pytest

from algo1.wk1assn import karatsuba


@pytest.mark.parametrize(
    "x,y",
    [ 
        ("1","2"),
        ("15", "6"),
        ("10", "21"),
        ("12", "11"),
        ("150", "862"),
        ("1000", "2563"),
        ("12346", "98765"),
    ],
)
def test_karatsuba(x: str, y: str):
    assert karatsuba(x, y) == int(x) * int(y)
