import sys
import os
import logging
import array
from typing import Tuple, AnyStr, List
from itertools import repeat
import math
from pathlib import Path
from ast import literal_eval
import argparse
from copy import deepcopy
from operator import itemgetter, iconcat
import functools
import random

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


class Graph:
    """Simple Undirected Graph Class"""

    def __init__(self, edges=None, nodes=None):
        self.nodes: List[int] = nodes if nodes is not None else []
        self.edges: List[Tuple[int, int]] = edges if edges is not None else []

        self.edges = list(map(tuple, map(sorted, self.edges)))

    def get_n(self) -> int:
        return len(self.nodes)

    def get_m(self) -> int:
        return len(self.edges)

    def merge(self, edge: Tuple[int, int]) -> int:
        """Merges two vertices from an edge

        Args:
            edge (tuple): Edge to merge

        Returns:
            int: Number of self-loops squashed
        """
        # lower index first, to make sure we keep track of the right thing
        node_keep, node_remove = tuple(sorted(edge))
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"KEEPING: {node_keep}")
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"REMOVE : {node_remove}")
        # remove the higher index node
        self.nodes.remove(node_remove)

        # remap all edges that contain the end index to the start index
        edges_to_remap = list(filter(lambda x: node_remove in x, self.edges))
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"edges to remap: {edges_to_remap} ")
        _ = [self.edges.remove(el) for el in edges_to_remap]

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(
                f"nodes to remap: {functools.reduce(iconcat, map(list,edges_to_remap), [])} "
            )

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"GRAPH EDGES: {self.edges}")
        nodes_to_remap = list(
            filter(
                lambda el: el not in edge,
                functools.reduce(iconcat, edges_to_remap, []),
            )
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"nodes to remap: {nodes_to_remap} ")

        # add new edges
        edges_remapped = [tuple(sorted((nd, node_keep))) for nd in nodes_to_remap]

        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"NEW   EDGES: {edges_remapped}")

        self.edges.extend(edges_remapped)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"GRAPH EDGES: {self.edges}")

    def merge_random(self, seed=1):
        idx = random.randint(0, len(self.edges) - 1)
        edge = self.edges.pop(idx)
        return self.merge(edge)


def load_graph(p: Path) -> Graph:
    lines = p.read_text().splitlines()
    nodes = []
    edges = set()
    for line in lines:
        _line = list(map(int, line.split()))
        _node = _line[0]
        _edges = _line[1:]
        _edges = list(map(lambda edg: tuple(sorted((_node, edg))), _edges))
        nodes.append(_node)
        edges.update(_edges)
        if LOGGER.isEnabledFor(logging.DEBUG):
            LOGGER.debug(f"Node {_node} --> Edges: {list(_edges)}")

    return Graph(edges=edges, nodes=nodes)


def main(p:Path)-> int:
    g = load_graph(p)
    n = g.get_n()
    # number_of_trials = 2
    number_of_trials = n#int(n ** 2 * math.log(n))
    LOGGER.info(f"Number of trials: {number_of_trials}")
    LOGGER.debug(f"GRAPH NODES: {g.get_n()}")
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"GRAPH NODES: {g.nodes}")
    LOGGER.debug(f"GRAPH EDGES: {g.get_m()}")
    if LOGGER.isEnabledFor(logging.DEBUG):
        LOGGER.debug(f"GRAPH EDGES: {g.edges}")

    results = []
    for _trial_n in range(number_of_trials):
        _g = deepcopy(g)
        while _g.get_n() > 2:
            _g.merge_random(seed=_g.get_n())
        results.append(_g.get_m())
    return min(results)

if __name__ == "__main__":
    from copy import deepcopy
    import math

    parser = argparse.ArgumentParser(
        prog="Number of comparisons in quicksort",
    )
    parser.add_argument("--spec", help="", default="invalid /path/ this doesn't exist")  # should give 7
    args = parser.parse_args()

    if Path(args.spec).exists():
        p = Path(args.spec)
    else:
        p: Path = (
        Path(__file__).absolute().parents[2]
        / "stanford-algs/testCases/course1/assignment4MinCut/input_random_1_6.txt"
        )


    min_cut = main(p)
    LOGGER.critical(f"Minimum cut: {min_cut}")
