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
|-- main.py                  # Entry point, runs the simulation
|-- README.md                # Project documentation
|-- requirements.txt         # dependencies
|-- src/                     # All modules/classes
    |-- __init__.py          # Makes 'src' a Python package
    |-- area_reactor.py      # Reactor framework / container
    |-- control_rods.py      # Neutron absorber rods
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
