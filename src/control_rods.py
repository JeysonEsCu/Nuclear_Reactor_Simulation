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
    """

    def __init__(self, x_position: float, y_position: float, width: float, 
                 depth: float, height: float, color_rod: str, label: str):
        """
        Args:
            x_position, y_position: Horizontal base center position of the rod.
            height: Initial rod height (how much it is inserted).
            width: Width of the rectangular rod.
            depth: Depth of the rectangular rod.
            label: Identifier label.
        """
        self.x_position = x_position
        self.y_position = y_position
        self.height     = height
        self.width      = width
        self.depth      = depth
        self.label      = label
        self.color_rod  = color_rod

    def set_height(self, new_height: float) -> None:
        """Update rod height."""
        self.height = max(new_height, 0.0)

    def draw(self, ax: Axes3D) -> None:
        """Draw the rod as a vertical rectangular prism."""

        # Corners
        x0, y0, z0 = self.x_position - self.width/2, self.y_position - self.depth/2, 0
        x1, y1, z1 = self.x_position + self.width/2, self.y_position + self.depth/2, self.height

        # Define 6 faces (each as list of 4 vertices)
        faces = [
            # bottom
            [(x0,y0,0),(x1,y0,0),(x1,y1,0),(x0,y1,0)],
            # top
            [(x0,y0,self.height),(x1,y0,self.height),(x1,y1,self.height),(x0,y1,self.height)],
            # front
            [(x0,y0,0),(x1,y0,0),(x1,y0,self.height),(x0,y0,self.height)],
            # back
            [(x0,y1,0),(x1,y1,0),(x1,y1,self.height),(x0,y1,self.height)],
            # left
            [(x0,y0,0),(x0,y1,0),(x0,y1,self.height),(x0,y0,self.height)],
            # right
            [(x1,y0,0),(x1,y1,0),(x1,y1,self.height),(x1,y0,self.height)],
        ]

        poly3d = Poly3DCollection(faces, facecolors=self.color_rod, alpha=0.35, linewidths=0.5)
        ax.add_collection3d(poly3d)

        # Label
        ax.text(self.x_position, self.y_position, self.height + 0.2, self.label, color="black")
