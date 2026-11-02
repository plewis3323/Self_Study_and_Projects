#include <TH1.h>
#include <TGraph.h>
#include <TFile.h>
#include <iostream>
#include <cmath>
#include <string>
#include <TGraphErrors.h>
#include <TF1.h>
#include <TMath.h>
#include <TRandom.h>
#include <TFitResultPtr.h>
#include <TMatrixDSym.h>
#include <TCanvas.h>
#include <vector>
#include <TAxis.h>
using namespace std;

void Diff_Cross()
{


double hbar = 1.05e-34; // Unit: J*s
double m = 1.675e-27; // Unit: kg
double E = (10e6)*(1.602e-19); //Unit: J


int num_points = 20;          // Total number of points
double start = 0.0;           // Starting value (0)
double end = M_PI;            // Ending value (π)
double end_b = 2*M_PI;            // Ending value (π)
double step = (end - start) / (num_points - 1); // Step size
double step2 = (end_b - start) / (num_points - 1); // Step size
    // Loop to print the points
vector <double> ang_values(num_points);
    for (int i = 0; i < num_points; ++i) {
        ang_values[i] = start + i * step; // Calculate the current value
    }
vector <double> Diff_cross(num_points); 
for(int k = 0; k < num_points; k++) {
     Diff_cross[k] = (pow(hbar,2)/(2*m*E))*((3.0/16.0)*pow((-1.0 + 3.0*cos(ang_values[k])),2.0) - pow((1.0 + 3.0*cos(ang_values[k])),2.0));
} 


double* x = ang_values.data();
double* y = Diff_cross.data();

// Create a TGraph object
    TGraph *graph = new TGraph(num_points, x, y);

    // Set graph title and axis labels
    graph->SetTitle("Differential Cross Section vs. Theta");

    // Create a canvas to draw the graph
    TCanvas *c1 = new TCanvas("c1", "Diff_C vs. Angle", 800, 600);

    // Draw the graph
    graph->SetMarkerStyle(21); // Use markers for points
    graph->SetMarkerSize(1);
    graph->SetLineColor(kBlue); // Set line color
    graph->SetLineWidth(2);     // Set line width
    graph->Draw("ALP");         // Draw with Axis, Line, and Points

    // Update the canvas to display the graph
    c1->Update();
    
   


}




void Integral_cross () {



double hbar = 1.05e-34; // Unit: J*s
double m = 1.675e-27; // Unit: kg
double E = (10e6)*(1.602e-19); //Unit: J


int num_points = 20;          // Total number of points
double start = 0.0;           // Starting value (0)
double end = M_PI;            // Ending value (π)
double end_b = 2*M_PI;            // Ending value (2π)
double step = (end - start) / (num_points - 1); // Step size
double step2 = (end_b - start) / (num_points - 1); // Step size
    // Loop to print the points
vector <double> ang_values(num_points);
    for (int i = 0; i < num_points; ++i) {
        ang_values[i] = start + i * step; // Calculate the current value
    }
    
    
vector <double> ang_values2(num_points);
    for (int i = 0; i < num_points; ++i) {
        ang_values[i] = start + i * step2; // Calculate the current value
    }    
    
    
    
vector <double> Diff_cross(num_points); 
for(int k = 0; k < num_points; k++) {
     Diff_cross[k] = (pow(hbar,2)/(2*m*E))*((3.0/16.0)*pow((-1.0 + 3.0*cos(ang_values[k])),2.0) - pow((1.0 + 3.0*cos(ang_values[k])),2.0));
} 


double T_Diff_cross = 0.0; 
for (int p = 0; p < num_points; p++)
    {
            T_Diff_cross += abs(end_b*sin(ang_values[p])*(pow(hbar,2.0)/(2*m*E))*((3.0/16.0)*pow((-1.0 + 3.0*cos(ang_values[p])),2.0) - pow((1.0 + 3.0*cos(ang_values[p])),2.0)));
            
            
   }
   
   
cout << "The total value:  " << T_Diff_cross << "  m^2 " << endl; 





}


















