import os
import sys
import logging
import array
from pathlib import Path
import pytest
from operator import itemgetter
import context


from algo1.wk3assn_first import quicksort_and_count

log_level = {
    "CRITICAL": logging.CRITICAL,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}.get(
    os.getenv("LOG_LEVEL", "INFO")
)  # TODO: make fix wrt this in some nice way)

LOGGER = logging.getLogger(__name__)
FORMAT = "[%(filename)s:%(lineno)3s - %(funcName)25s() ] %(message)s"
logging.basicConfig(format=FORMAT)
LOGGER.setLevel(log_level)


def load_test_cases(test_cases_path: Path):
    cases = []  # list of dicts
    for test_case_path in test_cases_path.glob("input_*.txt"):
        answer_path: Path = test_case_path.parent / test_case_path.name.replace(
            "input", "output"
        )
        length = int(answer_path.stem.split("_")[-1])

        answer = answer_path.read_text().splitlines()[0]

        LOGGER.debug(
            f"Found test case at: {str(test_case_path.name): <30s} with answer {str(answer) : <10s} and lenght {length: <10d}"
        )

        cases.append({"path": test_case_path, "answer": int(answer), "length": length})

    return cases


def test_wk3_first(path, answer):
    arr = array.array("I", map(int, path.read_text().splitlines()))
    LOGGER.info(f"Case: {str(test_case_path.name): <30s} | LEN: {len(arr)}")
    pred = quicksort_and_count(arr, start=0, stop=len(arr) - 1)

    LOGGER.info(
        f"Case: {str(test_case_path.name): <30s} | TRUE: {answer: >10d} | {pred: <10d} PRED | {'PASSED' if answer==pred else 'FAILED'}"
    )
    return answer == pred


if __name__ == "__main__":
    MAX_LEN = 100000
    test_case_path = (
        Path(__file__).absolute().parent.parent.parent.parent
        / "stanford-algs/testCases/course1/assignment3Quicksort"
    )
    cases = load_test_cases(test_case_path)
    LOGGER.info(f"Found {len(cases):>5d} test cases")
    results = [
        test_wk3_first(_p, _ans)
        for _p, _ans in map(
            itemgetter("path", "answer"),
            filter(
                lambda x: x.get("length") <= MAX_LEN,
                sorted(cases, key=itemgetter("length")),
            ),
        )
    ]
    LOGGER.info(
        f"PASS RATE: {sum(results): <5d}/{len(results): <5d} = {float(sum(results))/len(results):.0%}"
    )
