"""
RINEX loader for Project 4.

Loads GPS-only observations (C1C, L1C, L2W) needed for
pseudorange vs carrier-phase comparison.
"""

import georinex as gr


def load_rinex(obs_path):
    """
    Loads RINEX header and GPS observation data.

    Returns:
        obs    (xarray.Dataset) : GPS observation data
        header (dict)           : RINEX file header
    """
    print("FILE HEADER")
    print("=" * 60)
    header = gr.rinexheader(obs_path)
    for k, v in header.items():
        print(f"{k:<25}: {v}")

    print("\nLoading GPS observation data...")
    obs = gr.load(obs_path, interval=30, use='G')
    print(f"Data loaded: {len(obs.sv)} SVs | {len(obs.time)} epochs\n")

    return obs, header
