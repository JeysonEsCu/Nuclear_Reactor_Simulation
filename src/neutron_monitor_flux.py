# neutron_monitor_flux.py
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from src.control_rods import ControlRod

# It uses all the attributes and methods from the ControlRod class
class NeutronMonitor(ControlRod):
    """
    Rectangular neutron detector box.
    Inherits drawing logic from ControlRod but has a fixed height (size)
    and can move its base height along Z-axis.
    """
    # Call the construct ControlRod and reuse the logic    
    def __init__(self, x_position: float, y_position: float, width: float, 
                 depth: float, height: float, color_rod: str, label: str = "Monitor"):
        """
        Args:
            height: the fixed Z-size of the monitor
        """
        # From ControlRod
        super().__init__(x_position, y_position, width, depth, height, color_rod, label)

        # More attribute, only for NeutronMonitor
        self.base_height = 0.0      # bottom position along Z
    
    # New attributes:
    def set_base_height(self, new_base: float):
        """Update the vertical position of the monitor."""
        self.base_height = new_base

    # Compacting by using the attributes from the ControlRod class
    def draw(self, ax: Axes3D) -> None:
        """Plot the monitor at fixed height with variable base."""
        # Do NOT modify self.height here
        z0 = self.base_height
        z1 = self.base_height + self.height
        x0, y0 = self.x_position - self.width/2, self.y_position - self.depth/2
        x1, y1 = self.x_position + self.width/2, self.y_position + self.depth/2

        # Define 6 faces (each as list of 4 vertices)
        faces = [
            [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0)],  # bottom
            [(x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)],  # top
            [(x0, y0, z0), (x1, y0, z0), (x1, y0, z1), (x0, y0, z1)],  # front
            [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],  # back
            [(x0, y0, z0), (x0, y1, z0), (x0, y1, z1), (x0, y0, z1)],  # left
            [(x1, y0, z0), (x1, y1, z0), (x1, y1, z1), (x1, y0, z1)],  # right
        ]

        poly3d = Poly3DCollection(faces, facecolors=self.color_rod, alpha=0.35, linewidths=0.5)
        ax.add_collection3d(poly3d)

        # Label above the top of the monitor
        ax.text(self.x_position, self.y_position, z1 + 0.2, self.label, color="black")