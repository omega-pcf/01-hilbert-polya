#!/usr/bin/env python3
"""
Dual spectral structure of T*
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import sys

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from generators import register
from utils import save_figure, PHI

# ─────────────────────────────────────────────────────────────────────
# First 100 Riemann zeros (imaginary parts)
# ─────────────────────────────────────────────────────────────────────
zeros = np.array([
    14.134725, 21.022040, 25.010858, 30.424876, 32.935062,
    37.586178, 40.918719, 43.327073, 48.005151, 49.773832,
    52.970321, 56.446248, 59.347044, 60.831779, 65.112544,
    67.079811, 69.546402, 72.067158, 75.704691, 77.144840,
    79.337375, 82.910381, 84.735493, 87.425275, 88.809111,
    92.491899, 94.651344, 95.870634, 98.831194, 101.317851,
    103.725538, 105.446623, 107.168611, 111.029536, 111.874659,
    114.320221, 116.226680, 118.790783, 121.370125, 122.946829,
    124.256819, 127.516684, 129.578704, 131.087689, 133.497737,
    134.756510, 138.116042, 139.736209, 141.123707, 143.111846,
    146.000982, 147.422765, 150.053521, 150.925258, 153.024694,
    156.112909, 157.597592, 158.849988, 161.188964, 163.030709,
    165.537070, 167.184439, 169.094515, 169.911977, 173.411537,
    174.754191, 176.441434, 178.377407, 179.916484, 182.207079,
    184.874467, 185.598783, 187.228922, 189.416159, 192.026656,
    193.079727, 195.265397, 196.876481, 198.015309, 201.264751,
    202.493595, 204.189671, 205.394697, 207.906259, 209.576509,
    211.690862, 213.347919, 214.547044, 216.169538, 219.067596,
    220.714919, 221.430705, 224.007000, 224.983324, 227.421444,
    229.337413, 231.561651, 233.693404, 236.524230, 238.169759,
])

PI   = np.pi
ALPHA0, BETA0 = 59/40, 1/8
MU,    SIGMA  = 0.5,   1.5

def c_func(n, alpha=ALPHA0, beta=BETA0):
    return 2.0 + alpha / (1.0 + beta * np.log(n))

def T_star_r2(n, alpha=ALPHA0, beta=BETA0):
    c = c_func(n, alpha, beta)
    return c * PI * n / np.log(MU * n + SIGMA)

def get_generation(n):
    return int(np.floor(np.log2(max(n, 1))))

def T_star_r1(n):
    k = get_generation(n)
    beta_k = 2.0**(-k)
    return T_star_r2(n, alpha=ALPHA0, beta=beta_k)

@register("dual_spectrum")
def generate_dual_spectrum(output_dir: Path, verbose: bool = False) -> None:
    if verbose:
        print("  Generating dual spectrum figure...")

    ns = np.arange(1, 101)
    Tstar = np.array([T_star_r1(n) if n <= 30 else T_star_r2(n) for n in ns])
    ratio = Tstar / zeros
    c_vals_r1 = np.array([c_func(n, ALPHA0, 2.0**(-get_generation(n))) for n in range(1, 31)])
    n_c2 = np.arange(1, 101)
    c_vals_r2 = np.array([c_func(n) for n in n_c2])

    def envelope(ns, sign=+1):
        return 1.0 + sign / np.log(np.maximum(ns, 2))

    fig = plt.figure(figsize=(8, 10))
    gs = gridspec.GridSpec(3, 1, hspace=0.15, left=0.10, right=0.97, top=0.97, bottom=0.07)

    GEN_BOUNDARIES = [2**k for k in range(0, 8)]
    GEN_COLORS = ['#e8f4f8', '#d4ebf2', '#c0e2ec', '#acd9e6', '#98d0e0', '#84c7da', '#70bed4']
    MERSENNE = {3: r'$M_2$', 7: r'$M_3$', 31: r'$M_5$'}

    def draw_gen_bands(ax, alpha=0.18):
        for k in range(len(GEN_BOUNDARIES) - 1):
            lo, hi = GEN_BOUNDARIES[k], min(GEN_BOUNDARIES[k + 1], 101)
            if lo <= 100:
                ax.axvspan(lo, hi, color=GEN_COLORS[k % len(GEN_COLORS)], alpha=alpha, lw=0, zorder=0)

    # (a) Spectrum
    ax1 = fig.add_subplot(gs[0])
    draw_gen_bands(ax1)
    ax1.plot(ns, zeros, 'o', color='#222', ms=3, label=r'$t_n$ (exact zeros)')
    ax1.plot(ns, Tstar, 's', color='#cc2222', ms=3.5, mfc='none', mew=0.8, label=r'$T^*(n)$')
    ax1.set_ylabel(r'Height $t_n$')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.tick_params(labelbottom=False)

    # (b) Ratio
    ax2 = fig.add_subplot(gs[1], sharex=ax1)
    draw_gen_bands(ax2)
    ns_env = np.linspace(2, 100, 500)
    ax2.fill_between(ns_env, envelope(ns_env, -1), envelope(ns_env, +1), color='0.85', alpha=0.5, lw=0, label=r'$1\pm O(1/\ln n)$')
    ax2.plot(ns[:30], ratio[:30], 'o', color='0.35', ms=2.5, label='Regime I')
    ax2.plot(ns[30:], ratio[30:], 's', color='#b22222', ms=2.5, label='Regime II')
    ax2.axhline(1.0, color='0.5', lw=0.5, ls='--')
    ax2.set_ylabel(r'$T^*(n)/t_n$')
    ax2.set_ylim(0.8, 1.2)
    ax2.legend(loc='upper right', fontsize=9)
    ax2.tick_params(labelbottom=False)

    # (c) Modulation
    ax3 = fig.add_subplot(gs[2], sharex=ax1)
    draw_gen_bands(ax3, 0.2)
    ax3.plot(range(1, 31), c_vals_r1, 'o-', color='0.3', ms=2.5, lw=1, label=r'$c(n)$ adaptive')
    ax3.plot(n_c2[30:], c_vals_r2[30:], 's-', color='#b22222', ms=2.5, lw=1, label=r'$c(n)$ fixed')
    ax3.axhline(2.0, color='0.65', lw=0.5, ls='--')
    ax3.set_xlabel(r'Zero index $n$')
    ax3.set_ylabel(r'$c(n)$')
    ax3.set_ylim(1.8, 3.6)
    ax3.legend(loc='upper right', fontsize=9)

    plt.tight_layout()
    output_path = output_dir / "fig_dual_spectrum"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_dual_spectrum(Path("src/images"), verbose=True)
