import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

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

@register("cylinder_lattice_lateral")
def generate_lateral(output_dir: Path, verbose: bool = False) -> None:
    if verbose: print("  Generating cylinder-lattice lateral figure...")
    fig = plt.figure(figsize=(18, 6))
    
    # Lateral view Cylinder
    ax1 = fig.add_subplot(131)
    y_line = np.linspace(-4, 4, 100)
    ax1.plot(y_line, PHI*y_line, 'purple', lw=2.5, label=r'$z = \phi y$')
    ax1.scatter([P_cyl[1], C_cyl[1], F_cyl[1]], [P_cyl[2], C_cyl[2], F_cyl[2]], c=['red','green','blue'], s=150, edgecolors='black', zorder=10)
    
    # Larger text for labels
    ax1.text(P_cyl[1]+0.3, P_cyl[2]+0.3, 'P', fontsize=14, fontweight='bold', color='red')
    ax1.text(C_cyl[1]+0.3, C_cyl[2]+0.3, 'C', fontsize=14, fontweight='bold', color='green')
    ax1.text(F_cyl[1]+0.3, F_cyl[2]-0.8, 'F', fontsize=14, fontweight='bold', color='blue')
    
    ax1.set_xlim(-5, 5); ax1.set_ylim(-8, 8); ax1.set_aspect('equal')
    ax1.set_xlabel('y (Im)', fontsize=12)
    ax1.set_ylabel('z', fontsize=12)
    ax1.tick_params(labelsize=10)

    # Lateral view Lattice
    ax2 = fig.add_subplot(132)
    for n2 in range(-2, 3):
        v, w = n2*M_vis, PHI*n2*M_vis
        ax2.scatter(v, w, c='cyan', s=80, marker='D', edgecolors='blue')
    ax2.plot([0, M_vis], [0, PHI*M_vis], 'b-', lw=3.5)
    
    ax2.set_xlim(-5, 5); ax2.set_ylim(-8, 8); ax2.set_aspect('equal')
    ax2.set_xlabel('v (Im)', fontsize=12)
    ax2.set_ylabel('w', fontsize=12)
    ax2.tick_params(labelsize=10)

    # Isometric view Lattice
    ax3 = fig.add_subplot(133, projection='3d')
    for n1 in range(-2, 3):
        for n2 in range(-2, 3):
            ax3.scatter(n1*M_vis, n2*M_vis, PHI*n2*M_vis, c='cyan', s=60, marker='s', edgecolors='blue')
    v1 = np.array([M_vis, 0, 0]); v2 = np.array([0, M_vis, PHI*M_vis])
    verts = [[np.array([0,0,0]), v1, v1+v2, v2]]
    ax3.add_collection3d(Poly3DCollection(verts, alpha=0.4, facecolor='cyan', edgecolor='blue', lw=2))
    
    ax3.set_xlabel('u', fontsize=12)
    ax3.set_ylabel('v', fontsize=12)
    ax3.set_zlabel('w', fontsize=12)
    ax3.tick_params(labelsize=10)
    ax3.view_init(elev=45, azim=0)

    plt.tight_layout()
    output_path = output_dir / "cylinder_lattice_lateral"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_lateral(Path("src/images"), verbose=True)
