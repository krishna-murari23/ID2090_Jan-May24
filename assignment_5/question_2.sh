#!/usr/bin/python3
import sys 
from sympy import *
from math import *
import subprocess
file_name = sys.argv[1]
with open(file_name) as line:
    pressure_gradient = line.readline()
z, r= symbols("z r")
p_symp = sympify(pressure_gradient)
p = p_symp.diff(z)
P = Function('P')(z)
v_z = Function('v_z')(r)
d_e1 = Eq(p  , v_z.diff(r,2) + 1/r*(diff(v_z , r)))
initial_conditions = {diff(v_z,r).subs(r, 0): 0,
                      v_z.subs(r, 1): 0
                      
}
solution = dsolve(d_e1, v_z ,ics = initial_conditions)
#converting the solution to cpp format
cpp_vel = ccode(solution)
cpp_vel = cpp_vel.split("=")[-1]
#CPP Code
cpp = f'''
#include <iostream>
#include <cmath>

double solve(double r) {{
    return {cpp_vel};
}}

int main(int argc, char* argv[]) {{
    double radial = std::stod(argv[1]);
    double velocity =std::abs(solve(radial));
    std::cout << velocity << std::endl;
}}
'''

#writing the cpp code
with open('vel_temp.cpp', 'w') as f:
    f.write(cpp)

#compiling the CPP code through Python
compile_process = subprocess.run(["g++", "-o", "vel.cpp", "vel_temp.cpp"], stdout=subprocess.PIPE) 

