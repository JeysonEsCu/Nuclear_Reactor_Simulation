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
    
    absorber_rods = [
        ControlRod(x_position=x_rod1, y_position=y_rod1, width=width, depth=depth, height=height, label="Absorber\nA"), 
        ControlRod(x_position=x_rod2, y_position=y_rod2, width=width, depth=depth, height=height, label="Absorber\nB"), 
        ControlRod(x_position=x_rod3, y_position=y_rod3, width=width, depth=depth, height=height, label="Absorber\nC"), 
    ]

    # plot all the rods
    for rod in absorber_rods:
        reactor.add(rod)
        
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

    # Create sliders (one for each rod)
    sliders = []
    slider_xpos   = 0.80
    slider_ypos   = 0.25  # starting position of first slider
    slider_height = 0.40    # initial high of the rods
    slider_width  = 0.03

    fig.text(slider_xpos + 0.065, slider_ypos + slider_height + 0.05 + 0.01,
         "Control Rod Heights", color="black", ha="center", fontsize=10)
    for rod in absorber_rods:
        ax_slider = fig.add_axes([slider_xpos, slider_ypos, slider_width, slider_height])
        slider = Slider(
            ax_slider,
            label=f"{rod.label}",
            valmin=0.0,
            valmax=reactor.height,
            valinit=0.0, #rod.height,
            orientation='vertical',
            color="gray"
        )
        sliders.append(slider)
        slider_xpos += slider_width + 0.03  # move next slider left

    # Slider update handler
    def update(_):
        ax.cla()  # clear drawing
        ax.set_xlim(0, reactor.width)
        ax.set_ylim(0, reactor.depth)
        ax.set_zlim(0, reactor.height)

        # Apply slider values to rod heights
        for slider, rod in zip(sliders, absorber_rods):
            rod.set_height(slider.val)

        # Redraw reactor with updated rod heights
        reactor.draw(ax)
        fig.canvas.draw_idle()

    for slider in sliders:
        slider.on_changed(update)

    plt.show()

if __name__ == "__main__":
    main()
