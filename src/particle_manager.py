from __future__ import annotations
# particle_manager.py
from src.particle import Particle
import numpy as np

class ParticleManager:
    """
    Manages a collection of particles in the reactor.
    Handles spawning, updating, collisions, and removal.
    """

    def __init__(self):
        self.particles: list[Particle] = []  # store all Particle instances

    def spawn(self, position: np.ndarray, velocity: np.ndarray, energy: float) -> None:
        """Add a new particle to the system."""
        particle = Particle(position, velocity, energy)
        self.particles.append(particle)

    def update_all(self, dt: float) -> None:
        """Update all particles' positions."""
        for particle in self.particles:
            if particle.alive:
                particle.move(dt)

    def remove_dead(self) -> None:
        """Remove all dead particles to keep the list clean."""
        self.particles = [particle for particle in self.particles if particle.alive]

    # "dunder" methods: special methods
    
    # __len__: avoids TypeError: object of type 'ParticleManager' has no len()  def __len__(self) -> int:
    def __len__(self) -> int:
        """
            ParticleManager does not know what is the meaning of 'size'
            __len__ says what i the meaning of 'size' of the array self.particles
        """
        return len(self.particles)

    def __repr__(self) -> str:
        """
            Used to shows an object
        """
        return f"ParticleManager({len(self.particles)} particles)"
