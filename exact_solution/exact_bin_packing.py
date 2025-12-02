# exact_bin_packing.py
import time, random, math, csv, os
from functools import lru_cache

class ExactBinPacking:
    def __init__(self, capacity):
        self.capacity = capacity
        self.best_bins = None
        self.best_k = float('inf')

    def ffd_upper_bound(self, items):
        # First-fit decreasing heuristic to get initial upper bound
        bins = []
        for x in items:
            placed = False
            for i in range(len(bins)):
                if bins[i] + x <= self.capacity:
                    bins[i] += x
                    placed = True
                    break
            if not placed:
                bins.append(x)
        return len(bins)

    def lower_bound(self, items, start_index=0):
        # Simple LB: ceil(sum(remaining)/capacity)
        s = sum(items[start_index:])
        return math.ceil(s / self.capacity)

    def solve(self, items, time_limit=None):
        # items are assumed sorted descending
        self.best_k = self.ffd_upper_bound(items)
        self.best_bins = None
        start_time = time.time()
        n = len(items)

        def dfs(index, bins):
            nonlocal start_time
            if time_limit and (time.time() - start_time) > time_limit:
                raise TimeoutError("Time limit exceeded")

            if index == n:
                k = len(bins)
                if k < self.best_k:
                    self.best_k = k
                    self.best_bins = bins.copy()
                return

            if len(bins) >= self.best_k:
                return

            lb = len(bins) + self.lower_bound(items, index)
            if lb >= self.best_k:
                return

            x = items[index]
            # try existing bins
            seen_new_bin = False
            for i in range(len(bins)):
                if bins[i] + x <= self.capacity:
                    bins[i] += x
                    dfs(index + 1, bins)
                    bins[i] -= x
            # open a new bin (symmetry: only try opening one new bin option)
            bins.append(x)
            dfs(index + 1, bins)
            bins.pop()

        try:
            dfs(0, [])
        except TimeoutError:
            pass

        return self.best_k, self.best_bins, time.time() - start_time

# Test case generator and runner (driver)
def generate_test_cases(num_cases=60, n_min=8, n_max=22, capacity=100, seed=12345):
    random.seed(seed)
    cases = []
    for i in range(num_cases):
        n = random.randint(n_min, n_max)
        if random.random() < 0.6:
            items = [random.randint(1, capacity) for _ in range(n)]
        else:
            items = [random.randint(int(0.5*capacity), capacity) for _ in range(max(1, n//6))]
            items += [random.randint(1, int(0.5*capacity)) for _ in range(n - len(items))]
            random.shuffle(items)
        items = [min(x, capacity) for x in items]
        cases.append((f"case_{i+1:03d}", n, capacity, items))
    return cases

def run_cases(cases, time_limit_per_case=30.0, out_dir='results'):
    os.makedirs(out_dir, exist_ok=True)
    results = []
    for case_id, n, capacity, items in cases:
        items_sorted = sorted(items, reverse=True)
        solver = ExactBinPacking(capacity)
        try:
            k, bins, t = solver.solve(items_sorted, time_limit=time_limit_per_case)
            timeout = False
        except Exception:
            k, bins, t = None, None, time_limit_per_case
            timeout = True
        results.append({
            "case_id": case_id,
            "n_items": n,
            "capacity": capacity,
            "optimal_bins": k,
            "time_sec": t,
            "timeout": timeout,
            "items": items
        })
        print(f"Ran {case_id}: n={n}, time={t:.3f}s, optimal_bins={k}, timeout={timeout}")

    # write CSV
    csv_path = os.path.join(out_dir, "results.csv")
    with open(csv_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["case_id", "n_items", "capacity", "optimal_bins", "time_sec", "timeout"])
        for r in results:
            writer.writerow([r["case_id"], r["n_items"], r["capacity"], r["optimal_bins"], r["time_sec"], r["timeout"]])
    return results, csv_path

if __name__ == "__main__":
    cases = generate_test_cases(num_cases=60, n_min=8, n_max=22, capacity=100, seed=42)
    results, csv_path = run_cases(cases, time_limit_per_case=30.0, out_dir='binpacking_results')
    print("Wrote:", csv_path)
