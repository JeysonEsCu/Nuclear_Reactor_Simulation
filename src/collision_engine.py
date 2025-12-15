from __future__ import annotations
import numpy as np

def handle_collision(particle, obj, elastic: bool = True) -> bool:
    """
    Check and handle collision between a particle and a rectangular object.
        particle: Particle object with .position and .velocity
        obj: Object where the particle collides, with .x_position, .y_position, .base_height, .height, .width, .depth
        elastic: If True, collision is elastic; if False, could reduce energy (future)
        getattr(obj, "name_attr", Value) is used to access to an attribute of an object
        if it does not have the attribute, its value will be the given "value"
        
        Extended to adapt any kind off collision in any surface by using
            behavior = getattr(obj, "collision_behavior", "reflect")
    """
    # Object bounds
    x_min = obj.x_position - obj.width / 2
    x_max = obj.x_position + obj.width / 2
    y_min = obj.y_position - obj.depth / 2
    y_max = obj.y_position + obj.depth / 2
    z_min = getattr(obj, "base_height", 0)
    z_max = getattr(obj, "base_height", 0) + getattr(obj, "height", 0)

    position0 = particle.prev_position
    position1 = particle.position
    velocity  = particle.velocity

    # Check inside states
    def inside(particle_position: list) -> bool:
        return (
            x_min <= particle_position[0] <= x_max and
            y_min <= particle_position[1] <= y_max and
            z_min <= particle_position[2] <= z_max
        )

    if not inside(position0) and inside(position1):
        # Collision detected (crossed surface)

        # Determine which face was crossed
        normal_vector = []

        # cross from left to right
        if position0[0] < x_min and position1[0] >= x_min:
            normal_vector.append(np.array([-1, 0, 0]))
        # cross from right to left
        elif position0[0] > x_max and position1[0] <= x_max:
            normal_vector.append(np.array([1, 0, 0]))

        # cross from the front
        if position0[1] < y_min and position1[1] >= y_min:
            normal_vector.append(np.array([0, -1, 0]))
        # cross from the back
        elif position0[1] > y_max and position1[1] <= y_max:
            normal_vector.append(np.array([0, 1, 0]))
            
        # cross from the bottom
        if position0[2] < z_min and position1[2] >= z_min:
            normal_vector.append(np.array([0, 0, -1]))
        # cross from the top
        elif position0[2] > z_max and position1[2] <= z_max:
            normal_vector.append(np.array([0, 0, 1]))

        if not normal_vector:
            # No collision
            return False

        # Use the first detected surface
        n = normal_vector[0]

        # behavior of the particle after collision with the surface of the object
        # if it does not have one, by default: reflect
        behavior = getattr(obj, "collision_behavior", "reflect")
        
        if behavior == "absorb":
            particle.absorb()   # defined method
            # Collision
            return True
        
        elif behavior == "reflect":
            particle.position = position0.copy()
            # Reflect velocity
            if elastic:
                particle.velocity = velocity - 2 * np.dot(velocity, n) * n
            else:
                # simple model, more complex in the future
                particle.velocity = 0.5 * (velocity - 2 * np.dot(velocity, n) * n)
                particle.energy = 0.25 * particle.energy # velocity is reduced by half
            # Collision
            return True
        
        elif behavior == "transmit":
            # allow particle to enter object (future use)
            # Collision
            return True
    
    # No collision
    return False
