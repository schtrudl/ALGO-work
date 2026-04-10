#!/usr/bin/env python3

import argparse
import sys

from reference import is_valid, mach, read_input

parser = argparse.ArgumentParser(description="Verify the integrity of the solution")
parser.add_argument("input", help="Path to the input file of the problem (usually .in)")
parser.add_argument(
    "solution", help="Path to the solution file to verify (usually .out)"
)
args = parser.parse_args()


# Read input file
with open(args.input, "r") as f:
    global n, nbhs, edges
    n, nbhs, edges = read_input(f)


# Read solution file
with open(args.solution, "r") as f:
    num_pairs = int(f.readline().strip())
    pairs = []
    for _ in range(num_pairs):
        x, y = map(int, f.readline().strip().split())
        pairs.append((x - 1, y - 1))  # Convert to 0-indexed

# Verify the solution
errors = []

# Check 1: Each pair must be an edge in the graph
for i, (x, y) in enumerate(pairs):
    if (x, y) not in edges:
        errors.append(f"({x + 1}, {y + 1}) is not an edge in the graph!")

# Check 2: No two pairs share a common neighbor
for i, (x1, y1) in enumerate(pairs):
    for j, (x2, y2) in enumerate(pairs):
        if i == j:
            continue
        # Check if any vertex from pair i is a neighbor of any vertex from pair j
        if not is_valid(nbhs, (x1, y1), [(x2, y2)]):
            errors.append(
                f"Pairs ({x1 + 1}, {y1 + 1}) and ({x2 + 1}, {y2 + 1}) share a common neighbor"
            )

# Check 3: The set is maximal

best_n = mach(edges, nbhs, 0, [])
if len(pairs) < len(best_n):
    errors.append(
        f"The set of pairs is not maximal! Found a larger independent set of size {len(best_n)}"
    )

# Report results
if errors:
    print("INVALID SOLUTION:")
    for err in errors:
        print(f"  - {err}")
    sys.exit(1)
else:
    print(f"OK")
    sys.exit(0)
