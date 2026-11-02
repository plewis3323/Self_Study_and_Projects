#include <iostream>
#include <TCanvas.h>
#include <vector>
#include <string>
#include <TString.h>
#include <TGraph.h>
#include <TGraphErrors.h>
#include <TRandom.h>
#include <TF1.h>
#include <TH1.h>
#include <TFile.h>
#include <TH1F.h>
#include <cmath>




void chi_2_ex() 

{


//Intialize the data points neccssary 


vector<double> t_j =  {1.0, 2.0,  3.0};
vector<double> u_j =  {0.8, 1.5, 2.7};
vector<double> sigma_j = {0.1, 0.05, 0.2};
double a;



//Finding slope parameter a
double sum_num = 0.0; 
double sum_den = 0.0; 
for (int v = 0; v <t_j.size(); v++)
{

sum_num += (t_j[v] * u_j[v] )/(pow(sigma_j[v], 2));
sum_den += (pow(t_j[v], 2)) / (pow(sigma_j[v],2));

}

a = sum_num/sum_den;
cout << "The slope parameter a = " << a << endl; 



//How to calculate variance of a 
double variance_a_dem = 0.0; 
for (int p = 0; p < 3; p++)
{

 variance_a_dem += (pow(t_j[p],2))/(pow(sigma_j[p],2));

}

double var_a = 1/(variance_a_dem) ; 
cout << "the variance of a = " << var_a << endl;



 
// Make the data into a histogram 
double xlow = 0.0; //low range
double xhigh = 5.0; //high range
TH1F *hist = new TH1F("hist", "histogram t vs. u", 100 , xlow, xhigh);



//Fill the histogram 
for (int i = 0; i<100; i++) 
{

int bin = hist->FindBin(t_j[i]);  //bin fot t_j[i]
hist->SetBinContent(bin, u_j[i]); //bin content to u_j[i]


}


//Draw the histogram and fitting function
TCanvas *c1 = new TCanvas("c1");
// Step 1: Create a TF1 object for the linear function a * t
TF1 *linearFunc = new TF1("linearFunc", "[0]*x", 0, 3); // Define from 0 to 4 for t range
linearFunc->SetParameter(0, a); // Set the parameter [0] = a
hist->Fit(linearFunc, "R");
hist->Draw();
linearFunc->Draw("SAME");



//Chi-square comparisons 
    

//Perform Chi-square test with user defined functions. 
     double chi_square = 0.0; 
     for(int k = 0; k < 3; k++)
     {
     
         chi_square += pow(((u_j[k] - a*t_j[k])/(sigma_j[k])), 2);
         
     }
     
     cout << "Manual Chi-square value: " << chi_square << endl; 


}



 



