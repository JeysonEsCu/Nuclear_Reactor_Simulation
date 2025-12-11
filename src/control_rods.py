from __future__ import annotations
# control_rod.py
"""
Defines a simple control rod object that can be placed inside the reactor.
"""
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class ControlRod:
    """
    Represents a vertical rectangular control rod inside the reactor.
    Can also be used as a monitor with fixed height and variable base.
    """
    def __init__(self, x_position: float, y_position: float, width: float, 
             depth: float, height: float, color_rod: str, label: str, 
             base_height: float = 0.0):


        """
        Args:
            x_position, y_position: Horizontal base center position of the rod.
            height: Height of the rod (total vertical size).
            width: Width of the rectangular rod.
            depth: Depth of the rectangular rod.
            label: Identifier label.
            base_height: Optional Z-position of the base (default 0.0). 
                         Useful for monitors that move up and down.
        """
        self.x_position = x_position
        self.y_position = y_position
        self.height     = height
        self.width      = width
        self.depth      = depth
        self.label      = label
        self.color_rod  = color_rod
        self.base_height = base_height

    def set_height(self, new_height: float) -> None:
        """Update rod height."""
        self.height = max(new_height, 0.0)

    def set_base_height(self, new_base: float) -> None:
        """Update the vertical position of the base."""
        self.base_height = new_base

    def draw(self, ax: Axes3D) -> None:
        """Draw the rod as a vertical rectangular prism."""

        # Corners, z0 is base, z1 is top
        z0 = self.base_height
        z1 = self.base_height + self.height  # fixed size
        x0, y0 = self.x_position - self.width/2, self.y_position - self.depth/2
        x1, y1 = self.x_position + self.width/2, self.y_position + self.depth/2

        # Define 6 faces (each as list of 4 vertices)
        faces = [
            # bottom
            [(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0)],
            # top
            [(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)],
            # front
            [(x0,y0,z0),(x1,y0,z0),(x1,y0,z1),(x0,y0,z1)],
            # back
            [(x0,y1,z0),(x1,y1,z0),(x1,y1,z1),(x0,y1,z1)],
            # left
            [(x0,y0,z0),(x0,y1,z0),(x0,y1,z1),(x0,y0,z1)],
            # right
            [(x1,y0,z0),(x1,y1,z0),(x1,y1,z1),(x1,y0,z1)],
        ]

        poly3d = Poly3DCollection(faces, facecolors=self.color_rod, alpha=0.35, linewidths=0.5)
        ax.add_collection3d(poly3d)

        # Label above the top of the rod
        ax.text(self.x_position, self.y_position, z1 + 0.2, self.label, color="black")
