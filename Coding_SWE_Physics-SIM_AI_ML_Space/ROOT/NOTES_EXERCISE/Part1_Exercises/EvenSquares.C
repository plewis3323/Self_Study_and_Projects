// Exercise 1.4: Lambdas and vectors
// Run: root -l -b -q EvenSquares.C
#include <iostream>
#include <vector>

void EvenSquares() {
    std::vector<double> squares;
    for (int i = 1; i <= 10; i++) squares.push_back(i * i);

    // Lambda: true if the value is even
    auto isEven = [](double v) { return static_cast<long>(v) % 2 == 0; };

    std::cout << "Even squares of 1-10:";
    for (double s : squares)
        if (isEven(s)) std::cout << " " << s;
    std::cout << "\n";
}
