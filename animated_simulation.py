import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Slider

# Objective functions
def latency(C):
    """Latency (A): inversely proportional to C."""
    return 1 / C + 5

def energy(x):
    """Energy consumption (B): depends on other resources."""
    return 0.5 * x + 20

def bandwidth(x):
    """Bandwidth (C): inversely proportional to x."""
    return 1 / (0.2 * x + 1)

# Trade-off computations
def direct_tradeoff(x_values):
    A_values, B_values, C_values = [], [], []
    for x in x_values:
        C = bandwidth(x)
        A = latency(C)
        B = energy(x)
        A_values.append(A)
        B_values.append(B)
        C_values.append(C)
    return A_values, B_values, C_values

def indirect_tradeoff(x_values, degradation_limit):
    A_values, B_values, C_values = [], [], []
    for x in x_values:
        C = bandwidth(x)
        degraded_C = max(C - degradation_limit, 0.1)  # Controlled degradation
        A = latency(degraded_C)
        B = energy(x)
        A_values.append(A)
        B_values.append(B)
        C_values.append(degraded_C)
    return A_values, B_values, C_values

# Initialize resource range
x_values = np.linspace(1, 100, 100)

# Default degradation limit
default_degradation_limit = 0.1

# Compute values for both approaches
A_direct, B_direct, C_direct = direct_tradeoff(x_values)
A_indirect, B_indirect, C_indirect = indirect_tradeoff(x_values, default_degradation_limit)

# Create figure and axes
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
plt.subplots_adjust(bottom=0.25)  # Adjust space for sliders

# Titles for subplots
titles = [
    "Traditional: Latency (A)", "Traditional: Energy (B)", "Traditional: Bandwidth (C)",
    "Indirect: Latency (A)", "Indirect: Energy (B)", "Indirect: Bandwidth (C)"
]

# Initialize plots
plots = []
for i, ax in enumerate(axes.flat):
    ax.set_title(titles[i])
    ax.set_xlabel("Resource Level (x)")
    ax.set_ylabel(["Latency", "Energy", "Bandwidth"][(i % 3)])
    ax.grid(True)
    if i < 3:
        # Traditional approach plots
        plot, = ax.plot(x_values, [A_direct, B_direct, C_direct][i], label="Traditional")
    else:
        # Indirect approach plots
        plot, = ax.plot(x_values, [A_indirect, B_indirect, C_indirect][i - 3], label="Indirect")
    plots.append(plot)
    ax.legend()

# Slider for degradation limit
ax_degradation = plt.axes([0.15, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_degradation = Slider(ax_degradation, "Degradation Limit", 0.01, 0.5, valinit=default_degradation_limit)

# Slider for resource range
ax_resource = plt.axes([0.15, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_resource = Slider(ax_resource, "Resource Max", 10, 200, valinit=100)

# Update function
def update(val):
    # Get slider values
    degradation_limit = slider_degradation.val
    resource_max = slider_resource.val

    # Recompute data
    x_values = np.linspace(1, resource_max, 100)
    A_direct, B_direct, C_direct = direct_tradeoff(x_values)
    A_indirect, B_indirect, C_indirect = indirect_tradeoff(x_values, degradation_limit)

    # Update plots
    plots[0].set_data(x_values, A_direct)
    plots[1].set_data(x_values, B_direct)
    plots[2].set_data(x_values, C_direct)
    plots[3].set_data(x_values, A_indirect)
    plots[4].set_data(x_values, B_indirect)
    plots[5].set_data(x_values, C_indirect)

    # Adjust axes limits dynamically
    for ax in axes.flat:
        ax.relim()
        ax.autoscale_view()

    fig.canvas.draw_idle()

# Connect sliders to update function
slider_degradation.on_changed(update)
slider_resource.on_changed(update)

# Show plot
plt.show()
