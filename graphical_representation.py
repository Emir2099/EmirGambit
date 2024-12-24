import numpy as np
import matplotlib.pyplot as plt

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

# Traditional Direct Trade-off Optimization
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

# Novel Indirect Trade-off Optimization
def indirect_tradeoff(x_values, degradation_limit=0.1):
    A_values, B_values, C_values = [], [], []
    for x in x_values:
        C = bandwidth(x)
        degraded_C = max(C - degradation_limit, 0.1)  # Controlled degradation
        A = latency(degraded_C)  # Latency improves with degraded C
        B = energy(x)  # Energy remains unaffected
        A_values.append(A)
        B_values.append(B)
        C_values.append(degraded_C)
    return A_values, B_values, C_values

# Simulation
x_values = np.linspace(1, 100, 100)

# Compute values for both approaches
A_direct, B_direct, C_direct = direct_tradeoff(x_values)
A_indirect, B_indirect, C_indirect = indirect_tradeoff(x_values)

# Plotting
fig, axes = plt.subplots(2, 3, figsize=(15, 8), sharex=True)

# Traditional Approach
axes[0, 0].plot(x_values, A_direct, color="blue", label="Latency (A)")
axes[0, 0].set_title("Traditional: Latency (A)")
axes[0, 0].set_ylabel("Latency")
axes[0, 0].grid(True)
axes[0, 0].legend()

axes[0, 1].plot(x_values, B_direct, color="red", label="Energy (B)")
axes[0, 1].set_title("Traditional: Energy (B)")
axes[0, 1].grid(True)
axes[0, 1].legend()

axes[0, 2].plot(x_values, C_direct, color="green", label="Bandwidth (C)")
axes[0, 2].set_title("Traditional: Bandwidth (C)")
axes[0, 2].grid(True)
axes[0, 2].legend()

# Indirect Approach
axes[1, 0].plot(x_values, A_indirect, color="blue", label="Latency (A)")
axes[1, 0].set_title("Indirect: Latency (A)")
axes[1, 0].set_xlabel("Input Resource Level (x)")
axes[1, 0].set_ylabel("Latency")
axes[1, 0].grid(True)
axes[1, 0].legend()

axes[1, 1].plot(x_values, B_indirect, color="red", label="Energy (B)")
axes[1, 1].set_title("Indirect: Energy (B)")
axes[1, 1].set_xlabel("Input Resource Level (x)")
axes[1, 1].grid(True)
axes[1, 1].legend()

axes[1, 2].plot(x_values, C_indirect, color="green", label="Bandwidth (C)")
axes[1, 2].set_title("Indirect: Bandwidth (C)")
axes[1, 2].set_xlabel("Input Resource Level (x)")
axes[1, 2].grid(True)
axes[1, 2].legend()

# Adjust layout
plt.tight_layout()
plt.show()
