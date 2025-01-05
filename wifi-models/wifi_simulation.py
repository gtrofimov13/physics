import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, Optional

# Configuration parameters
ROOM_SIZE: int = 101  # Size of square room in centimeters
WAVELENGTH_5GHZ: float = 6.0  # WiFi wavelength in centimeters (5GHz)
WAVELENGTH_24GHZ: float = 12.5  # WiFi wavelength in centimeters (2.4GHz)
SOURCE_OFFSET: int = 5  # Distance of source from room edges

def setup_simulation_parameters(room_size: int, wavelength: float) -> Tuple[float, int, int]:
    """
    Initialize core simulation parameters.
    
    Args:
        room_size: Length/width of square room in centimeters
        wavelength: EM wavelength in centimeters
    
    Returns:
        Tuple containing:
        - Wave number squared ((2π/λ)²)
        - x-position of source
        - y-position of source
    """
    k_squared = (2 * np.pi / wavelength) ** 2
    source_x = source_y = room_size - SOURCE_OFFSET
    return k_squared, source_x, source_y

def create_simulation_matrices(room_size: int) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Create initial matrices needed for simulation.
    
    Args:
        room_size: Length/width of square room
    
    Returns:
        Tuple containing:
        - Index matrix (reshaped to column vector)
        - Empty equation matrix
        - Empty source term vector
    """
    total_size = room_size ** 2
    
    # Create index matrix (all ones, reshaped to column)
    index_matrix = np.ones((total_size, 1))
    
    # Initialize equation and source matrices
    equation_matrix = np.zeros((total_size, total_size))
    source_vector = np.zeros((total_size, 1))
    
    return index_matrix, equation_matrix, source_vector

def build_helmholtz_matrix(
    room_size: int, 
    k_squared: float, 
    index_matrix: np.ndarray, 
    source_pos: Tuple[int, int]
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Build the Helmholtz equation matrix exactly matching original implementation.
    """
    total_size = room_size ** 2
    equation_matrix = np.zeros((total_size, total_size))
    source_vector = np.zeros((total_size, 1))
    
    # Set source position
    source_x, source_y = source_pos
    source_vector[source_x * room_size + source_y] = 1
    
    # Build matrix exactly as in original
    for j in range(total_size):
        for i in range(total_size):
            if i == j == 0:   
                equation_matrix[i,j] = -2 + k_squared * index_matrix[j]**2
                equation_matrix[i,j+1] = 1
                equation_matrix[i,j+room_size] = 1
            
            elif 0 < i == j < room_size-1:
                equation_matrix[i,j] = -3 + k_squared * index_matrix[j]**2
                equation_matrix[i,j+room_size] = 1
                equation_matrix[i,j+1] = 1
                equation_matrix[i,j-1] = 1
                
            elif i == j == room_size-1:
                equation_matrix[i,j] = -2 + k_squared * index_matrix[j]**2
                equation_matrix[i,j+room_size] = 1
                equation_matrix[i,j-1] = 1
              
            elif room_size-1 < i == j < total_size-room_size:
                equation_matrix[i,j] = -4 + k_squared * index_matrix[j]**2
                equation_matrix[i,j+room_size] = 1
                equation_matrix[i,j+1] = 1
                equation_matrix[i,j-1] = 1
                equation_matrix[i,j-room_size] = 1
                
            elif i == j == total_size-room_size:   
                equation_matrix[i,j] = -2 + k_squared * index_matrix[j]**2
                equation_matrix[i,j+1] = 1
                equation_matrix[i,j-room_size] = 1
            
            elif total_size-room_size < i == j < total_size-1:
                equation_matrix[i,j] = -3 + k_squared * index_matrix[j]**2
                equation_matrix[i,j-room_size] = 1
                equation_matrix[i,j+1] = 1
                equation_matrix[i,j-1] = 1
                
            elif i == j == total_size-1:
                equation_matrix[i,j] = -2 + k_squared * index_matrix[j]**2
                equation_matrix[i,j-room_size] = 1
                equation_matrix[i,j-1] = 1
    
    return equation_matrix, source_vector

def solve_field(equation_matrix: np.ndarray, source_vector: np.ndarray, room_size: int) -> np.ndarray:
    """
    Solve the Helmholtz equation and reshape result to room dimensions.
    
    Args:
        equation_matrix: Matrix of field equations
        source_vector: Vector containing source terms
        room_size: Length/width of square room
    
    Returns:
        2D array of field values
    """
    field_vector = np.linalg.solve(equation_matrix, source_vector)
    return field_vector.reshape((room_size, room_size))

def plot_field(field: np.ndarray, title: Optional[str] = "Electric Field Distribution") -> None:
    """
    Visualize the field distribution.
    
    Args:
        field: 2D array of field values
        title: Optional plot title
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(field, cmap='jet', aspect='equal')
    plt.colorbar(label='Field Strength')
    plt.title(title)
    plt.show()

def simulate_wifi_field(
    room_size: int = ROOM_SIZE, 
    wavelength: float = WAVELENGTH_5GHZ
) -> np.ndarray:
    """
    Run complete WiFi field simulation.
    
    Args:
        room_size: Length/width of square room
        wavelength: EM wavelength in centimeters
    
    Returns:
        2D array of field values
    """
    # Setup simulation
    k_squared, source_x, source_y = setup_simulation_parameters(room_size, wavelength)
    index_matrix, _, _ = create_simulation_matrices(room_size)
    
    # Build and solve equation system
    equation_matrix, source_vector = build_helmholtz_matrix(
        room_size, k_squared, index_matrix, (source_x, source_y)
    )
    
    return solve_field(equation_matrix, source_vector, room_size)

if __name__ == "__main__":
    # Run simulation with default parameters
    field = simulate_wifi_field()
    plot_field(field)
