"""
Project 4 — Pseudorange vs Carrier-Phase Comparison
=====================================================
Station  : AUCK00NZL — Auckland, New Zealand
File     : AUCK00NZL_R_20260010000_01D_30S_MO.rnx
Date     : 2026-01-01

Pipeline
--------
1. Load RINEX (GPS only)
2. Select best GPS satellite
3. Extract and align observables
4. Report statistics
5. Plot 1 — Raw overlay (pseudorange + carrier phase)
6. Plot 2 — Epoch-to-epoch noise comparison (via ΔCMP)
7. Plot 3 — Code minus phase (P − Φ)
"""

import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')

from config import OBS_PATH, SAT, LAM_L1

from rinex_loader        import load_rinex
from satellite_selection import select_satellite
from observables         import extract_observables, compute_noise
from reporting           import (print_wavelengths, print_observable_stats,
                                 print_noise_stats)
from visualization       import (plot_raw_overlay, plot_noise_comparison,
                                 plot_code_minus_phase)


def main():

    # ── 1. Load RINEX ────────────────────────────────────────
    obs, header = load_rinex(OBS_PATH)

    # ── 2. Select satellite ──────────────────────────────────
    sat = select_satellite(obs, SAT)

    # ── 3. Extract observables ───────────────────────────────
    pr, cp_L1, cp_L2, code_minus_phase, common = extract_observables(obs, sat)

    # ── 4. Report ────────────────────────────────────────────
    print_wavelengths()
    print_observable_stats(sat, pr, cp_L1, code_minus_phase, common)

    cmp_diff, pr_noise_std, cp_noise_std, noise_ratio, slips = \
        compute_noise(pr, cp_L1)
    print_noise_stats(pr_noise_std, cp_noise_std, noise_ratio, slips)

    # ── 5. Plot 1 — Raw overlay ──────────────────────────────
    offset = plot_raw_overlay(sat, pr, cp_L1)
    print(f"   Applied shift = {offset:.3f} m  ≈  {offset/LAM_L1:.0f} L1 wavelengths")

    # ── 6. Plot 2 — Noise comparison ─────────────────────────
    plot_noise_comparison(sat, cmp_diff, pr_noise_std, cp_noise_std,
                          noise_ratio, slips)

    # ── 7. Plot 3 — Code minus phase ─────────────────────────
    cmp_mean, n_cycles = plot_code_minus_phase(sat, code_minus_phase)
    print(f"   Mean (P − Φ) = {cmp_mean:.2f} m  ≈  {n_cycles:.0f} L1 wavelengths")

    print("\nAll plots saved successfully.")


if __name__ == "__main__":
    main()
