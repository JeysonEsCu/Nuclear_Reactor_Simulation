from __future__ import annotations
"""
Demo: Create a rectangular reactor with control rods, fuel, flux monitors,
and a simple moving particle (neutron) demo with sliders.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

from src.area_reactor import ReactorArea
from src.control_rods import ControlRod
from src.neutron_monitor_flux import NeutronMonitor
from src.particle_manager import ParticleManager
from src.particle_visualization import draw_particles
from src.reactor_builder import populate_reactor

def main():
    # Create reactor
    # src/area_reactor.py
    reactor = ReactorArea(width=10, depth=10, height=8)
    
    # --------------------------
    # width and depth of the grid in the reactor
    # --------------------------
    width = 1.9
    depth = 1.9

    # --------------------------
    # Flux monitors geometry
    # --------------------------
    monitor_height = 0.95
    width_flux_mon = 0.95
    depth_flux_mon = 0.95
    
    # --------------------------
    # Rods coordinates: grid position (x, y)
    # --------------------------
    # absorbers
    absorber1 = (3, 3)
    absorber2 = (5, 5)
    absorber3 = (7, 7)
    height_absorber = 0
    
    # Fuel
    fuel1 = (5, 7)
    fuel2 = (7, 9)
    height_reactor = reactor.height

    # flux monitor
    monitor1 = (7, 3)

    # --------------------------
    # Create objects
    # --------------------------
    # src/control_rods.py
    # src/neutron_monitor_flux.py
    absorber_rods = [
        ControlRod(absorber1[0], absorber1[1], width, depth, height_absorber, "blue", "Absorber\nA"),
        ControlRod(absorber2[0], absorber2[1], width, depth, height_absorber, "blue", "Absorber\nB"),
        ControlRod(absorber3[0], absorber3[1], width, depth, height_absorber, "blue", "Absorber\nC")
    ]

    nuclear_fuel_rods = [
        ControlRod(fuel1[0], fuel1[1], width, depth, height_reactor, "green", "fuel1"),
        ControlRod(fuel2[0], fuel2[1], width, depth, height_reactor, "green", "fuel2")
    ]

    neutron_flux_monitor = [
        NeutronMonitor(monitor1[0], monitor1[1], width_flux_mon, depth_flux_mon, monitor_height, "gray", "flux\nA")
    ]
    # Add all objects to reactor
    reactor_elements = absorber_rods + nuclear_fuel_rods + neutron_flux_monitor
    populate_reactor(reactor, reactor_elements)

    # Particle system
    particle_manager = ParticleManager()
    for fuel in nuclear_fuel_rods:
        for _ in range(5):  # particles per fuel
            particle_manager.spawn(
                position=np.array([fuel.x_position, fuel.y_position, reactor.height / 2]),
                velocity=np.random.uniform(-0.3, 0.3, size=3),
                energy=2.0
            )

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
    draw_particles(ax, particle_manager)

    # --------------------------
    # Sliders
    # --------------------------
    # Absorbers
    abs_slider_xpos = 0.80
    abs_slider_ypos = 0.25
    abs_slider_width = 0.03
    abs_slider_height = 0.40

    fig.text(abs_slider_xpos + 0.13,
             abs_slider_ypos + abs_slider_height + 0.06,
             "Control Rod Heights",
             ha="center")

    sliders_absorber = []
    for rod in absorber_rods:
        ax_slider = fig.add_axes([abs_slider_xpos, abs_slider_ypos, abs_slider_width, abs_slider_height])
        slider = Slider(ax_slider, rod.label, valmin=0.0, valmax=reactor.height, valinit=0.0, orientation="vertical", color="blue")
        sliders_absorber.append(slider)
        abs_slider_xpos += abs_slider_width + 0.015

    # Flux monitors
    flux_slider_xpos = 0.10
    flux_slider_ypos = 0.25
    flux_slider_width = 0.03
    flux_slider_height = 0.40

    fig.text(flux_slider_xpos,
             flux_slider_ypos + flux_slider_height + 0.06,
             "Flux Monitor Heights",
             ha="center")

    sliders_monitors = []
    for monitor in neutron_flux_monitor:
        ax_slider = fig.add_axes([flux_slider_xpos, flux_slider_ypos, flux_slider_width, flux_slider_height])
        slider = Slider(ax_slider, monitor.label, valmin=0.0, valmax=reactor.height - monitor.height, valinit=0.0, orientation="vertical", color="gray")
        sliders_monitors.append(slider)

    # --------------------------
    # Animation and slider update
    # --------------------------
    animation_running = False

    def update_all(val=None):
        ax.cla()
        ax.set_xlim(0, reactor.width)
        ax.set_ylim(0, reactor.depth)
        ax.set_zlim(0, reactor.height)

        # Update rods from sliders
        for s, rod in zip(sliders_absorber, absorber_rods):
            rod.set_height(s.val)
        for s, m in zip(sliders_monitors, neutron_flux_monitor):
            m.base_height = s.val

        # Move particles
        if animation_running:
            dt = 0.05
            for particle in particle_manager.particles:
                if particle.alive:
                    particle.move(dt)
                    # Wall collisions
                    limits = [reactor.width, reactor.depth, reactor.height]
                    for i in range(3):
                        if particle.position[i] < 0:
                            particle.position[i] = 0
                            particle.velocity[i] *= -1
                        elif particle.position[i] > limits[i]:
                            particle.position[i] = limits[i]
                            particle.velocity[i] *= -1

        # Redraw
        reactor.draw(ax)
        draw_particles(ax, particle_manager)
        fig.canvas.draw_idle()

    # Connect sliders
    for s in sliders_absorber + sliders_monitors:
        s.on_changed(update_all)

    # --------------------------
    # Keyboard: space = toggle animation
    # --------------------------
    def on_key(event):
        nonlocal animation_running
        if event.key == " ":
            animation_running = not animation_running

    fig.canvas.mpl_connect("key_press_event", on_key)

    # --------------------------
    # Main loop
    # --------------------------
    while plt.fignum_exists(fig.number):
        update_all()
        plt.pause(0.05)

    plt.show()

if __name__ == "__main__":
    main()
