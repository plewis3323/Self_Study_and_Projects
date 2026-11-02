

/* --------------------------------------------------------------------------------------------------------



                              ROOT Primer (2-3-25):
                              
                              
                              
                              
                              
                              
-------------------------------------------------------------------------------------------------------------*/



// Root Basics:


/* 


* Now that you have installed ROOT, what’s this interactive shell thing you’re running ? It’s like this: ROOT leads a double life. It has an interpreter for macros (Cling) that you can run from the command line or run like applications. But it is also an interactive shell that can evaluate arbitrary statements and expressions. This is extremely useful for debugging, quick hacking and testing. Let us first have a look at some very simple examples

* ex.) root [0] 1+1
(int) 2
root [1] 2*(4+2)/12.
(double) 1.000000
root [2] sqrt(3.)
(double) 1.732051
root [3] 1 > 2
(bool) false
root [4] TMath::Pi()
(double) 3.141593
root [5] TMath::Erf(.2)
(double) 0.222703



* Not bad. You can see that ROOT offers you the possibility not only to type in C++ statements, but also advanced mathematical functions, which live in the TMath namespace.

Now let’s do something more elaborated. A numerical example with the well known geometrical series:


* namespace -> container for variables, functions, classes, etc (all identifiers)



* ex.)   root [0] double x = .5
(double) 0.50000000
root [1] int N = 30
(int) 30
root [2] double geom_series = 0
(double) 0.0000000
root [3] for (int i = 0; i < N; i++)geom_series+=TMath::Power(x,i)
root [4] cout << TMath::Abs(geom_series - (1-TMath::Power(x,N-1))/(1-x)) <<endl;
1.86265e-09
root [5]




* Here we made a step forward. We even declared variables and used a for control structure. Note that there are some subtle differences between Cling and the standard C++ language. You do not need the “;” at the end of line in interactive mode – try the difference e.g. using the command at line root [6] 




- Learn C++ at the ROOT prompt: 


* Behind the ROOT prompt there is an interpreter based on a real compiler toolkit: LLVM. It is therefore possible to exercise many features of C++ and the standard library. For example in the following snippet we define a lambda function, a vector and we sort it in different ways:

* real compiler tolkit-> Tools and trinkets that develop and framework a compiler. 

* standard library-> Yes, that's a great way to think about it! The Standard Template Library (STL) in C++ can indeed be thought of as a set of pre-defined libraries or building blocks that are declared at the beginning of your code (usually with #include statements), enabling you to access essential data structures, algorithms, and utilities without needing to implement them from scratch.

---------------------------------------------------------------------------------------------------*/






















































































































































































































































