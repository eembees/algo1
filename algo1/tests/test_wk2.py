import pytest

from algo1.wk2assn import num_inversions


@pytest.mark.parametrize(
    "x,n_true",
    [
        ((1, 4, 3), 1),
        ((1, 2, 4, 3), 1),
        ((1, 2, 3, 5, 4), 1),
        ((1, 3, 2, 5, 4), 2),
        ((1, 2, 3, 5, 4, 6), 1),
        ((1, 2, 5, 3, 4, 6), 2),
        ((1, 3, 5, 2, 4, 6), 3),
        ((6, 5, 4, 3, 2, 1), 15),
        ((6, 5, 4, 3, 2, 1, 7), 15),
        ((6, 5, 4, 3, 2, 1, 8, 7), 16),
        ((1,), 0),
        # (tuple(), 0),
    ],
)
def test_inversions(x, n_true):
    n_pred = num_inversions(x)
    assert n_pred == n_true