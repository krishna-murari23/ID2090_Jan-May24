#!/bin/bash

# Function to perform convolution using Fourier Transform
convolve_fourier_transform() {
    f1="$1"
    f2="$2"
    
    python3 - <<END
import sympy as sp


x, xi = sp.symbols('x xi')

# Parse functions from strings
f1 = sp.sympify("$f1")
f2 = sp.sympify("$f2")

# Apply Fourier Transform on the two functions
F1 = sp.fourier_transform(f1, x, xi)
F2 = sp.fourier_transform(f2, x, xi)

# Convolution in Fourier domain
convolved_F = F1 * F2

# Inverse Fourier Transform to get the final convolved function
convolution = sp.inverse_fourier_transform(convolved_F, xi, x)

# Print the simplified final convolved function
print(sp.latex(convolution.simplify())) #Using sp.latex simplifies the given output to it's latex expression, using sp.pprint makes it appear in a nice mathematical fashion

END
}

# Defining a Main
main() {
    # Read the functions from plaintext file
    functions_file="functions.txt" 
    if [[ ! -f "$functions_file" ]]; then
        echo "Error: $functions_file not found"
        exit 1
    fi

    # Read the functions from the file
    functions=()
    while IFS= read -r line; do
        functions+=("$line")
    done < "$functions_file"
    
    # Ensure there are exactly two lines (two functions)
    if [[ ${#functions[@]} -ne 2 ]]; then
        echo "Error: $functions_file must contain exactly two lines (two functions)"
        exit 1
    fi

    # Perform convolution using Fourier Transform
    convolve_fourier_transform "${functions[0]}" "${functions[1]}"
}

# Run the main function
main

