"""
PCF hypercube multiple views figure generator.

Shows 8 different perspectives of the PCF hypercube with nested cubes
growing as φ^σ, demonstrating the structure from various angles.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import sys
from pathlib import Path as PathLib
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.ticker import MaxNLocator

_parent_dir = PathLib(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from generators import register
from utils import save_figure, PHI

# Constants
epsilon_0 = np.log(PHI) / (6 * np.sqrt(3))
M_PCF = np.pi / epsilon_0

# Colors for each level
colors = {
    0: '#2980b9',  # blue
    1: '#27ae60',  # green
    2: '#f39c12',  # orange
    3: '#e74c3c',  # red
    4: '#9b59b6',  # purple
}


def draw_3d_cube(ax, origin, size, color, alpha_face=0.1, alpha_edge=0.7, lw=2):
    """Draw a 3D cube with semi-transparent faces and solid edges."""
    o = np.array(origin)
    s = size
    
    # Vertices
    v = np.array([
        [0, 0, 0], [s, 0, 0], [s, s, 0], [0, s, 0],
        [0, 0, s], [s, 0, s], [s, s, s], [0, s, s]
    ]) + o
    
    # Faces
    faces = [
        [v[0], v[1], v[2], v[3]],  # bottom
        [v[4], v[5], v[6], v[7]],  # top
        [v[0], v[1], v[5], v[4]],  # front
        [v[2], v[3], v[7], v[6]],  # back
        [v[0], v[3], v[7], v[4]],  # left
        [v[1], v[2], v[6], v[5]]   # right
    ]
    
    ax.add_collection3d(Poly3DCollection(faces, alpha=alpha_face, 
                                          facecolor=color, edgecolor='none'))
    
    # Edges
    edges = [
        [v[0], v[1]], [v[1], v[2]], [v[2], v[3]], [v[3], v[0]],
        [v[4], v[5]], [v[5], v[6]], [v[6], v[7]], [v[7], v[4]],
        [v[0], v[4]], [v[1], v[5]], [v[2], v[6]], [v[3], v[7]]
    ]
    
    for edge in edges:
        ax.plot3D(*zip(*edge), color=color, linewidth=lw, alpha=alpha_edge)


@register("hypercube_views")
def generate_hypercube_views(output_dir: Path, verbose: bool = False) -> None:
    """
    Generate figure showing 8 different perspectives of the hypercube.
    
    Args:
        output_dir: Directory where to save the figure
        verbose: If True, show additional information
    """
    if verbose:
        print("  Generating hypercube views figure...")
    
    fig = plt.figure(figsize=(20, 16))
    
    # 8 different views
    views = [
        (20, 35),   # Standard view
        (20, 125),  # Rotated 90°
        (20, 215),  # Rotated 180°
        (20, 305),  # Rotated 270°
        (90, 0),    # Top view
        (0, 0),     # Front view
        (0, 90),    # Side view
        (45, 45),   # Isometric view
    ]
    
    for idx, (elev, azim) in enumerate(views):
        ax = fig.add_subplot(2, 4, idx + 1, projection='3d')
        
        # Orthographic views (top, front, side) - idx 4, 5, 6
        is_orthographic = idx in [4, 5, 6]  # Top view, Front view, Side view
        
        if is_orthographic:
            # Use orthographic projection for flat views
            ax.set_proj_type('ortho')
        
        # Draw nested cubes
        for sigma in range(4):
            M_sigma = (PHI ** sigma) * M_PCF
            draw_3d_cube(ax, (0, 0, 0), M_sigma, colors[sigma], 
                        alpha_face=0.1, alpha_edge=0.7, lw=2)
        
        ax.view_init(elev=elev, azim=azim)
        
        # Orthographic views need different labelpad (no depth perception)
        if is_orthographic:
            labelpad = 15  # Moderate spacing for orthographic views (no depth)
        elif idx >= 4:  # Isometric view (idx 7)
            labelpad = 20  # More spacing for isometric view
        else:
            labelpad = 10  # Normal spacing for first row
        
        ax.set_xlabel('$u$', fontsize=16, labelpad=labelpad)
        ax.set_ylabel('$v$', fontsize=16, labelpad=labelpad)
        ax.set_zlabel('$w$', fontsize=16, labelpad=labelpad)
        
        # Reduce number of ticks and their size
        ax.xaxis.set_major_locator(MaxNLocator(3))  # Max 3 ticks instead of default
        ax.yaxis.set_major_locator(MaxNLocator(3))
        ax.zaxis.set_major_locator(MaxNLocator(3))
        ax.tick_params(labelsize=10)  # Smaller tick labels
    
    plt.tight_layout()
    
    # Save figure with descriptive name matching generator
    output_path_pdf = output_dir / "hypercube_views.pdf"
    output_path_png = output_dir / "hypercube_views.png"
    fig.savefig(output_path_pdf, bbox_inches='tight', pad_inches=0.01)
    fig.savefig(output_path_png, dpi=200, bbox_inches='tight', pad_inches=0.01)
    plt.close(fig)
    
    if verbose:
        print("  ✓ Hypercube views figure generated")

