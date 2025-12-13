from __future__ import annotations
import numpy as np

"""
Defines a single particle (e.g., neutron) for reactor simulation.

Each particle stores its position, velocity, energy, and state.
Provides methods to move and update the particle in time.
"""

class Particle:
    """
    Represents a single particle in 3D space.
    """
    def __init__(self, position: np.ndarray, velocity: np.ndarray, energy: float):
        """
        Args:
            energy: Kinetic energy of the particle.
        """
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.energy   = energy
        self.alive    = True  # Flag to know if particle is active
        self.history  = [self.position.copy()]  # Store path for visualization

    def move(self, dt: float) -> None:
        """
        Update the position of the particle based on its velocity.
        Args:
            dt: Time step
        """
        if not self.alive:
            return
        # Simple linear motion
        self.position += self.velocity * dt
        self.history.append(self.position.copy())

    def absorb(self) -> None:
        """
        Mark particle as absorbed (e.g., by control rod).
        """
        self.alive = False

    def scatter(self, new_velocity: np.ndarray, energy_loss: float = 0.0) -> None:
        """
        Update particle velocity due to scattering and optionally reduce energy.
        Args:
            new_velocity: New 3D velocity vector
            energy_loss: Amount of energy lost in scattering
        """
        self.velocity = np.array(new_velocity)
        self.energy = max(self.energy - energy_loss, 0.0)

    def is_alive(self) -> bool:
        """
        Returns:
            True if particle is still active
        """
        return self.alive

    def __repr__(self) -> str:
        return f"Particle(pos={self.position}, vel={self.velocity}, energy={self.energy:.2f}, alive={self.alive})"
