#include <TH1.h>
#include <TGraph.h>
#include <TFile.h>
#include <iostream>
#include <cmath>
#include <string>
#include <TGraphErrors.h>
#include <TF1.h>
#include <TRandom.h>
#include <TFitResultPtr.h>
#include <TMatrixDSym.h>
#include <TCanvas.h>
#include <vector>
#include <TAxis.h>
using namespace std;

void Diff_Cross()
{

double Const_cross = 30; //(mb/sr)
int num_points = 20;          // Total number of points
double start = 0.0;           // Starting value (0)
double end = M_PI;            // Ending value (π)
double step = (end - start) / (num_points - 1); // Step size
    // Loop to print the points
vector <double> ang_values(num_points);
    for (int i = 0; i < num_points; ++i) {
        ang_values[i] = start + i * step; // Calculate the current value
    }
vector <double> Diff_cross(num_points); 
for(int k = 0; k < num_points; k++) {
     Diff_cross[k] = Const_cross*(1 + 3*cos(ang_values[k])*cos(ang_values[k]) + 3*cos(ang_values[k]));
} 


double* x = ang_values.data();
double* y = Diff_cross.data();

// Create a TGraph object
    TGraph *graph = new TGraph(num_points, x, y);

    // Set graph title and axis labels
    graph->SetTitle("Cross Section vs. Angular distribution");

    // Create a canvas to draw the graph
    TCanvas *c1 = new TCanvas("c1", "Cross example", 800, 600);

    // Draw the graph
    graph->SetMarkerStyle(21); // Use markers for points
    graph->SetMarkerSize(1);
    graph->SetLineColor(kBlue); // Set line color
    graph->SetLineWidth(2);     // Set line width
    graph->Draw("ALP");         // Draw with Axis, Line, and Points

    // Update the canvas to display the graph
    c1->Update();


}





















































































































































