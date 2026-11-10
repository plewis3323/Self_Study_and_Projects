// Exercise 1.5: Interpreted vs compiled
// Interpreted: root -l -b -q SlowLoop.C
// Compiled:    root -l -b -q SlowLoop.C+
#include <iostream>
#include "TMath.h"
#include "TStopwatch.h"

void SlowLoop() {
    TStopwatch timer;
    timer.Start();

    double sum = 0;
    for (long i = 0; i <= 100000000L; i++) sum += TMath::Sqrt(i);

    timer.Stop();
    std::cout << "sum = " << sum << "\n";
    std::cout << "real time = " << timer.RealTime() << " s, "
              << "cpu time = " << timer.CpuTime() << " s\n";
}
