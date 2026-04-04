import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.ticker import MaxNLocator

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

@register("cylinder_lattice_3d")
def generate_3d(output_dir: Path, verbose: bool = False) -> None:
    if verbose: print("  Generating cylinder-lattice 3D figure...")
    fig = plt.figure(figsize=(18, 6))
    
    # Cylinder 3D
    ax1 = fig.add_subplot(131, projection='3d')
    theta = np.linspace(0, 2*np.pi, 50); z_surf = np.linspace(-6, 6, 30)
    Theta, Z = np.meshgrid(theta, z_surf)
    ax1.plot_surface(R0*np.cos(Theta), R0*np.sin(Theta), Z, alpha=0.15, color='lightblue')
    ax1.plot(R0*np.cos(theta), R0*np.sin(theta), 0, 'b-', lw=2)
    ax1.scatter(*P_cyl, c='red', s=150, edgecolors='black', zorder=10)
    ax1.scatter(*C_cyl, c='green', s=150, edgecolors='black', zorder=10)
    ax1.scatter(*F_cyl, c='blue', s=150, edgecolors='black', zorder=10)
    # Labels P, C, F Enlarged
    ax1.text(P_cyl[0]+0.5, P_cyl[1], P_cyl[2]+0.5, 'P', fontsize=16, fontweight='bold', color='red')
    ax1.text(C_cyl[0]-0.8, C_cyl[1], C_cyl[2]+0.8, 'C', fontsize=16, fontweight='bold', color='green')
    ax1.text(F_cyl[0]-0.8, F_cyl[1], F_cyl[2]-0.8, 'F', fontsize=16, fontweight='bold', color='blue')
    
    ax1.view_init(elev=20, azim=45)
    ax1.set_xlabel('x', fontsize=12)
    ax1.set_ylabel('y', fontsize=12)
    ax1.set_zlabel('z', fontsize=12)
    ax1.tick_params(labelsize=10)

    # Lattice 3D
    ax2 = fig.add_subplot(132, projection='3d')
    for n1 in range(-2, 3):
        for n2 in range(-2, 3):
            ax2.scatter(n1*M_vis, n2*M_vis, PHI*n2*M_vis, c='cyan', s=80, edgecolors='blue', marker='s')
    v1 = np.array([M_vis, 0, 0]); v2 = np.array([0, M_vis, PHI*M_vis])
    verts = [[np.array([0,0,0]), v1, v1+v2, v2]]
    ax2.add_collection3d(Poly3DCollection(verts, alpha=0.3, facecolor='cyan', edgecolor='blue', lw=2))
    
    # Larger axis labels
    ax2.set_xlabel('u', fontsize=12)
    ax2.set_ylabel('v', fontsize=12)
    ax2.set_zlabel('w', fontsize=12)
    ax2.tick_params(labelsize=10)
    ax2.view_init(elev=20, azim=45)

    # Superposition
    ax3 = fig.add_subplot(133, projection='3d')
    scale = M_vis / R0
    ax3.plot_surface(R0*np.cos(Theta)*scale, R0*np.sin(Theta)*scale, Z*scale*0.8, alpha=0.1, color='lightblue')
    for a, b in [(P_cyl, C_cyl), (C_cyl, F_cyl), (F_cyl, P_cyl)]:
        ax3.plot([a[0]*scale, b[0]*scale], [a[1]*scale, b[1]*scale], [a[2]*scale*0.8, b[2]*scale*0.8], 'purple', lw=2.5)
    
    ax3.set_xlabel('x/u', fontsize=12)
    ax3.set_ylabel('y/v', fontsize=12)
    ax3.set_zlabel('z/w', fontsize=12)
    ax3.tick_params(labelsize=10)
    ax3.view_init(elev=20, azim=45)

    plt.tight_layout()
    output_path = output_dir / "cylinder_lattice_3d"
    save_figure(fig, output_path, verbose=verbose)
    plt.close(fig)

if __name__ == "__main__":
    generate_3d(Path("src/images"), verbose=True)
