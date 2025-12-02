Project: Exact Bin Packing (branch-and-bound)

1 Problem:
   Given items with sizes s1..sn and identical bins of capacity C,
   partition the items into the minimum number of bins.

   Practical applications: packing, container loading, memory allocation,
   scheduling tasks onto identical machines, cutting stock approximations.

2 Algorithm:
   - Sort items in descending order.
   - DFS placing each item into existing bins (if it fits) or open a new bin.
   - Prune using:
     * best-known solution (upper bound)
     * lower bound = ceil(sum(remaining)/capacity)
     * initial upper bound from First-Fit Decreasing (FFD)
     * symmetry avoidance when opening new bin

   Worst-case running time: exponential in n (roughly O(b^n) for branching factor b).
   Practical runtime depends heavily on item sizes and ordering.

3 Files:
   - exact_bin_packing.py  (source)
   - binpacking_results/   (place where results.csv and plot are saved)
   - run_test_cases.sh     (example shell script below)
   - presentation.pdf      (your slides)

4 Example command-line:
   python exact_bin_packing.py
   (the script runs a built-in generator and writes results to ./binpacking_results/results.csv)

5 Running longer tests:
   - Modify generate_test_cases (increase n_max -> e.g., 30 or 34).
   - Increase time_limit_per_case in run_cases to allow long runs.
   - Run on a machine with enough time; some instances may take >60 minutes.

6 Parallelization (extra credit, outline):
   A simple parallelization is to spawn a worker for each choice of placing the first k items,
   e.g., fix the placements of the first 1-3 items and run DFS in parallel for each subtree
   (use multiprocessing.Pool). This divides search space but requires careful load balancing.