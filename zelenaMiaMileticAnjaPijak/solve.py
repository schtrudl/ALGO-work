import sys
import random

EPS = 1e-9

def solve(items):
    open_bins = []
    covered = []

    for i, size in enumerate(items):
        idx = i + 1
        cover_candidate = None
        cover_waste = float('inf')
        best_bin = None
        best_sum = -1

        for b in open_bins:
            s = b[0]
            new_sum = s + size
            if new_sum >= 1 - EPS:
                waste = new_sum - 1
                if waste < cover_waste:
                    cover_waste = waste
                    cover_candidate = b
            else:
                if s > best_sum:
                    best_sum = s
                    best_bin = b

        if cover_candidate:
            cover_candidate[0] += size
            cover_candidate[1].append(idx)
            open_bins.remove(cover_candidate)
            covered.append(cover_candidate[1])
            continue

        if size > 0.5:
            smallest = None
            smallest_sum = float('inf')
            for b in open_bins:
                if b[0] < smallest_sum:
                    smallest_sum = b[0]
                    smallest = b
            if smallest:
                smallest[0] += size
                smallest[1].append(idx)
                continue

        if best_bin:
            best_bin[0] += size
            best_bin[1].append(idx)
        else:
            open_bins.append([size, [idx]])

    return covered


def run_solver(filename="input.txt", outputfile="output.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.read().split()
    n = int(lines[0])
    items = [float(lines[i+1]) for i in range(n)]
    covered_bins = solve(items)
    with open(outputfile, "w", encoding="utf-8") as f:
        f.write(f"{len(covered_bins)}\n")
        for b in covered_bins:
            f.write(" ".join(map(str, b)) + "\n")
    print(f"Solved: {len(covered_bins)} covered bins. Output -> {outputfile}")


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
    out = sys.argv[2] if len(sys.argv) > 2 else "output.txt"
    run_solver(inp, out)
