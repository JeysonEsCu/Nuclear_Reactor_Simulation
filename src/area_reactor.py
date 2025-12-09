from __future__ import annotations
# area_reactor.py
"""
Defines the reactor area and manages all reactor components.
This module acts as the container. Anything inside the reactor
(control rods, sensors, particles, etc.) attaches here.
"""
from typing import List
from mpl_toolkits.mplot3d import Axes3D  

class ReactorArea:
    """
    A rectangular 3D reactor area that can host control rods or other components.
    """

    def __init__(self, width: float, depth: float, height: float) -> None:
        """
        Args:
            width: Total X-extent of the reactor.
            depth: Total Y-extent of the reactor.
            height: Total Z-extent of the reactor.
        """
        self.width = width
        self.depth = depth
        self.height = height

        # Any component added (rods, sensors, etc.)
        self.components: List[object] = []

    # To add any component in the future
    def add(self, component: object) -> None:
        """Register a component inside the reactor."""
        self.components.append(component)

    def draw_frame(self, ax: Axes3D) -> None:
        """
        Draw the outer wireframe reactor box.
        """
        width, depth, height = self.width, self.depth, self.height
                                                
        # Line segments (pairs of indices)          #    7 ----------6
        edges_of_reactor = [                        #   / |         /|
            (0,1), (1,2), (2,3), (3,0),             #  4--|--------5 |
            (4,5), (5,6), (6,7), (7,4),             #  |  3--------|-2
            (0,4), (1,5), (2,6), (3,7),             #  | /         |/
        ]                                           #  0 ----------1

        # 8 corners of the reactor
        corners = [
            (0, 0, 0), (width, 0, 0), (width, depth, 0), (0, depth, 0), # 0, 1, 2, 3
            (0, 0, height), (width, 0, height), (width, depth, height), # 4, 5, 6,
            (0, depth, height)                                          # 7
        ]

        # Connect the edges of the container (reactor)
        for (i,j) in edges_of_reactor:
            x = [corners[i][0], corners[j][0]]
            y = [corners[i][1], corners[j][1]]
            z = [corners[i][2], corners[j][2]]
            ax.plot(x, y, z, color="white", linewidth=1.2)

    def draw(self, ax: Axes3D) -> None:
        """Draw the frame and all components."""
        self.draw_frame(ax)
        for comp in self.components:
            comp.draw(ax)
