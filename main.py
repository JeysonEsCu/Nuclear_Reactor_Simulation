from __future__ import annotations
# main.py
"""
Demo: Create a rectangular reactor and control multiple rods with sliders.
"""

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from src.area_reactor import ReactorArea


def main():
    # Create reactor
    reactor = ReactorArea(width=10, depth=6, height=8)

    # Set up
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim(0, reactor.width)
    ax.set_ylim(0, reactor.depth)
    ax.set_zlim(0, reactor.height)
    ax.set_facecolor("black")
    fig.patch.set_facecolor("black")

    # Draw once initially
    reactor.draw(ax)

    plt.show()


if __name__ == "__main__":
    main()
