
#include <iostream>
#include <cmath>

double solve(double r) {
    return  (1.0/2.0)*pow(r, 2) - 1.0/2.0;
}

int main(int argc, char* argv[]) {
    double radial = std::stod(argv[1]);
    double velocity =std::abs(solve(radial));
    std::cout << velocity << std::endl;
}
