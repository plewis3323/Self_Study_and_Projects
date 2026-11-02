function plot_data(x, y)
    plot(x, y);
    xlabel('X-axis');
    ylabel('Y-axis');
    title('Sample Plot');
end

% Usage
x = 1:10;
y = x .^ 2;
plot_data(x, y);

