import os
import sys
import logging
import array
from pathlib import Path
import pytest
from operator import itemgetter

import context
from algo1.wk4assn import main


MAX_LEN = int(os.getenv("MAX_TEST_LEN", "100"))

log_level = {
    "CRITICAL": logging.CRITICAL,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG,
}.get(os.getenv("LOG_LEVEL", "INFO"))


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

        answer = int(answer_path.read_text())

        LOGGER.debug(
            f"Found test case at: {str(test_case_path.name): <30s} with answer {str(answer) : <10s} and length {length: <10d}"
        )

        cases.append({"path": test_case_path, "answer": answer, "length": length})

    return list(
        filter(
            lambda x: x.get("length") <= MAX_LEN,
            sorted(cases, key=itemgetter("length")),
        )
    )


def test_wk4_single(case) -> bool:
    ans = case.get("answer")
    pred = main(case.get("path"))

    LOGGER.info(
        f"Case: {str(case.get('path').name): <30s} | TRUE: {ans: >10d} | {pred: <10d} PRED | {'PASSED' if ans==pred else 'FAILED'}"
    )
    return ans == pred


def test_wk4_cases(cases):
    results = [test_wk4_single(case) for case in cases]
    LOGGER.critical(
        f"PASS RATE: {sum(results): <5d}/{len(results): <5d} = {float(sum(results))/len(results):.0%}"
    )


if __name__ == "__main__":
    test_case_path = (
        Path(__file__).absolute().parent.parent.parent.parent
        / "stanford-algs/testCases/course1/assignment4MinCut"
    )
    cases = load_test_cases(test_case_path)
    test_wk4_cases(cases)