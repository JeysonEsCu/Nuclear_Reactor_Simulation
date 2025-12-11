from __future__ import annotations
# main.py
"""
Demo: Create a rectangular reactor and control multiple rods with sliders.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D

from src.area_reactor import ReactorArea
from src.control_rods import ControlRod
from src.neutron_monitor_flux import NeutronMonitor

def main():
    # Create reactor, library from src/
    reactor = ReactorArea(width=10, depth=10, height=8)
    
    # Create any number of control rods from src/control_rods.py at specific height.
    # all the rods (nuclear fuel, neutron absorbers and other) 
    # will have the same width and depth.
    width = 1.9
    depth = 1.9
    # position of the absorber rods
    x_rod1, y_rod1 = 3, 3
    x_rod2, y_rod2 = 5, 5
    x_rod3, y_rod3 = 7, 7
    height         = 0
    # position and height of nuclear fuel
    x_fuel1, y_fuel1 = 5, 7
    x_fuel2, y_fuel2 = 7, 9
    height_reactor = 8
    # geometry and position of neutron flux monitor
    width_flux_mon = 0.95
    depth_flux_mon = 0.95
    x_flux_monitor1, y_flux_monitor1 = 7, 3
    
    absorber_rods = [
        ControlRod(x_position=x_rod1, y_position=y_rod1, width=width, depth=depth, 
                   height=height, color_rod="blue", label="Absorber\nA"), 
        ControlRod(x_position=x_rod2, y_position=y_rod2, width=width, depth=depth, 
                   height=height, color_rod="blue", label="Absorber\nB"), 
        ControlRod(x_position=x_rod3, y_position=y_rod3, width=width, depth=depth, 
                   height=height, color_rod="blue", label="Absorber\nC"), 
    ]
    
    nuclear_fuel_rods = [
        ControlRod(x_position=x_fuel1, y_position=y_fuel1, width=width, depth=depth, 
                   height=height_reactor, color_rod="green", label="fuel1"),
        ControlRod(x_position=x_fuel2, y_position=y_fuel2, width=width, depth=depth, 
                   height=height_reactor, color_rod="green", label="fuel2")
    ]
    
    neutron_flux_monitor = [
        NeutronMonitor(x_position=x_flux_monitor1, y_position=y_flux_monitor1, 
                       width=width_flux_mon, depth=depth_flux_mon, height=0, #height_reactor, 
                       base_height=0.0, color_rod="gray", label="flux")
    ]

    # plot all the rods
    for rod in absorber_rods + nuclear_fuel_rods + neutron_flux_monitor:
        reactor.add(rod)
#    for rod in nuclear_fuel_rods:
#        reactor.add(rod)
#    for rod in neutron_flux_monitor:
#        reactor.add(rod)
        
    # Set up
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(0, reactor.width)
    ax.set_ylim(0, reactor.depth)
    ax.set_zlim(0, reactor.height)
    ax.set_facecolor("white")
    fig.patch.set_facecolor("white")

    # Draw once initially
    reactor.draw(ax)

    slider_xpos   = 0.80
    slider_ypos   = 0.25    # starting position of first slider
    slider_height = 0.40    # initial high of the rods
    slider_width  = 0.03

    fig.text(slider_xpos + 0.13, slider_ypos + slider_height + 0.05 + 0.01,
         "Control Rod Heights", color="black", ha="center", fontsize=10)
    
    # sliders absorbers
    sliders_absorber = []
    for rod in absorber_rods:
        ax_slider = fig.add_axes([slider_xpos, slider_ypos, slider_width, slider_height])
        slider = Slider(
            ax_slider,
            label=f"{rod.label}",
            valmin=0.0,
            valmax=reactor.height,
            valinit=0.0, #rod.height,
            orientation='vertical',
            color="blue"
        )
        sliders_absorber.append(slider)
        slider_xpos += slider_width + 0.015  # move next slider left

    # sliders monitors
    sliders_monitors = []

    for i, monitor in enumerate(neutron_flux_monitor):
        ax_slider_monitor = fig.add_axes([0.1, 0.25 + i*0.45, 0.03, 0.40])
        slider_mon = Slider(
            ax_slider_monitor,
            label=f"{monitor.label}",
            valmin=0.0,
            valmax=reactor.height, #- monitor.height,
            valinit=0, #monitor.base_height,
            orientation='vertical',
            color="gray"
        )
        sliders_monitors.append(slider_mon)

    # Slider update handler
    def update_all(val):
        ax.cla()  # clear drawing
        ax.set_xlim(0, reactor.width)
        ax.set_ylim(0, reactor.depth)
        ax.set_zlim(0, reactor.height)

        # update absorbers
        for s, rod in zip(sliders_absorber, absorber_rods):
            rod.set_height(s.val)

        # update monitors
        for s, m in zip(sliders_monitors, neutron_flux_monitor):
            m.base_height = s.val

        # redraw everything
        reactor.draw(ax)
        fig.canvas.draw_idle()

    # connect all sliders
    for s in sliders_absorber:
        s.on_changed(update_all)

    for s in sliders_monitors:
        s.on_changed(update_all)

    plt.show()

if __name__ == "__main__":
    main()
