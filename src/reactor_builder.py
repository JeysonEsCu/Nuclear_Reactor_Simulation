from __future__ import annotations
# reactor_builder.py
import numpy as np

from src.area_reactor import ReactorArea
from src.particle_manager import ParticleManager
from src.control_rods import ControlRod
from src.neutron_monitor_flux import NeutronMonitor

def element_on_grid(coordinates_list: list, width: float, depth: float, 
                    height:float, color: str, type_element: str) -> list:
    """
    Works for absorber and fuel rods
    """
    # if statement for debug and experimentation in the code
    if not coordinates_list:    # when coordinates_list is None or []
        return []
    
    elements = []
    for i, (x, y) in enumerate(coordinates_list):
        elements.append(ControlRod(x, y, width, depth, height, color, 
                                   f"{type_element}\n{i+1}"))
    return elements

def flux_monitor_on_grid(coordinates_list: list, width: float, depth: float, 
                    height:float, color: str) -> list:
    """Only for flux monitor"""
    elements = []
    for i, (x, y) in enumerate(coordinates_list):
        elements.append(NeutronMonitor(x, y, width, depth, height, color, 
                                       f"flux\n{i+1}"))
    return elements
        
def populate_reactor(reactor: ReactorArea, reactor_elements: list) -> None:
    """Add all the elements into the reactor"""
    for each_element in reactor_elements:
        reactor.add(each_element)
        
def populate_particles(particle_manager: ParticleManager, fuel_rods: list, 
                       reactor_height: float, energies: np.ndarray | None = None, 
                       particles_per_fuel: int = 5, particle_mass: float=1.0) -> None:
    """
    Create particle in each fuel rod and adds to ParticleManager
    fuel_rods: list of objects of ControlRod class.
    energies: array with energies in MeV, if None, energy by default
    particle_per_fuel: number of particles er fuel rod
    """
    print('NOTE:\
          energy assumed in arbitrary units\
              (MeV not yet converted to Joules)\
                  src/reactor_builder.py')
    energy_by_default = 1.0 # MeV
    all_fuel_index = []
    for i, fuel in enumerate(fuel_rods):
        all_fuel_index.extend([i] * particles_per_fuel)
        
    # Use the energy
    if energies is None:
        energies = np.full(len(all_fuel_index), energy_by_default)
        
    # Generate particles
    for idx, fuel_idx in enumerate(all_fuel_index):
        fuel = fuel_rods[fuel_idx]
        energy = energies[idx]
        
        # random position in z-axis
        position = np.array([
            fuel.x_position, fuel.y_position, 
            np.random.uniform(0, reactor_height)
            ])
    
        # velocity(Energy) E = 1/2 * m * v**2
        speed = np.sqrt(2 * energy / particle_mass) # module
        direction = np.random.uniform(-1, 1, 3)     # (x, y, z)
        norm = np.linalg.norm(direction)
        if norm == 0:
            direction = np.array([1.0, 0.0, 0.0])
        else:
            direction /= norm      # unit vector
        velocity = direction * speed
        
        # Create particle in ParticleManager
        particle_manager.spawn(position, velocity, energy)
