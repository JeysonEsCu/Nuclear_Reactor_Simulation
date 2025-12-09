# 3D Modular Nuclear Reactor Simulator

It includes adjustable control rods, randomly moving particles, and a modular design
based on classes to keep the code clean.

## Features

- 3D reactor with transparent geometry
- Adjustable control rods with sliders (in progress)
- Randomly moving particle system (will take as a reference from previous project)
- `src/` contains all modules and code
- Easier to run and extend

## Project Structure

Nuclear_Reactor_simulation/
|
|-- main.py <- Entry point, runs the simulation
|
|--src/ <- All modules/classes
| |
| |-- area_reactor.py <- Reactor framework / container
| |-- control_rods.py <- Neutron absorbers/Nuclear fuel/..
| |
| |-- **init**.py
|-- README.md

## Running simulation

python main.py
