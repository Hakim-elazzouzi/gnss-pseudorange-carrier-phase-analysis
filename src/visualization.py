"""
Visualization for Project 4.
Produces three plots:
  1. Pseudorange vs carrier phase (raw, overlaid)
  2. Epoch-to-epoch noise comparison (via ΔCMP — code-minus-phase difference)
  3. Code minus phase (P − Φ) — raw and detrended
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from config import (
    LAM_L1,
    COLOR_CODE, COLOR_PHASE, COLOR_DIFF,
    FIGURE_FACE, AX_FACE, GRID_COLOR, SPINE_COLOR, TICK_COLOR,
)


# ─────────────────────────────────────────────────────────────
# Plot 1 — Pseudorange vs Carrier Phase (raw, overlaid)
# ─────────────────────────────────────────────────────────────

def plot_raw_overlay(sat, pr, cp_L1):
    """
    Overlays pseudorange and carrier phase on the same range axis.

    Carrier phase is shifted by its mean offset (λ·N) to align
    the curves geometrically — making the noise difference visible.
    """
    offset     = pr.mean() - cp_L1.mean()
    cp_shifted = cp_L1 + offset

    fig, ax = plt.subplots(figsize=(16, 6), facecolor=FIGURE_FACE)
    ax.set_facecolor(AX_FACE)

    ax.set_title(
        f'Pseudorange vs Carrier Phase — GPS {sat} | AUCK00NZL | 2026-01-01\n'
        'Both measure the same geometric range — carrier phase is shifted by λ·N to align',
        fontsize=13, fontweight='bold', color="#ffffff"
    )

    ax.plot(pr.index, pr.values / 1e6,
            color=COLOR_CODE, lw=1.8, alpha=0.9,
            label='Pseudorange C1C  — code measurement  (~1–3 m noise)')

    ax.plot(cp_shifted.index, cp_shifted.values / 1e6,
            color=COLOR_PHASE, lw=1.2, alpha=0.9,
            label=(f'Carrier Phase L1C  — phase measurement  (~3 mm noise)'
                   f'  [shifted by {offset/1e6:.4f} Mm = λ·N]'))

    # ── Zoom inset around peak elevation ─────────────────────
    idx_min    = pr.idxmin()
    zoom_start = idx_min - pd.Timedelta('15min')
    zoom_end   = idx_min + pd.Timedelta('15min')
    pr_zoom    = pr[zoom_start:zoom_end]
    cp_zoom    = cp_shifted[zoom_start:zoom_end]

    if len(pr_zoom) > 3:
        axins = ax.inset_axes([0.02, 0.05, 0.28, 0.38])
        axins.set_facecolor("#0d1b2a")
        axins.plot(pr_zoom.index,  pr_zoom.values / 1e6,
                   color=COLOR_CODE,  lw=1.2, alpha=0.9)
        axins.plot(cp_zoom.index,  cp_zoom.values / 1e6,
                   color=COLOR_PHASE, lw=1.0, alpha=0.9)
        axins.set_title('Zoom: 30 min at peak elevation',
                        fontsize=7, color=TICK_COLOR)
        axins.tick_params(colors=TICK_COLOR, labelsize=6)
        axins.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
        for spine in axins.spines.values():
            spine.set_edgecolor("#444444")
        axins.grid(True, color=GRID_COLOR, linewidth=0.4)

    ax.set_ylabel('Range [Mm = million metres]', fontsize=11, color=TICK_COLOR)
    ax.set_xlabel('UTC Time (HH:MM)', fontsize=11, color=TICK_COLOR)
    ax.tick_params(colors=TICK_COLOR)
    ax.grid(True, color=GRID_COLOR, linewidth=0.5)
    for spine in ax.spines.values():
        spine.set_edgecolor(SPINE_COLOR)
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color=TICK_COLOR)

    legend = ax.legend(fontsize=9, loc='upper right',
                       framealpha=0.3, facecolor="#1a1a2e", edgecolor="#444444")
    for text in legend.get_texts():
        text.set_color("white")

    plt.tight_layout()
    plt.savefig('plot1_pseudorange_vs_carrier_phase.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot1_pseudorange_vs_carrier_phase.png")

    return offset


# ─────────────────────────────────────────────────────────────
# Plot 2 — Noise Comparison via Δ(Code − Phase)
# ─────────────────────────────────────────────────────────────

def plot_noise_comparison(sat, cmp_diff, pr_noise_std, cp_noise_std,
                          noise_ratio, slips):
    """
    Two-panel plot comparing pseudorange noise vs carrier-phase noise.

    Uses Δ(P − Φ) as the noise proxy: differencing P − Φ cancels
    geometric range, clocks, and troposphere — leaving code noise
    (since phase noise is ~100× smaller and negligible here).

    Panel 1: Δ(P − Φ) with ±1σ lines — the code noise signal
    Panel 2: Simulated phase noise at mm level for visual comparison
    """
    # Simulate phase noise for visual scale comparison
    # Phase noise ~ LAM_L1 * 0.005 cycles ≈ 1 mm per epoch
    rng = np.random.default_rng(seed=42)
    cp_noise_sim = pd.Series(
        rng.normal(0, cp_noise_std, len(cmp_diff)),
        index=cmp_diff.index
    )

    fig, axes = plt.subplots(2, 1, figsize=(16, 8), sharex=True,
                             facecolor=FIGURE_FACE)
    fig.suptitle(
        f'Epoch-to-Epoch Noise: Pseudorange vs Carrier Phase — GPS {sat}\n'
        'Δ(P − Φ) isolates code noise | Y-axes are on different scales',
        fontsize=13, fontweight='bold', color="#ffffff"
    )

    for ax in axes:
        ax.set_facecolor(AX_FACE)
        ax.tick_params(colors=TICK_COLOR)
        ax.grid(True, color=GRID_COLOR, linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor(SPINE_COLOR)

    # ── Panel 1: Code noise via Δ(CMP) ───────────────────────
    axes[0].plot(cmp_diff.index, cmp_diff.values,
                 color=COLOR_CODE, lw=0.8, alpha=0.85)
    axes[0].fill_between(cmp_diff.index, cmp_diff.values,
                         color=COLOR_CODE, alpha=0.15)
    axes[0].axhline(0,  color="#555555", lw=0.8, ls='--')
    axes[0].axhline(+pr_noise_std, color=COLOR_CODE, lw=1.0, ls=':', alpha=0.8,
                    label=f'+1σ = {pr_noise_std:.3f} m')
    axes[0].axhline(-pr_noise_std, color=COLOR_CODE, lw=1.0, ls=':', alpha=0.8,
                    label=f'−1σ = {pr_noise_std:.3f} m')

    if len(slips) > 0:
        axes[0].scatter(slips.index, slips.values,
                        color="#F44336", s=60, zorder=5,
                        label=f'Anomaly / cycle slip ({len(slips)} detected)')

    axes[0].set_ylabel('Δ(P − Φ)  [m / epoch]', color=TICK_COLOR, fontsize=11)
    axes[0].set_title(
        f'Code noise  C1C  |  σ = {pr_noise_std:.3f} m'
        f'  (~{pr_noise_std*100:.0f} cm RMS per epoch)',
        fontsize=10, color="#ffffff"
    )
    legend0 = axes[0].legend(fontsize=9, framealpha=0.3,
                             facecolor="#1a1a2e", edgecolor="#444444")
    for t in legend0.get_texts():
        t.set_color("white")

    # ── Panel 2: Phase noise (spec-based, mm level) ───────────
    axes[1].plot(cp_noise_sim.index, cp_noise_sim.values * 100,
                 color=COLOR_PHASE, lw=0.8, alpha=0.85)
    axes[1].fill_between(cp_noise_sim.index, cp_noise_sim.values * 100,
                         color=COLOR_PHASE, alpha=0.15)
    axes[1].axhline(0, color="#555555", lw=0.8, ls='--')
    axes[1].axhline(+cp_noise_std * 100, color=COLOR_PHASE, lw=1.0, ls=':', alpha=0.8,
                    label=f'+1σ = {cp_noise_std*100:.2f} cm')
    axes[1].axhline(-cp_noise_std * 100, color=COLOR_PHASE, lw=1.0, ls=':', alpha=0.8,
                    label=f'−1σ = {cp_noise_std*100:.2f} cm')

    axes[1].set_ylabel('ΔCarrier Phase [cm / epoch]', color=TICK_COLOR, fontsize=11)
    axes[1].set_xlabel('UTC Time (HH:MM)', color=TICK_COLOR, fontsize=11)
    axes[1].set_title(
        f'Phase noise  L1C  |  σ ≈ {cp_noise_std*100:.2f} cm'
        f'  —  {noise_ratio:.0f}× less noisy than pseudorange',
        fontsize=10, color="#ffffff"
    )
    legend1 = axes[1].legend(fontsize=9, framealpha=0.3,
                             facecolor="#1a1a2e", edgecolor="#444444")
    for t in legend1.get_texts():
        t.set_color("white")

    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axes[1].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color=TICK_COLOR)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('plot2_noise_comparison.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot2_noise_comparison.png")


# ─────────────────────────────────────────────────────────────
# Plot 3 — Code Minus Phase (P − Φ)
# ─────────────────────────────────────────────────────────────

def plot_code_minus_phase(sat, code_minus_phase):
    """
    Two-panel plot of Code Minus Phase (P − Φ).

    Panel 1: raw P − Φ (level dominated by λ·N integer ambiguity)
    Panel 2: detrended (mean removed), isolating ionospheric variation 2·ΔI
    """
    cmp_mean        = code_minus_phase.mean()
    cmp_detrend     = code_minus_phase - cmp_mean
    n_cycles_approx = cmp_mean / LAM_L1

    fig, axes = plt.subplots(2, 1, figsize=(16, 9), sharex=True,
                             facecolor=FIGURE_FACE)
    fig.suptitle(
        f'Code Minus Phase  (P − Φ)  —  GPS {sat} | AUCK00NZL | 2026-01-01\n'
        'P − Φ = 2·I + λ·N + noise  —  constant level = ambiguity, variations = ionosphere',
        fontsize=13, fontweight='bold', color="#ffffff"
    )

    for ax in axes:
        ax.set_facecolor(AX_FACE)
        ax.tick_params(colors=TICK_COLOR)
        ax.grid(True, color=GRID_COLOR, linewidth=0.5)
        for spine in ax.spines.values():
            spine.set_edgecolor(SPINE_COLOR)

    # ── Panel 1: Raw P − Φ ────────────────────────────────────
    axes[0].plot(code_minus_phase.index, code_minus_phase.values,
                 color=COLOR_DIFF, lw=1.3, alpha=0.9,
                 label='P − Φ  (raw)')
    axes[0].axhline(cmp_mean, color="#FFEB3B", ls='--', lw=1.2,
                    label=f'Mean = {cmp_mean:.2f} m  ≈  2·I + λ·N')
    axes[0].annotate(
        f'Mean ≈ {cmp_mean:.1f} m\n≈ {n_cycles_approx:.0f} L1 cycles\n(contains λ·N)',
        xy=(code_minus_phase.index[len(code_minus_phase) // 2], cmp_mean),
        xytext=(30, 30), textcoords='offset points',
        color="#FFEB3B", fontsize=9,
        arrowprops=dict(arrowstyle='->', color="#FFEB3B")
    )
    axes[0].set_ylabel('P − Φ  [m]', color=TICK_COLOR, fontsize=11)
    axes[0].set_title(
        'P − Φ = 2·I + λ·N  |  Level dominated by integer ambiguity λ·N',
        fontsize=10, color="#ffffff"
    )
    legend0 = axes[0].legend(fontsize=9, framealpha=0.3,
                             facecolor="#1a1a2e", edgecolor="#444444")
    for t in legend0.get_texts():
        t.set_color("white")

    # ── Panel 2: Detrended P − Φ (ionospheric variation) ─────
    axes[1].plot(cmp_detrend.index, cmp_detrend.values,
                 color="#00BCD4", lw=1.3, alpha=0.9,
                 label='(P − Φ) − mean  ≈  2·ΔI  (ionospheric variation)')
    axes[1].fill_between(cmp_detrend.index, cmp_detrend.values,
                         color="#00BCD4", alpha=0.1)
    axes[1].axhline(0, color="#555555", lw=0.8, ls='--')
    axes[1].fill_between(cmp_detrend.index, cmp_detrend.values, 0,
                         where=(cmp_detrend.values > 0),
                         color="#F44336", alpha=0.15,
                         label='Ionospheric delay increasing')
    axes[1].fill_between(cmp_detrend.index, cmp_detrend.values, 0,
                         where=(cmp_detrend.values < 0),
                         color="#4CAF50", alpha=0.15,
                         label='Ionospheric delay decreasing')
    axes[1].set_ylabel('(P − Φ) − mean  [m]', color=TICK_COLOR, fontsize=11)
    axes[1].set_xlabel('UTC Time (HH:MM)', color=TICK_COLOR, fontsize=11)
    axes[1].set_title(
        '(P − Φ) detrended  ≈  2·ΔI  |  Slow variations = ionospheric delay changes',
        fontsize=10, color="#ffffff"
    )
    legend1 = axes[1].legend(fontsize=9, framealpha=0.3,
                             facecolor="#1a1a2e", edgecolor="#444444")
    for t in legend1.get_texts():
        t.set_color("white")

    axes[1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    axes[1].xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color=TICK_COLOR)

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('plot3_code_minus_phase.png', dpi=150,
                bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close()
    print("Plot saved: plot3_code_minus_phase.png")

    return cmp_mean, n_cycles_approx
