"""
Observable extraction for Project 4.

Extracts and aligns pseudorange, carrier-phase, and
derived quantities for a single GPS satellite.
"""

import numpy as np
import pandas as pd

from config import LAM_L1, LAM_L2


def extract_observables(obs, sat):
    """
    Extracts pseudorange (C1C), L1 carrier phase (L1C), and
    optionally L2 carrier phase (L2W) for the given satellite.

    Aligns C1C and L1C to their common timestamps.

    Returns:
        pr              (pd.Series)      : pseudorange C1C [m]
        cp_L1           (pd.Series)      : L1 carrier phase [m]
        cp_L2           (pd.Series|None) : L2 carrier phase [m], or None
        code_minus_phase(pd.Series)      : P − Φ [m]
        common          (DatetimeIndex)
    """
    # Pseudorange C1C [m]
    pr = obs['C1C'].sel(sv=sat).to_series().dropna()

    # Carrier phase L1C [cycles → m]
    cp_L1 = obs['L1C'].sel(sv=sat).to_series().dropna() * LAM_L1

    # Carrier phase L2W [cycles → m] if available
    cp_L2 = None
    if 'L2W' in obs.data_vars:
        raw_L2 = obs['L2W'].sel(sv=sat).to_series().dropna()
        if len(raw_L2) > 0:
            cp_L2 = raw_L2 * LAM_L2

    # Align to common timestamps
    common = pr.index.intersection(cp_L1.index)
    pr    = pr[common]
    cp_L1 = cp_L1[common]

    # Code minus phase:  P − Φ = 2·I + λ·N + noise
    code_minus_phase = pr - cp_L1

    return pr, cp_L1, cp_L2, code_minus_phase, common


def compute_noise(pr, cp_L1):
    """
    Computes epoch-to-epoch noise statistics using the code-minus-phase
    difference (ΔCMP), which is the textbook-correct GNSS noise proxy.

    Why CMP diff and not raw pr.diff():
    - Raw pr.diff() includes orbital velocity (~15–20 km per 30 s epoch),
      which completely swamps the metre-level code noise.
    - CMP = P − Φ cancels geometric range, clock, and troposphere.
    - Δ(CMP) then isolates code noise (phase noise is ~100× smaller).

    Only consecutive epochs within 31 seconds are differenced to avoid
    large jumps across tracking gaps.

    Returns:
        cmp_diff      (pd.Series) : epoch differences of (P − Φ) [m]
        pr_noise_std  (float)     : std of cmp_diff [m]  ≈ code noise
        cp_noise_std  (float)     : phase noise estimate [m] (≈ pr_noise/ratio)
        noise_ratio   (float)     : typical code/phase ratio (~100)
        slips         (pd.Series) : cycle-slip candidates (5-sigma jumps in Δ(CMP))
    """
    code_minus_phase = pr - cp_L1

    # Epoch-to-epoch difference of CMP
    cmp_diff_raw = code_minus_phase.diff()

    # Mask cross-gap differences (gap > 31 s)
    time_gap = pd.Series(pr.index.astype(np.int64), index=pr.index).diff()
    valid    = time_gap <= 31e9   # nanoseconds
    cmp_diff = cmp_diff_raw[valid].dropna()

    # Code noise std from CMP diff
    pr_noise_std = cmp_diff.std()

    # Phase noise: L1 wavelength ≈ 19 cm, typical tracking ~1 mm → ~0.005 cycles
    # Estimated from hardware specs; not directly observable from single-freq data
    cp_noise_std = LAM_L1 * 0.005   # ~1 mm

    noise_ratio = pr_noise_std / cp_noise_std

    # Cycle slip candidates: sudden large jump in CMP diff (>> normal code noise)
    slip_threshold = 5 * pr_noise_std
    slips = cmp_diff[np.abs(cmp_diff) > slip_threshold]

    return cmp_diff, pr_noise_std, cp_noise_std, noise_ratio, slips
