# CSP algorithm to solve Cryptarithemtic Problem
The programs solves the cryptarithmetic problem below:

    x1  x2  x3  x4  
+   x5  x6  x7  x8  
___________________  
x9 x10 x11 x12 x13

# implementation
The program implements the function SELECT-UNASSIGNED-VARIABLE in the algorithm by using the minimum remaining values heuristic, followed by the degree heuristic. For the INFERENCE function, I use Forward Checking to detect early failures and reduce the domain values of variables.

# input
The input file contains three rows (or lines) of capital letters:
LLLL  
LLLL  
LLLLL  
The first and second rows contain four capital letters and the third row contains five capital letters with no blank space between letters. The output file should follow the following format
DDDD  
DDDD  
DDDDD  
where the Ds represent digits from 0 to 9 with no bank space between the digits.

# testing  the program
Go to the csp_final.py directory in the terminal
In terminal, run `python csp_final.py`
To change the input file name, go to main function in the python file and change the in_file variable to the whatever file name you want to consider input as
