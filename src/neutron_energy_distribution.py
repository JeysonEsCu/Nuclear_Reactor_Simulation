from __future__ import annotations
# neutron_energy_distribution.py

import numpy as np

distribution_dict = {
    "debug_uniform": lambda num_neutrons: np.random.uniform(0.1, 10.0, size= num_neutrons),
    "debug_normal": lambda num_neutrons: np.random.normal(loc=1.0, scale=0.5, size= num_neutrons)
}

def neutron_energy_distribution(distribution_name: str, num_neutrons: int) -> np.ndarray:
    """
    Return array of neutron energies in MeV.
    
    Parameters:
        distribution_list: dict of functions returning energies
        distribution_name: str, key in distribution_list
        num_neutrons: int, number of neutrons
    Returns:
        np.ndarray of energies
    """
    if distribution_name not in distribution_dict:
        raise ValueError(f"Distribution '{distribution_name}' not supported")
    
    energies = distribution_dict[distribution_name](num_neutrons)
    # energies >= 0.0
    energies = np.clip(energies, 0.0, None)
    return energies