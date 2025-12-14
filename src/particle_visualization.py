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

def add_energy_colorbar(fig, energy_distribution, cmap_name="turbo", label="Neutron Energy [MeV]"):
    """
    Adds a single horizontal colorbar for the energy range.
    """
    if energy_distribution is None or len(energy_distribution) == 0:
        return None

    cmap = cm.get_cmap(cmap_name)
    norm = Normalize(vmin=energy_distribution.min(), vmax=energy_distribution.max())
    # maps colors(cmpas) -> values(norm)
    sm = cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # required for colorbar
    
    # Create a new axes above the plot for the horizontal colorbar
    cax = fig.add_axes([0.2, 0.92, 0.6, 0.03])  # [left, bottom, width, height] in figure coordinates
    cbar = fig.colorbar(sm, cax=cax, orientation="horizontal")
    cbar.set_label(label)
    return cbar
