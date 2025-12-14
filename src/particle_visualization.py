from __future__ import annotations
# particle_visualization.py
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import Normalize


def draw_particles(ax, particle_manager, energy_distribution: list, 
                   cmap_name: str="turbo") -> None:
    """
    Draw only current positions of particles (no trajectories).
        cmap_name : Matplotlib colormap name (e.g. 'turbo', 'bwr', 'coolwarm')
        
    """
    if energy_distribution is None or len(energy_distribution) == 0:
        return
    
    # Colormap and normalization
    cmap = cm.get_cmap(cmap_name)
    norm = Normalize(vmin=energy_distribution.min(), vmax=energy_distribution.max())
    
    for particle in particle_manager.particles:
        if not particle.alive:
            continue
        # Normalize energy in color space
        color = cmap(norm(particle.energy))
        ax.scatter(
            particle.position[0],
            particle.position[1],
            particle.position[2],
            color=color,
            s=10
        )
