"""
Reporting for Project 4.

All console output: observable statistics and noise metrics.
"""

import numpy as np
from config import LAM_L1, LAM_L2


def print_wavelengths():
    """Prints L1 and L2 wavelengths."""
    print(f"LAM_L1 = {LAM_L1:.15f} m  ≈  {LAM_L1*100:.4f} cm")
    print(f"LAM_L2 = {LAM_L2:.15f} m  ≈  {LAM_L2*100:.4f} cm")


def print_observable_stats(sat, pr, cp_L1, code_minus_phase, common):
    """Prints pseudorange, carrier-phase, and code-minus-phase statistics."""
    print()
    print(f"   Observable statistics for {sat}:")
    print(f"   Common epochs (C1C ∩ L1C) : {len(common)}")
    print()
    print(f"   Pseudorange  C1C  min: {pr.min()/1e6:.3f} Mm   "
          f"max: {pr.max()/1e6:.3f} Mm")
    print(f"   Carrier Ph.  L1C  min: {cp_L1.min()/1e6:.3f} Mm   "
          f"max: {cp_L1.max()/1e6:.3f} Mm")
    print()
    print(f"   Code − Phase (P − Φ):")
    print(f"     Mean  : {code_minus_phase.mean():,.3f} m"
          f"  ← contains λ·N (integer ambiguity term)")
    print(f"     Std   : {code_minus_phase.std():.3f} m"
          f"    ← reflects code noise + ionosphere")
    print(f"     Min   : {code_minus_phase.min():,.3f} m")
    print(f"     Max   : {code_minus_phase.max():,.3f} m")
    print()
    print(f"   The mean of (P − Φ) ≈ 2·I + λ·N")
    print(f"   We cannot separate I and N without a second frequency.")
    print(f"   But changes in (P − Φ) over time ≈ ionospheric variation (2·ΔI).")


def print_noise_stats(pr_noise_std, cp_noise_std, noise_ratio, slips):
    """Prints noise statistics and cycle-slip count."""
    print(f"Pseudorange  noise σ (from ΔCMP)    : {pr_noise_std:.4f} m")
    print(f"Carrier phase noise σ (spec estimate): {cp_noise_std*100:.4f} cm")
    print(f"Noise ratio code/phase               : {noise_ratio:.0f}×"
          f"  — phase is {noise_ratio:.0f}× less noisy")
    if len(slips) > 0:
        print(f"Cycle slip candidates detected       : {len(slips)}")
