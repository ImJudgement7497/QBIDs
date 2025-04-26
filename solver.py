# PLAN
# Construct Sparse Matrix either using function above or similar way
# Solve eigenvalues/vectors and check against inspo
# Plot
# Optimise
# Parallise

# Optional Features: adding the boundary back on

import argparse
import sys
import numpy as np
from PIL import Image
import scipy as sp
from Debugging import Debugging
import cv2


# Function to get potential from image
def get_potential_from_image(file_name: str, debugger: Debugging, boundary_value) -> tuple:

    # Open image in black and white
    image = (Image.open(file_name)).convert('L')

    # Create an image matrix with white pixels being false, and black being true
    bool_image_matrix = np.array(image) == 0

    # Get number of points in y and x (num of rows/cols in the original image)
    total_y_points, total_x_points = bool_image_matrix.shape

    # Image needs to be a square to construct a square Hamiltonian
    if total_x_points != total_y_points:
        sys.exit("ERROR: Image must be a square")
    
    grid_size = total_x_points

    # Create a mesh for when constructing the Hamiltonian

    potential_matrix = np.where(bool_image_matrix, 0, boundary_value) # MAKE THIS USER INPUTTED

    # Save debug information
    debugger.debug_store(bool_image_matrix, "./debug/bool_image.mat")
    debugger.debug_store(potential_matrix, "./debug/position_mesh.mat")

    image = np.array(image)
    # Perform Canny edge detection
    edges = cv2.Canny(image, 50, 150)
    
    return (potential_matrix, grid_size, edges)

def get_potential_from_shape(shape: str, grid_info: list, debugger: Debugging, boundary_value):
    
    x_start = grid_info[0]
    x_end = grid_info[1]
    y_start = grid_info[2]
    y_end = grid_info[3]

    grid_size = grid_info[4]
    grid_step = grid_info[5]

    L_x = x_end - x_start
    L_y = y_end - y_start

    if L_x <= 0 or L_y <=0:
        sys.exit("Error: Length in x or y is negative or equal to 0")

    X,Y = np.meshgrid(np.linspace(x_start, x_end, grid_size,
    dtype=float),np.linspace(y_start, y_end, grid_size,
    dtype=float))

    if shape == "square":
        if L_x != L_y:
            sys.exit("Error: Length in x must be same as y for a square") 
        potential_matrix = 0*X
    
    potential_matrix = np.full((grid_size, grid_size), boundary_value)
    if shape == "rectangle":
        center = grid_size // 2
        temp_x = int(L_x / (2*grid_step))
        temp_y = int(L_y / (2*grid_step))

        potential_matrix[center - temp_x : center + temp_x + 1, 
                         center - temp_y : center + temp_y + 1] = 0
    
    if shape == "e_triangle":
        # Triangle properties
        height = np.sqrt(3) / 2 * L_x  # Height of the equilateral triangle
        half_base = L_x / 2  # Half the base width

        # Define the triangle's bounding lines
        left_line = (Y >= np.sqrt(3) * (X + half_base))  # Left side
        right_line = (Y >= -np.sqrt(3) * (X - half_base))  # Right side
        bottom_line = (Y <= height / 2)  # Base

        # Combine the conditions for the triangular region
        triangle_mask = left_line & right_line & bottom_line

        # Set the potential to 0 inside the triangle
        potential_matrix[triangle_mask] = 0

    return potential_matrix



def construct_hamiltonian(potential_matrix, grid_size, debugger: Debugging, boundary_value: float):

    r"""
    Following created by Wai Jui Wong, paper at https://www.researchgate.net/publication/356858518_Solving_2D_Time_Independent_Schrodinger_Equation_Using_Numerical_Method
    """
    #Construct 2D Laplacian
    diag = np.ones([grid_size])
    diags = np.array([diag, -2*diag, diag])
    D = sp.sparse.spdiags(diags, np.array([-1, 0, 1]), grid_size, grid_size)

    # Construct Kinetic energy operator
    # See paper for why we do this
    K = -1/2 * sp.sparse.kronsum(D, D)

    V = potential_matrix.reshape(grid_size, grid_size)  # Reshape into 2D grid
    
    # Apply infinite potential at the boundaries by setting large values at the boundary indices
    V[0, :] = boundary_value  # Top boundary
    V[-1, :] = boundary_value  # Bottom boundary
    V[:, 0] = boundary_value  # Left boundary
    V[:, -1] = boundary_value  # Right boundary
    
    # Convert the potential into a sparse matrix
    V_sparse = sp.sparse.diags(V.flatten(), 0)  # Flatten V and convert to sparse

    # print(V_sparse.toarray())

    # Construct H
    H = K + V_sparse

    debugger.debug_store(H, "./debug/Ham.mat")
    # for row in H.toarray():
    #     print(row)
    return H