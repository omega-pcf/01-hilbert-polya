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

# Constants
R0 = 3
M_vis = 2
P_cyl = np.array([3, 0, 0])
C_cyl = np.array([-1.5, 2.598, PHI * 2.598])
F_cyl = np.array([-1.5, -2.598, PHI * (-2.598)])

@register("cylinder_lattice_top")
def generate_top(output_dir: Path, verbose: bool = False) -> None:
    if verbose: print("  Generating cylinder-lattice top figure...")
    fig = plt.figure(figsize=(18, 6))
    
    # Top view Cylinder
    ax1 = fig.add_subplot(131)
    theta = np.linspace(0, 2*np.pi, 100)
    ax1.plot(R0*np.cos(theta), R0*np.sin(theta), 'b-', lw=2)
    ax1.fill(R0*np.cos(theta), R0*np.sin(theta), alpha=0.1, color='blue')
    ax1.scatter([P_cyl[0], C_cyl[0], F_cyl[0]], [P_cyl[1], C_cyl[1], F_cyl[1]], c=['red','green','blue'], s=150, edgecolors='black', zorder=10)
    
    # Larger text for vertices
    ax1.text(P_cyl[0]+0.3, P_cyl[1], 'P', fontsize=14, fontweight='bold', color='red')
    ax1.text(C_cyl[0]-0.8, C_cyl[1]+0.3, 'C', fontsize=14, fontweight='bold', color='green')
    ax1.text(F_cyl[0]-0.8, F_cyl[1]-0.5, 'F', fontsize=14, fontweight='bold', color='blue')
    
    ax1.set_xlim(-4, 4); ax1.set_ylim(-4, 4); ax1.set_aspect('equal')
    ax1.set_xlabel('x (Re)', fontsize=12)
    ax1.set_ylabel('y (Im)', fontsize=12)
    ax1.tick_params(labelsize=10)

    # Top view Lattice
    ax2 = fig.add_subplot(132)
    for n1 in range(-2, 3):
        for n2 in range(-2, 3):
            ax2.scatter(n1*M_vis, n2*M_vis, c='cyan', s=80, marker='s', edgecolors='blue')
    ax2.add_patch(plt.Rectangle((0, 0), M_vis, M_vis, alpha=0.2, color='cyan', ec='blue', lw=2.5))
    
    # Larger axis labels
    ax2.set_xlim(-4, 4); ax2.set_ylim(-4, 4); ax2.set_aspect('equal')
    ax2.set_xlabel('u (Re)', fontsize=12)
    ax2.set_ylabel('v (Im)', fontsize=12)
    ax2.tick_params(labelsize=10)

    # Top view Superposition
    ax3 = fig.add_subplot(133)
    scale = M_vis / R0
    ax3.plot(R0*scale*np.cos(theta), R0*scale*np.sin(theta), 'purple', lw=2.5)
    ax3.scatter([P_cyl[0]*scale, C_cyl[0]*scale, F_cyl[0]*scale], [P_cyl[1]*scale, C_cyl[1]*scale, F_cyl[1]*scale], c=['red','green','blue'], s=100, edgecolors='black', zorder=10)
    
    ax3.set_xlim(-4, 4); ax3.set_ylim(-4, 4); ax3.set_aspect('equal')
    ax3.set_xlabel('x/u (Re)', fontsize=12)
    ax3.set_ylabel('y/v (Im)', fontsize=12)
    ax3.tick_params(labelsize=10)

    plt.tight_layout()
    output_path = output_dir / "cylinder_lattice_top"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_top(Path("src/images"), verbose=True)
