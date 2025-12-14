from __future__ import annotations
"""
Demo: Create a rectangular reactor with control rods, fuel, flux monitors,
and a simple moving particle (neutron) demo with sliders.
"""

import matplotlib.pyplot as plt
#from matplotlib.widgets import Slider
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

from src.area_reactor import ReactorArea
from src.particle_manager import ParticleManager
from src.particle_visualization import draw_particles, add_energy_colorbar
from src.reactor_builder import element_on_grid, flux_monitor_on_grid, populate_reactor, populate_particles
from src.neutron_energy_distribution import neutron_energy_distribution
from src.simulation_helpers import create_sliders, update_simulation, connect_keyboard

def main():
    # Create reactor        src/area_reactor.py
    reactor = ReactorArea(width=10, depth=10, height=8)
    # width and depth of the grid in the reactor
    width = 1.9
    depth = 1.9
    
    # --------------------------
    # Rods geometry: grid position (x, y)
    # --------------------------
    # absorbers
    absorber_coords = [(3, 3), (5, 5), (7, 7)]
    height_absorber = 0
    
    # Fuel
    fuel_coords = [(5, 7),  (7, 9)]
    height_reactor = reactor.height

    # flux monitor
    monitor_coords = [(7, 3)]
    # Flux monitors dimension
    monitor_height = 0.95
    width_flux_mon = 0.95
    depth_flux_mon = 0.95
    
    # --------------------------
    # Create objects
    # --------------------------
    # src/reactor_builder.py
    absorber_rods = element_on_grid(absorber_coords, width, depth, 
                    height_absorber, "blue", "Abs")
    
    neutron_flux_monitor = element_on_grid(monitor_coords, width_flux_mon, depth_flux_mon, 
                                           monitor_height, "gray", "mon")

    nuclear_fuel_rods = flux_monitor_on_grid(fuel_coords, width, depth, 
                    height_reactor, "green")
    
    # Add all objects to reactor        # src.reactor_builder
    reactor_elements = absorber_rods + nuclear_fuel_rods + neutron_flux_monitor
    populate_reactor(reactor, reactor_elements)
    
    # Manage a collection of particles in the reactor   # src.particle_manager
    particle_manager = ParticleManager()

    # Number of particles at the beginning
    particles_per_fuel = 5
    num_particles = len(nuclear_fuel_rods) * particles_per_fuel
    
    # src.neutron_energy_distribution
    energies = neutron_energy_distribution("debug_uniform", num_particles)
    
    # Particle system
    populate_particles(particle_manager, nuclear_fuel_rods, reactor.height, energies, 
                       particles_per_fuel, 1.0)

    # --------------------------
    # Plot setup
    # --------------------------
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")

    ax.set_xlim(0, reactor.width)
    ax.set_ylim(0, reactor.depth)
    ax.set_zlim(0, reactor.height)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    reactor.draw(ax)
    # particles in a range of colors, the last argument refers the color
    draw_particles(ax, particle_manager, energies, "turbo")
    
    # Add colorbar
    add_energy_colorbar(fig, energies, "turbo")

    # --------------------------
    # Sliders
    # --------------------------
    # Absorbers
    absorber_slider_position = (0.80, 0.25)     # (x, y)
    absorber_slider_dimension = (0.03, 0.40)    # (height, width)
    # flux monitor
    monitor_slider_position = (0.10, 0.25) 
    monitor_slider_dimension = (0.03, 0.40)
    
    absorber_slider = create_sliders(fig, absorber_rods, 
                   absorber_slider_position, absorber_slider_dimension, 
                   reactor.height, "Control Rod Heights", "blue")
    
    monitor_slider = create_sliders(fig, neutron_flux_monitor, 
                   monitor_slider_position, monitor_slider_dimension, 
                   reactor.height - monitor_height, "Monitor flux position", "gray")

    # --------------------------
    # Animation and slider update
    # --------------------------
    animation_state = {"running": False}
    connect_keyboard(fig, animation_state)
    
    animation = FuncAnimation(fig, lambda frame: update_simulation(
        ax, fig, reactor, particle_manager, absorber_slider + monitor_slider, 
        absorber_rods, monitor_slider, neutron_flux_monitor, animation_state, 
        energies, dt=0.05), interval = 50)
    
    plt.show()

if __name__ == "__main__":
    main()
