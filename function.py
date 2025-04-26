import numpy as np

r""" Yang and Guo Example Cartesian Form
x = [-2, 4], y = [-3, 3]"""
# def function(x, y):
#     r = np.sqrt(x**2 + y**2)
#     theta = np.arctan2(y, x)
#     return (r-2)**2 + ((theta**2) / 4) - 1

r""" Yang and Guo Example Polar Orthognal Form
x = [-0.5, 4.5], y = [-2.5, 2.5]"""
# def function(x, y):
#     return (x-2)**2 + ((y**2) / 4) - 1

r""" Nephroid Equation for constant a
x = y = [-8.5, 8.5] for a = 2"""
# def function(x, y, a=2):
#     inside = x**2 + y**2 - 4*(a**2)
#     return (inside**3) - 108 * (y**2) * (a**4)

r""" Cardioid Equation for constant a
x=[-9, 3]
y=[-6, 6]"""
# def function(x, y, a=2):
#     r = np.sqrt(x**2 + y**2)
#     theta = np.arctan2(y, x)
    
#     return r - 2*a*(1-np.cos(theta))

r""" Astroid Equation for constant a"""
# def function(x, y, a=5):
#     inside = x**2 + y**2 - a**2
#     return (inside)**3 + 27*(a**2)*(x**2)*(y**2)

r"""Circle Equation for radius a"""
# def function(x, y, a=4):
#     return x**2 + y**2 - a**2
    
r"""Polar Nephroid Equation for constant a"""
# def function(x, y, a=1):
#     r = np.sqrt(x**2 + y**2)
#     theta = np.arctan2(y, x)
    
#     first = (r/(2*a))**(2/3)
#     second = np.abs(np.sin(theta/2)) ** (2/3)

#     third = np.abs(np.cos(theta/2)) ** (2/3)
    
#     return first - second - third

r"""Polar Nephroid Equation in terms of x and y"""
# def function(x, y, a=1):
#     first = np.abs(x/(2*a))**(2/3)
#     second = np.abs(np.sin(y/2)) ** (2/3)

#     third = np.abs(np.cos(y/2)) ** (2/3)
    
#     return first - second - third
