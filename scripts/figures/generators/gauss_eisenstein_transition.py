import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add parent directory to path for imports
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from generators import register
from utils import save_figure, PHI

@register("gauss_eisenstein_transition")
def generate_transition(output_dir: Path, verbose: bool = False) -> None:
    """
    Shows the transition from Eisenstein symmetry (120 deg) to Gauss symmetry (90 deg).
    """
    if verbose:
        print("  Generating Gauss-Eisenstein transition figure...")

    fig = plt.figure(figsize=(12, 6))
    
    # Panel 1: Eisenstein Eigenvalues
    ax1 = fig.add_subplot(1, 2, 1)
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(0.5*np.cos(theta), 0.5*np.sin(theta), 'k--', lw=0.8, alpha=0.3)
    
    angles = [0, 2*np.pi/3, 4*np.pi/3]
    colors = ['red', 'green', 'blue']
    labels = [r'$\lambda_0$', r'$\lambda_1$', r'$\lambda_2$']
    
    for ang, col, lbl in zip(angles, colors, labels):
        x, y = 0.5*np.cos(ang), 0.5*np.sin(ang)
        ax1.scatter(x, y, color=col, s=150, edgecolors='black', zorder=10)
        ax1.text(x*1.4, y*1.4, lbl, fontsize=16, fontweight='bold', ha='center')
    
    # Draw triangle
    tri_x = [0.5*np.cos(a) for a in angles + [angles[0]]]
    tri_y = [0.5*np.sin(a) for a in angles + [angles[0]]]
    ax1.plot(tri_x, tri_y, 'k-', lw=1.5, alpha=0.6)
    
    ax1.set_title("EISENSTEIN: $120^\circ$ Symmetry", fontsize=14, pad=10)
    ax1.set_xlim(-1, 1); ax1.set_ylim(-1, 1)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)
    ax1.set_xlabel("Re", fontsize=12); ax1.set_ylabel("Im", fontsize=12)

    # Panel 2: Gauss Lattice
    ax2 = fig.add_subplot(1, 2, 2)
    M = 1.0
    for i in range(-2, 3):
        for j in range(-2, 3):
            ax2.scatter(i*M, j*M, color='gray', s=30, alpha=0.4)
    
    # Square cell
    rect = plt.Rectangle((0,0), M, M, color='cyan', alpha=0.2, ec='blue', lw=2)
    ax2.add_patch(rect)
    ax2.text(0.5, 0.5, r'$90^\circ$', fontsize=16, ha='center', va='center', fontweight='bold', color='blue')
    
    ax2.set_title("GAUSS: $90^\circ$ Lattice", fontsize=14, pad=10)
    ax2.set_xlim(-2.5, 2.5); ax2.set_ylim(-2.5, 2.5)
    ax2.set_aspect('equal')
    ax2.grid(True, alpha=0.2)
    ax2.set_xlabel("u", fontsize=12); ax2.set_ylabel("v", fontsize=12)

    plt.tight_layout()
    output_path = output_dir / "gauss_eisenstein_transition"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_transition(Path("src/images"), verbose=True)
