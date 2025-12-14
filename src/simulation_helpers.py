from __future__ import annotations
# simulation_helpers.py
from matplotlib.widgets import Slider

from src.area_reactor import ReactorArea
from src.particle_manager import ParticleManager
from src.particle_visualization import draw_particles

def create_sliders(fig, elements_list: list, slider_position: tuple, 
                   slider_dimension: tuple, max_value: float, title: str, slider_color:str):
    """
    Create vertical sliders for a list of elements.
    """
    x_pos, y_pos = slider_position
    slider_width, slider_height = slider_dimension   
    
    fig.text(x_pos + 0.06, y_pos + slider_height + 0.06, title, ha="center")
    
    store_slider = []
    for element in elements_list:
        ax_slider = fig.add_axes([x_pos, y_pos, slider_width, slider_height])
        slider = Slider(ax_slider, element.label, valmin = 0.0, valmax = max_value, 
                        valinit = 0.0, orientation = "vertical", color = slider_color
                        )
        store_slider.append(slider)
        x_pos += slider_width + 0.015
        
    return store_slider

def update_simulation(ax, fig, reactor: ReactorArea, particle_manager: ParticleManager, 
                      sliders_elements: list, elements_list: list, 
                      monitor_sliders: list, monitors: list,
                      animation_state:bool,
                      energy_distribution: list, dt: float = 0.05) -> None:
    """
    Update full simulation step:
        Apply slider values
        Move particles
        Redraw reactor and particles
    """
    ax.cla()
    ax.set_xlim(0, reactor.width)
    ax.set_ylim(0, reactor.depth)
    ax.set_zlim(0, reactor.height)

    # Update monitor positions (keep height fixed)
    for slider, monitor in zip(monitor_sliders, monitors):
        monitor.base_height = slider.val
        
    # Update rods from sliders
    for slider, element in zip(sliders_elements, elements_list):
        # Return whether (T/F) the "element" object has an attribute with 
        # name "set_height"
        if hasattr(element, "set_height"):
            element.set_height(slider.val)
        elif hasattr(element, "base_height"):
            element.base_height = slider.val

    # Move particles
    if animation_state["running"]:
        for particle in particle_manager.particles:
            if particle.alive:
                particle.move(dt)
                # Wall collisions
                limits = [reactor.width, reactor.depth, reactor.height]
                for i in range(3):
                    if particle.position[i] < 0:
                        particle.position[i] = 0
                        particle.velocity[i] *= -1
                    elif particle.position[i] > limits[i]:
                        particle.position[i] = limits[i]
                        particle.velocity[i] *= -1

    # Redraw
    reactor.draw(ax)
    # Particle drawing stays separate
    draw_particles(ax, particle_manager, energy_distribution)
    fig.canvas.draw_idle()
    
def connect_keyboard(fig, animation_state: dict):
    """
    Keyboard handler:
    Space bar toggles animation on/off.
    """
    def on_key(event):
        if event.key == " ":
            animation_state["running"] = not animation_state["running"]
    
    fig.canvas.mpl_connect("key_press_event", on_key)