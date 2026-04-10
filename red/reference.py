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
        for j in range(i + 1, n):
            if nbhs[i][j]:
                edges.append((i, j))

    return n, nbhs, edges


def is_valid(nbhs, vu: tuple[int, int], current: list[tuple[int, int]]):
    """Check if edge is independent (orthogonal) from all edges in current set"""
    v_1, u_1 = vu
    for v_2, u_2 in current:
        if nbhs[u_1][u_2] or nbhs[u_1][v_2] or nbhs[v_1][u_2] or nbhs[v_1][v_2]:
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
    n, nbhs, edges = read_input(sys.stdin)
    best = mach(edges, nbhs, 0, [])
    print_best(best)
    # print all possible solutions
    # mach(edges, nbhs, 0, [], target=len(best))
    # for set in best_edges:
    #    print_best(list(set))
