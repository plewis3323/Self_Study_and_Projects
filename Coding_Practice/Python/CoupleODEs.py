import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt

# Define the first second-order ODE
def f1(t, y1, y1_dot, y2, y2_dot):
    return -2 * y1 + y2  # Example: -2y1 + y2

# Define the second second-order ODE
def f2(t, y1, y1_dot, y2, y2_dot):
    return y1 - y2  # Example: y1 - y2

# Convert the second-order ODEs to a system of first-order ODEs
def coupled_ode_system(t, z):
    y1, y1_dot, y2, y2_dot = z
    dy1_dt = y1_dot
    dy2_dt = y2_dot
    dy1_dot_dt = f1(t, y1, y1_dot, y2, y2_dot)
    dy2_dot_dt = f2(t, y1, y1_dot, y2, y2_dot)
    return [dy1_dt, dy1_dot_dt, dy2_dt, dy2_dot_dt]

# Initial conditions: y1(0) = y1_0, y1'(0) = y1_dot_0, y2(0) = y2_0, y2'(0) = y2_dot_0
y1_0 = 1
y1_dot_0 = 0
y2_0 = 0
y2_dot_0 = 1
initial_conditions = [y1_0, y1_dot_0, y2_0, y2_dot_0]

# Time span
t_span = (0, 10)
t_eval = np.linspace(t_span[0], t_span[1], 300)

# Solve the ODE system
solution = solve_ivp(coupled_ode_system, t_span, initial_conditions, t_eval=t_eval)

# Extract solutions
t = solution.t
y1 = solution.y[0]
y2 = solution.y[2]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, y1, label='y1(t)')
plt.plot(t, y2, label='y2(t)')
plt.xlabel('Time t')
plt.ylabel('Solutions y1, y2')
plt.title('Solutions of the Coupled ODEs')
plt.legend()
plt.grid(True)

# Save the plot as a PDF
plt.savefig('coupled_odes_solution.pdf')

# Show the plot
plt.show()

