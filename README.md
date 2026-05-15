# Project 4 — Pseudorange vs Carrier-Phase Comparison

> **Code Noise · Phase Precision · Integer Ambiguity · Ionospheric Signature | GPS | Auckland, NZ**

---

## Overview

Every GNSS receiver produces two fundamentally different measurements at every epoch.
This project compares them directly for a GPS satellite over 24 hours:

| Observable | Code | Precision | Drawback |
|-----------|------|-----------|----------|
| **Pseudorange** | `C1C` | ~1–3 metres | Noisy — thermal noise, multipath |
| **Carrier phase** | `L1C` | ~2–3 mm | Contains unknown integer ambiguity N |

---

## The Mathematics

### Pseudorange:
```
P = ρ + c·(dT − dt) + I + T + ε_P
```

### Carrier phase (metres):
```
Φ = ρ + c·(dT − dt) − I + T + λ·N + ε_Φ
```

### Code minus Phase:
```
P − Φ = 2·I + λ·N + (ε_P − ε_Φ)
      ≈ 2·I + λ·N
```

**Key insight:** even without knowing N, the combination `P − Φ` is nearly constant
over time. Slow variations reveal ionospheric delay. Sudden jumps are cycle slips.

---

## Output Plots

### Plot 1 — Raw Measurements Overlaid

Both observables plotted on the same scale. Carrier phase is shifted by a constant
`λ·N` offset to align the curves — making the noise difference visible. A 30-minute
zoom inset around peak elevation shows the noise level directly.

### Plot 2 — Epoch-to-Epoch Noise Comparison

Differences between consecutive 30-second epochs:
- **Top panel:** code noise in metres (σ ≈ 1–5 m)
- **Bottom panel:** phase noise in centimetres (σ ≈ 0.5–2 cm)
- Red dots mark cycle slip candidates (5σ threshold)

### Plot 3 — Code Minus Phase (P − Φ)

- **Top panel:** raw `P − Φ` — flat level dominated by `λ·N`
- **Bottom panel:** detrended — slow variation ≈ `2·ΔI` (ionospheric delay changes)
- Red shading = delay increasing, green = decreasing

---

## File Structure

```
project4-pseudorange-vs-carrier-phase/
├── Outputs/
│   ├── plot1_pseudorange_vs_carrier_phase.png
│   ├── plot2_noise_comparison.png
│   └── plot3_code_minus_phase.png
├── src/
│   ├──project4_pseudorange_vs_carrier_phase_comparison.py    ← Main python
├── requirements.txt                                          ← Python dependencies
├── LICENSE                                                   ← MIT License
└── README.md                                                 ← This file
```

---

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set your RINEX file path

Update **Step 2** of the notebook:

```python
obs_path = "/path/to/your/file.rnx"
```

### 3. Optional: choose a specific satellite

In **Step 3**, change:

```python
SAT = 'auto'   # ← or set to 'G29', 'G05', etc.
```

`auto` picks the GPS satellite with the most dual-frequency (L1 + L2) data.

### 4. Run all cells

```bash
jupyter notebook project4_pseudorange_vs_carrier_phase.ipynb
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `georinex` | Parse RINEX 3 observation files |
| `xarray` | N-dimensional array handling |
| `pandas` | Time series manipulation |
| `numpy` | Numerical computations |
| `matplotlib` | Publication-quality plotting |

---

## Observables Used

| Code | Description |
|------|-------------|
| `C1C` | Pseudorange on L1 C/A code [metres] |
| `L1C` | Carrier phase on L1 C/A [cycles] → converted to metres via `× λ₁` |
| `L2W` | Carrier phase on L2 P(Y) [cycles] → used for cycle slip detection |

### Physical constants used:

```python
C      = 299_792_458.0   # speed of light [m/s]
F1     = 1_575.42e6      # GPS L1 frequency [Hz]
LAM_L1 = C / F1          # L1 wavelength ≈ 0.1903 m  (≈ 19 cm)
```

---

## Why Does This Matter?

Understanding the pseudorange vs carrier-phase trade-off is at the core of GNSS engineering:

- **Standard GPS** (phones, basic receivers) → pseudorange only → metre-level accuracy
- **RTK (Real-Time Kinematic)** → resolves the integer ambiguity N → centimetre accuracy
- **PPP (Precise Point Positioning)** → uses both observables with precise clocks/orbits → cm globally
- **Ionospheric monitoring** → `P − Φ` combination is standard in space weather research

---

## Author

**Hakim El Azzouzi**  
MSc Global Navigation Satellite Systems  
Mohammed First University, Oujda, Morocco  
📧 elazzouzihakim10@gmail.com  
🔗 [linkedin.com/in/Hakim-El-Azzouzi](https://linkedin.com/in/Hakim-El-Azzouzi)  
📍 Luxembourg 🇱🇺

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Part of the GNSS RINEX Analysis Series

| # | Project |
|---|---------|
| 1 | Single GPS Satellite — Pseudorange & SNR Heatmap |
| 2 | All GPS Satellites — Fleet Pseudorange & SNR Heatmap |
| 3 | Multi-Constellation GNSS — One Satellite per System |
| **4** | **Pseudorange vs Carrier-Phase Comparison** ← You are here |
| 5 | Constellation Summary — Pie Chart & Histogram |
| 6 | Ionospheric Delay — Geometry-Free Combination |
| 7 | Data Quality Report |
