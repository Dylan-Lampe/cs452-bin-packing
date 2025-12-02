#!/usr/bin/env bash
# Example driver script to run the exact solver on generated test cases
# Writes results to binpacking_results/results.csv

python exact_bin_packing.py
# If you want to run with larger instances:
# python - <<'PY'
# from exact_bin_packing import generate_test_cases, run_cases
# cases = generate_test_cases(num_cases=80, n_min=10, n_max=30, capacity=100, seed=42)
# run_cases(cases, time_limit_per_case=3600.0, out_dir='binpacking_results')
# PY