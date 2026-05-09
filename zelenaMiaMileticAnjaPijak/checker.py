"""
Checker for Strong Bin Covering.
Usage: python checker.py <input_file> <output_file>

Exit code 0 = valid solution, prints number of covered bins.
Exit code 1 = invalid solution, prints error.
"""
import sys

EPS = 1e-9

def check(input_file, output_file):
    with open(input_file) as f:
        lines = f.read().split()
    n = int(lines[0])
    items = [float(lines[i+1]) for i in range(n)]

    with open(output_file) as f:
        out_lines = f.read().split('\n')
    out_lines = [l.strip() for l in out_lines if l.strip()]
    k = int(out_lines[0])

    used = set()
    bins = []
    for i in range(1, k+1):
        indices = list(map(int, out_lines[i].split()))
        for idx in indices:
            if idx < 1 or idx > n:
                print(f"ERROR: item index {idx} out of range [1,{n}]")
                sys.exit(1)
            if idx in used:
                print(f"ERROR: item {idx} used more than once")
                sys.exit(1)
            used.add(idx)
        total = sum(items[idx-1] for idx in indices)
        if total < 1 - EPS:
            print(f"ERROR: bin {i} sum={total:.6f} < 1 (not covered)")
            sys.exit(1)
        bins.append((indices, total))

    print(f"OK: {k} valid covered bins, {n - len(used)} items unused")
    sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python checker.py <input_file> <output_file>")
        sys.exit(2)
    check(sys.argv[1], sys.argv[2])
