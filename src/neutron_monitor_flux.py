# neutron_monitor_flux.py
from mpl_toolkits.mplot3d import Axes3D
from src.control_rods import ControlRod

# It uses all the attributes and methods from the ControlRod class
class NeutronMonitor(ControlRod):
    """
    Rectangular detector box to measure neutron flux.
    Inherits from ControlRod but allows to specify base height.
    """
    def __init__(self, x_position: float, y_position: float, base_height: float,
                 width: float, depth: float, height: float, color_rod: str, label: str = "Monitor"):
        super().__init__(x_position, y_position, width, depth, height, color_rod, label)
        self.base_height = base_height  # base Z position of the monitor

    def set_base_height(self, new_base: float):
        """Update the vertical position of the monitor."""
        self.base_height = new_base

    def draw(self, ax: Axes3D) -> None:
        """Plot the rod, shifted by base_height."""
        original_height = self.height
        self.height += self.base_height
        super().draw(ax)
        self.height = original_height
