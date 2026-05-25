# ─────────────────────────────────────────────────────────────
# Project 4 — Config
# Pseudorange vs Carrier-Phase Comparison
# ─────────────────────────────────────────────────────────────

OBS_PATH = "/AUCK00NZL_R_20260010000_01D_30S_MO.rnx"

# ── Physical constants ────────────────────────────────────────
C     = 299_792_458.0   # speed of light [m/s] — exact, by definition
F1    = 1_575.42e6      # GPS L1 frequency [Hz] — exact, from GPS ICD
F2    = 1_227.60e6      # GPS L2 frequency [Hz] — exact, from GPS ICD

LAM_L1 = C / F1        # L1 wavelength ≈ 0.1903 m
LAM_L2 = C / F2        # L2 wavelength ≈ 0.2442 m

# ── Satellite selection ───────────────────────────────────────
# Set to 'auto' to pick the GPS satellite with most valid data,
# or e.g. 'G10' to fix a specific satellite.
SAT = 'auto'

# ── Plot colours ─────────────────────────────────────────────
COLOR_CODE  = "#1E88E5"   # blue   → pseudorange  (noisy code)
COLOR_PHASE = "#43A047"   # green  → carrier phase (precise)
COLOR_DIFF  = "#8E24AA"   # purple → derived combination (P − Φ)

# ── Dark theme ────────────────────────────────────────────────
FIGURE_FACE = "#0d1117"
AX_FACE     = "#111827"
GRID_COLOR  = "#222222"
SPINE_COLOR = "#333333"
TICK_COLOR  = "#aaaaaa"
TEXT_COLOR  = "#aaaaaa"
