# 3D Modular Nuclear Reactor Simulator

It includes adjustable control rods, randomly moving particles, and a modular design
based on classes to keep the code clean.

## Features

- 3D reactor with transparent geometry
- Adjustable control rods with sliders (in progress)
- Randomly moving particle system (reference from previous project)
- `src/` contains all modules and code
- Easier to run and extend

## Project Structure

Nuclear_Reactor_simulation/
|-- main.py # Entry point, runs the simulation
|-- README.md # Project documentation
|-- requirements.txt # dependencies
|-- src/ # All modules/classes
|-- **init**.py # Makes 'src' a Python package
|-- area_reactor.py # Reactor framework / container
|-- control_rods.py # Neutron absorber rods
|-- neutron_monitor_flux.py # Flux monitor bars

## Clone the repository

```bash
git clone https://github.com/JeysonEsCu/Nuclear_Reactor_Simulation.git
cd Nuclear_Reactor_simulation
```

## Install dependencies

pip install -r requirements.txt

## Running the simulation

python main.py

## Next steps

- `particle.py`: represents only one neutron, storing position, velocity, energy, state (alive, absorbed, ...).
- `particle_emitter.py`: if fuel emits or not a neutron, neutrons/second, initial energy, direction, intermediate between `particle` and `particle_manager`.
- `particle_manager.py`: controls all the particles, simulation steps, verify if there is a collision, upload the state of the neutron.
- `irradiation_box.py`: samples inside and they will interact with the neutrons.
- `collision_engine.py`: apply some basic physics law when neutrons interact with fuel rods, control rods, monitors, reactor walls, some important regions in the reactor.
