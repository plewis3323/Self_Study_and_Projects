% Quantum Box Potential
% Parameters
L = 1; % Length of the box
n_max = 3; % Number of wave functions to plot
x = linspace(0, L, 1000); % Discretize the x-axis

% Planck's constant (h-bar)
hbar = 1.0545718e-34; % Planck's constant in J.s

% Mass of the particle (e.g., electron)
m = 9.10938356e-31; % Mass of electron in kg

% Plot the wave functions and energy levels
figure;
hold on;
for n = 1:n_max
    psi_n = sqrt(2/L) * sin(n * pi * x / L);
    E_n = (n^2 * pi^2 * hbar^2) / (2 * m * L^2);
    plot(x, psi_n, 'DisplayName', sprintf('n = %d', n));
    yline(E_n, '--', 'DisplayName', sprintf('E_n = %.2e J', E_n));
end
hold off;

title('Wave Functions and Energy Levels in a Quantum Box');
xlabel('Position x');
ylabel('Wave function \psi_n(x)');
legend show;
grid on;

% Save the figure
print('quantum_box_potential.png', '-dpng');

