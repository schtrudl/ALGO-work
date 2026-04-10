#!/usr/bin/env python3

# read from stdin, write to stdout

import sys
from typing import TextIO


def read_input(
    inn: TextIO,
) -> tuple[int, list[list[bool]], list[tuple[int, int]]]:
    """Read input from inn and return n, adjacency matrix and list of edges"""
    n = int(inn.readline().strip())
    nbhs = [[False] * n for _ in range(n)]
    for i in range(n):
        row = list(map(int, inn.readline().strip().split()))
        for j in range(n):
            nbhs[i][j] = bool(row[j])

    edges = []
    for i in range(n):
        for j in range(n):
            if nbhs[i][j]:
                edges.append((i, j))

    return n, nbhs, edges


def is_valid_pair(
    nbhs: list[list[bool]],
    vu1: tuple[int, int],
    vu2: tuple[int, int],
) -> bool:
    v_1, u_1 = vu1
    v_2, u_2 = vu2
    return not (nbhs[u_1][u_2] or nbhs[u_1][v_2] or nbhs[v_1][u_2] or nbhs[v_1][v_2])


def is_valid(nbhs, vu1: tuple[int, int], current: list[tuple[int, int]]):
    """Check if edge is independent (orthogonal) from all edges in current set"""
    for vu2 in current:
        if not is_valid_pair(nbhs, vu1, vu2) and not is_valid_pair(nbhs, vu2, vu1):
            return False
    return True


def print_best(best: list[tuple[int, int]]):
    print(len(best))
    for x, y in best:
        print(x + 1, y + 1)


best_edges: set[frozenset[tuple[int, int]]] = set()


def mach(
    edges: list[tuple[int, int]],
    nbhs: list[list[bool]],
    edge_idx: int,
    current_edges: list[tuple[int, int]],
    target: int | None = None,
) -> list[tuple[int, int]]:
    if target is not None and len(current_edges) == target:
        best_edges.add(frozenset(current_edges))
    if edge_idx == len(edges):
        return current_edges

    edge = edges[edge_idx]

    best = current_edges

    if is_valid(nbhs, edge, current_edges):
        wi = mach(edges, nbhs, edge_idx + 1, current_edges + [edge], target)
        if len(wi) > len(best):
            best = wi

    wo = mach(edges, nbhs, edge_idx + 1, current_edges, target)
    if len(wo) > len(best):
        best = wo

    return best


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Find the maximum independent set of edges"
    )
    parser.add_argument(
        "--all", help="Return all velid solutions of maximum size", action="store_true"
    )
    args = parser.parse_args()
    n, nbhs, edges = read_input(sys.stdin)
    best = mach(edges, nbhs, 0, [])
    if not args.all:
        print_best(best)
    else:
        # print all possible solutions
        mach(edges, nbhs, 0, [], target=len(best))
        for set in best_edges:
            print_best(list(set))
