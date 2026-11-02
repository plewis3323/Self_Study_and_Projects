

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Define the differential equation dy/dt = -2y
def dydt(t, y):
    return -2 * y

# Define the time range and initial condition
t_span = (0, 5)  # time range from 0 to 5
y0 = [1]  # initial condition y(0) = 1

# Solve the differential equation
solution = solve_ivp(dydt, t_span, y0, t_eval=np.linspace(0, 5, 100))

# Plot the solution
plt.plot(solution.t, solution.y[0])
plt.xlabel('t')
plt.ylabel('y(t)')
plt.title('Solution of the differential equation dy/dt = -2y')
plt.grid()
plt.show()


# Save the plot with a specified filename
filename = 'Ex_Diff_eq_plot.pdf'
plt.savefig(filename)



