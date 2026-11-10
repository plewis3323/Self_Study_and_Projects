// Exercise 1.6: Three TMath functions found with Tab-completion
// Run: root -l -b -q Explore.C
#include <iostream>
#include "TMath.h"

void Explore() {
    // Binomial(n, k): number of ways to choose k from n ("n choose k")
    std::cout << "TMath::Binomial(5, 2)    = " << TMath::Binomial(5, 2) << "\n";

    // Prob(chi2, ndf): probability that a chi^2 this large or larger happens by chance
    std::cout << "TMath::Prob(10.0, 10)    = " << TMath::Prob(10.0, 10) << "\n";

    // BreitWigner(x, mean, gamma): resonance line shape (e.g. a particle mass peak)
    std::cout << "TMath::BreitWigner(0,0,1)= " << TMath::BreitWigner(0., 0., 1.) << "\n";
}
