import matplotlib.pyplot as plt
import numpy as np

def plot_potential(potential_matrix, potential_type, grid_info, is_shape):
    
    if not is_shape:
        plt.figure(figsize=(6, 6))
        plt.imshow(potential_matrix, extent=[0, grid_info[4], 0, grid_info[4]], origin='lower', cmap='coolwarm', alpha=0.8)
        # plt.colorbar(label="Potential")

        # plt.xlabel("x")
        # plt.ylabel("y")
        # plt.title("Potential Matrix")
        plt.grid()
        plt.savefig(f"./plots/{potential_type}_plots/potential_plot.png")
        plt.close()
    else:
        plt.figure(figsize=(6, 6))
        plt.imshow(potential_matrix, extent=[grid_info[0], grid_info[1], grid_info[2], grid_info[3]], origin='lower', cmap='coolwarm', alpha=0.8)
        # plt.colorbar(label="Potential")

        # plt.xlabel("x")
        # plt.ylabel("y")
        # plt.title("Potential Matrix")
        plt.grid()
        plt.savefig(f"./plots/{potential_type}_plots/potential_plot.png")
        plt.close()
        


def plot_eigenfunctions_from_image(eigenvectors, potential_info, max_level, image_file):
    N = potential_info[1]
    for state in range(max_level):
        plt.figure(state, figsize=(6, 6))
        eig = plt.imshow(eigenvectors.T[state].reshape((N,N)), cmap="gray")
        #plt.title(f"State {state} eigenfunction", fontsize=16)
        plt.axis("off")
        # plt.colorbar(eig)
        plt.tight_layout()
        plt.savefig(f"./plots/{image_file}_plots/{state}/{state}_eigenfunction.png")
        plt.close()

def plot_prob_densities_from_image(eigenvectors, potential_info, max_level, image_file):
    N = potential_info[1]
    edges = potential_info[2]
    for state in range(max_level):
        plt.figure(state, figsize=(6, 6))
        plt.imshow(edges, cmap="gray", alpha = 0.3)
        prob_density = (np.abs(eigenvectors.T[state].reshape((N,N))))**2
        eig = plt.imshow(prob_density, cmap="viridis", alpha=0.7)
        plt.title(f"State {state} probability density", fontsize=16)
        plt.axis("off")
        # plt.colorbar(eig)
        plt.tight_layout()
        plt.savefig(f"./plots/{image_file}_plots/{state}/{state}_prob_density.png")
        plt.close()

def plot_eigenfunctions_from_shape(eigenvectors, grid_size, max_level, potential_type):
    for state in range(max_level):
        plt.figure(state, figsize=(6, 6))
        eig = plt.imshow(eigenvectors.T[state].reshape((grid_size,grid_size)), cmap="gray")
        #plt.title(f"State {state} eigenfunction", fontsize=16)
        plt.axis("off")
        # plt.colorbar(eig)
        plt.tight_layout()
        plt.savefig(f"./plots/{potential_type}_plots/{state}/{state}_eigenfunction.png")
        plt.close()

def plot_prob_densities_from_shape(eigenvectors, grid_size, max_level, potential_type):
    for state in range(max_level):
        plt.figure(state, figsize=(8, 8))
        prob_density = (np.abs(eigenvectors.T[state].reshape((grid_size,grid_size))))**2
        eig = plt.imshow(prob_density, cmap="viridis")
        plt.title(f"State {state} probability density", fontsize=16)
        plt.axis("off")
        # plt.colorbar(eig)
        plt.tight_layout()
        plt.savefig(f"./plots/{potential_type}_plots/{state}/{state}_prob_density.png")
        plt.close()

# def plot_eigenfunction_zero_crossings(eigenvectors, potential_info, max_level, image_file):
#     N = potential_info[1]
#     edges = potential_info[2]
#     for state in range(max_level):
#         plt.figure(state, figsize=(8, 8))
#         print(f"state {state} zero's calculating")
#         eigenfunction = eigenvectors.T[state].reshape((N, N))
        
#         zero_crossings = np.isclose(eigenfunction, 0, atol=1e-5)
#         plt.imshow(edges, cmap="gray", alpha=0.3)
        
#         zero_points = np.argwhere(zero_crossings)
#         for y, x in zero_points:
#             plt.scatter(x, y, color='red', s=10, zorder=5)  # Plot each point

#         plt.title(f"State {state} zero crossings", fontsize=16)
#         plt.axis("off")
#         plt.tight_layout()
        
#         # Save the figure
#         plt.savefig(f"./plots/{image_file}_plots/{state}/{state}_zero_crossings.png")

def plot_nodal_lines(eigenvectors, grid_size, max_level, potential_type):
    for state in range(max_level):
        fig, ax = plt.subplots(1, 1, figsize=(6,6))
        ax.contour(eigenvectors.T[state].reshape((grid_size,grid_size)), levels=[0], colors='black', linewidths=1.0)
        plt.setp(ax, xticks=[], yticks=[])
        ax.set_aspect('equal')
        plt.savefig(f"./plots/{potential_type}_plots/{state}/{state}_nodal_lines.png")
        plt.close()
