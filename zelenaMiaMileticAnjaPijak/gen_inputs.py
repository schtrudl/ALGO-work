"""Generate sample input files for Strong Bin Covering."""
import random

def gen(n, filename, seed=42):
    random.seed(seed)
    items = [round(random.uniform(0.01, 1.0), 6) for _ in range(n)]
    with open(filename, "w") as f:
        f.write(f"{n}\n")
        for x in items:
            f.write(f"{x}\n")
    print(f"Written {filename} ({n} items)")

# gen(10,  "input10.txt",  seed=1)
# gen(100, "input100.txt", seed=2)
# gen(500, "input500.txt", seed=3)
# gen(600, "input600.txt", seed=3)
# gen(700, "input700.txt", seed=3)
# gen(50, "input50.txt", seed=3)
