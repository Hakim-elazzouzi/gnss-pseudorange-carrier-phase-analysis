"""
Satellite selection for Project 4.

Picks the GPS satellite with the most valid C1C epochs
that also has L2W carrier-phase data available.
"""


def select_satellite(obs, sat_setting='auto'):
    """
    Selects the best GPS satellite for pseudorange/carrier-phase comparison.

    Preference: most valid C1C epochs AND has L2W data.

    Args:
        obs         (xarray.Dataset) : loaded RINEX GPS data
        sat_setting (str)            : 'auto' or a fixed SV id e.g. 'G10'

    Returns:
        sat (str): selected satellite ID
    """
    gps_sats = sorted([s for s in obs.sv.values if s.startswith('G')])

    if sat_setting != 'auto':
        print(f"Using manually selected satellite: {sat_setting}")
        return sat_setting

    best_sat   = None
    best_count = 0

    for sat in gps_sats:
        try:
            n = obs['C1C'].sel(sv=sat).to_series().notna().sum()
            has_L2 = (
                'L2W' in obs.data_vars
                and obs['L2W'].sel(sv=sat).to_series().notna().sum() > 10
            )
            if n > best_count and has_L2:
                best_count = n
                best_sat   = sat
        except Exception:
            pass

    sat = best_sat if best_sat else gps_sats[0]
    print(f"Auto-selected satellite: {sat} ({best_count} valid C1C epochs)")
    return sat
