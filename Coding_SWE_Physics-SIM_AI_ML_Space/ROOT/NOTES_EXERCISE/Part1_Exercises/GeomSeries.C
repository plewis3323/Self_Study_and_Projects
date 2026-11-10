// Exercise 1.3: Geometric series
// Run: root -l -b -q 'GeomSeries.C(0.9, 100)'
#include <iostream>
#include "TMath.h"

void GeomSeries(double x = 0.5, int N = 30) {
    double loopSum = 0;
    for (int i = 0; i < N; i++) loopSum += TMath::Power(x, i);

    double formula = (1 - TMath::Power(x, N)) / (1 - x);

    std::cout << "x = " << x << ", N = " << N << "\n";
    std::cout << "  loop sum = " << loopSum << "\n";
    std::cout << "  formula  = " << formula << "\n";
    std::cout << "  |diff|   = " << TMath::Abs(loopSum - formula) << "\n";
}
