# Solve the quadratic equation ax**2 + bx + c = 0

# import complex math module
import cmath

def quad(a,b,c):
    d = (b**2) - (4*a*c)
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)
    return sol1, sol2