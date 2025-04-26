#!/usr/bin/env python3

import os
import numpy as np
import scipy.sparse.linalg
import matplotlib.pyplot as plt
from Debugging import Debugging
from Parser import Parser
from solver import *
from plotting import *
import function

parser = Parser("./input.txt")

os.makedirs("./plots", exist_ok=True)
os.makedirs("./results", exist_ok=True)

shape = parser.get_config_value("shape")
image_file = parser.get_config_value("potential_image_name")
function_parsed = parser.get_config_value("function")

if sum(x is not None for x in [shape, image_file, function_parsed]) != 1:
    sys.exit("Please provide only one of: shape, potential_image_name, or function")

potential_type = shape or image_file or function_parsed
is_shape = shape is not None or function_parsed is not None
function_bool = function_parsed is not None

os.makedirs(f"./plots/{potential_type}_plots", exist_ok=True)

max_level = parser.get_config_value("max_level")
if max_level is None:
    sys.exit("Please provide max_levels")

for i in range(max_level):
    os.makedirs(f"./plots/{potential_type}_plots/{i}", exist_ok=True)

boundary_value = parser.get_config_value("boundary_value") or 1e6

grid_info_names = ["x_start", "x_end", "y_start", "y_end", "grid_size"]
grid_info = [parser.get_config_value(elm) for elm in grid_info_names]
grid_info.append((grid_info[1] - grid_info[0]) / (grid_info[4] - 1))

print(f"input.txt parsed: Using {potential_type}")
debugger = Debugging(debug=parser.args.debug)

if function_bool:
    x_vals = np.linspace(grid_info[0], grid_info[1], grid_info[4])
    y_vals = np.linspace(grid_info[2], grid_info[3], grid_info[4])
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = function.function(X, Y)
    
    plt.figure(figsize=(6, 6))
    plt.contour(X, Y, Z, levels=[0], colors='blue')
    # plt.title("Function in Cartesian Coordinates")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.savefig(f"./plots/{potential_type}_plots/function_plot.png")
    
    print("Function plotted")
    
    potential_matrix = np.where(Z <= 0, 0, boundary_value).reshape(grid_info[4], grid_info[4])
else:
    potential_matrix = (
        get_potential_from_image(image_file, debugger, boundary_value)[0]
        if not is_shape else get_potential_from_shape(shape, grid_info, debugger, boundary_value)
    )

plot_potential(potential_matrix, potential_type, grid_info, is_shape)
print("Potential matrix plotted")
Hamiltonian = construct_hamiltonian(potential_matrix, grid_info[4], debugger, boundary_value)
print(f"Hamiltonian constructed of size {Hamiltonian.get_shape()}, solving now")
eigenvalues, eigenvectors = scipy.sparse.linalg.eigsh(Hamiltonian, k=max_level, which="SM")
eigenvectors *= grid_info[-1] ** 2

print("Solved!")
plot_eigenfunctions_from_shape(eigenvectors, grid_info[4], max_level, potential_type) if is_shape else plot_eigenfunctions_from_image(eigenvectors, potential_matrix.shape, max_level, potential_type)
plot_nodal_lines(eigenvectors, grid_info[4] if is_shape else potential_matrix.shape[0], max_level, potential_type)

print("Done")
np.save(f"./results/{potential_type}_eigenvectors_upto_state_{max_level}.npy", eigenvectors)
np.save(f"./results/{potential_type}_eigenvalues_upto_state_{max_level}.npy", eigenvalues)
