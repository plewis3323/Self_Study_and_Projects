// Exercise 1.1: Calculator warm-up
// Run:     root -l -b -q Calculator.C
// Compile: root -l -b -q Calculator.C+
#include <iostream>
#include "TMath.h"

void Calculator() {
    // Integer vs floating-point division
    std::cout << "7/2   = " << 7/2  << "   (int / int -> int, truncated)\n";
    std::cout << "7/2.  = " << 7/2. << " (int / double -> double)\n";

    // e^-1
    std::cout << "exp(-1) = " << TMath::Exp(-1.) << "\n";

    // Gaussian at x=1, mean 0, sigma 1
    // TMath::Gaus(x, mean, sigma, norm=false)
    std::cout << "Gaus(1,0,1)        = " << TMath::Gaus(1., 0., 1.)
              << "  (peak height 1: exp(-x^2/2))\n";
    std::cout << "Gaus(1,0,1,kTRUE)  = " << TMath::Gaus(1., 0., 1., kTRUE)
              << "  (normalized: divided by sqrt(2*pi)*sigma)\n";
};
