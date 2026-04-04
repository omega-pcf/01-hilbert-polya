#!/usr/bin/env python3
"""
fig2_comparative — Comparative dimensional mechanisms
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from pathlib import Path
import sys

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from generators import register
from utils import save_figure, PHI

@register("comparative_dimensional_mechanisms")
def generate_comparative(output_dir: Path, verbose: bool = False) -> None:
    if verbose:
        print("  Generating comparative dimensional mechanisms figure...")

    fig = plt.figure(figsize=(14, 12))

    # (A) String Theory
    ax1 = fig.add_subplot(2, 2, 1, projection='3d')
    theta = np.linspace(0, 2*np.pi, 60)
    z_cyl = np.linspace(-1, 1, 40)
    Theta, Z_cyl = np.meshgrid(theta, z_cyl)
    X1 = np.cos(Theta)
    Y1 = np.sin(Theta)
    ax1.plot_surface(X1, Y1, Z_cyl, color='gray', alpha=0.2, linewidth=0)
    ax1.plot(np.cos(theta), np.sin(theta), 0, color='blue', lw=2, label='Closed String $S^1$')
    
    ax1.set_xlabel('Re(z)', fontsize=10, labelpad=1)
    ax1.set_ylabel('Im(z)', fontsize=10, labelpad=1)
    ax1.set_zlabel('z', fontsize=10, labelpad=1)
    ax1.set_xlim(-1.1, 1.1); ax1.set_ylim(-1.1, 1.1); ax1.set_zlim(-1.1, 1.1)
    ax1.tick_params(labelsize=9, pad=0)
    ax1.view_init(elev=18, azim=-60)

    # (B) AdS/CFT
    ax2 = fig.add_subplot(2, 2, 2, projection='3d')
    theta_ads = np.linspace(0, 2*np.pi, 60)
    z_ads     = np.linspace(0.38, 8.0, 55)
    T2, Z2    = np.meshgrid(theta_ads, z_ads)
    R2        = 3.5 / Z2
    X2        = R2 * np.cos(T2)
    Y2        = R2 * np.sin(T2)
    ax2.plot_wireframe(X2, Y2, Z2, color='black', lw=0.35, alpha=0.75, rstride=3, cstride=3)
    theta_bnd = np.linspace(0, 2*np.pi, 300)
    z_bnd     = 0.38
    r_bnd     = 3.5 / z_bnd
    ax2.plot(r_bnd * np.cos(theta_bnd), r_bnd * np.sin(theta_bnd), z_bnd * np.ones_like(theta_bnd), '-', color='red', lw=2.5, zorder=10)
    
    ax2.text(10.0, -12.0, 3.5, r'$\mathrm{CFT}_d$', color='red', fontsize=24, fontweight='bold', zorder=12)
    ax2.text(1.5, -1.5, 8.8, r'$\mathrm{AdS}_{d+1}$', color='blue', fontsize=26, fontweight='bold', zorder=12)


    ax2.set_xlabel('x', fontsize=10, labelpad=1)

    ax2.set_ylabel('y', fontsize=10, labelpad=1)
    ax2.set_zlabel('z', fontsize=10, labelpad=1)
    ax2.set_xlim(-10, 10); ax2.set_ylim(-10, 10); ax2.set_zlim(0, 9)
    ax2.xaxis.set_major_locator(plt.MultipleLocator(2.0))
    ax2.yaxis.set_major_locator(plt.MultipleLocator(2.0))
    ax2.zaxis.set_major_locator(plt.MultipleLocator(2.0))
    ax2.tick_params(labelsize=9, pad=0)
    ax2.view_init(elev=22, azim=-50)

    # (C) PCF Extended Space
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    y_range = np.linspace(-5, 5, 30)
    x_range = np.linspace(-5, 5, 30)
    YY3, XX3 = np.meshgrid(y_range, x_range)
    ZZ3 = PHI * YY3
    ax3.plot_surface(XX3, YY3, ZZ3, color='cyan', alpha=0.35, linewidth=0, antialiased=True)
    angles_v = [0, 2*np.pi/3, 4*np.pi/3]
    v_colors_c = ['red', 'green', 'blue']
    v_names_c  = ['P', 'C', 'F']
    R_v = 3.0
    for ang, col, name in zip(angles_v, v_colors_c, v_names_c):
        xv = R_v * np.cos(ang); yv = R_v * np.sin(ang); zv = PHI * yv
        ax3.scatter([xv], [yv], [zv], color=col, s=100, zorder=8, depthshade=False, edgecolors='black', linewidths=0.6)
        ax3.text(xv * 1.3, yv * 1.3, zv * 1.1, name, fontsize=14, color=col, fontweight='bold')
    ax3.set_xlabel('x', fontsize=10, labelpad=1)
    ax3.set_ylabel('y', fontsize=10, labelpad=1)
    ax3.set_zlabel('z', fontsize=10, labelpad=1)
    ax3.set_xlim(-5, 5); ax3.set_ylim(-5, 5); ax3.set_zlim(-9, 9)
    ax3.tick_params(labelsize=9, pad=0)
    ax3.view_init(elev=18, azim=-60)

    # (D) PCF Base Cylinder
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    R0 = 3.0
    u_cyl = np.linspace(0, 2*np.pi, 80)
    z_levels = np.linspace(-7, 7, 30)
    U4, Z4 = np.meshgrid(u_cyl, z_levels)
    X4 = R0 * np.cos(U4); Y4 = R0 * np.sin(U4)
    ax4.plot_surface(X4, Y4, Z4, color='gray', alpha=0.18, linewidth=0, antialiased=True)
    t_curve = np.linspace(0, 2*np.pi, 400)
    xh = R0*np.cos(t_curve); yh = R0*np.sin(t_curve); zh = PHI*yh
    ax4.plot(xh, yh, zh, '-', color='purple', lw=2.5, zorder=9)
    for ti, col, name in zip(angles_v, v_colors_c, v_names_c):
        xv = R0*np.cos(ti); yv = R0*np.sin(ti); zv = PHI*yv
        ax4.scatter([xv],[yv],[zv], color=col, s=120, zorder=12, depthshade=False, edgecolors='black', linewidths=0.6)
        ax4.text(xv*1.4, yv*1.4, zv + 0.5, name, fontsize=14, color=col, fontweight='bold', zorder=13)
    ax4.set_xlabel('y', fontsize=10, labelpad=1)
    ax4.set_ylabel('x', fontsize=10, labelpad=1)
    ax4.set_zlabel('z', fontsize=10, labelpad=1)
    ax4.set_xlim(-4, 4); ax4.set_ylim(-4, 4); ax4.set_zlim(-8, 9)
    ax4.tick_params(labelsize=9, pad=0)
    ax4.view_init(elev=22, azim=-55)

    plt.tight_layout()
    output_path = output_dir / "fig2_comparative"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_comparative(Path("src/images"), verbose=True)
