import numpy as np
from utils import dct2_homeMade, dct2_library, dct_library, dct_homeMade
import timeit
import matplotlib.pyplot as plt

block_8x8 = np.array([
        [231, 32, 233, 161, 24, 71, 140, 245],
        [247, 40, 248, 245, 124, 204, 36, 107],
        [234, 202, 245, 167, 9, 217, 239, 173],
        [193, 190, 100, 167, 43, 180, 8, 70],
        [11, 24, 210, 177, 81, 243, 8, 112],
        [97, 195, 203, 47, 125, 114, 165, 181],
        [193, 70, 174, 167, 41, 30, 127, 245],
        [87, 149, 57, 192, 65, 129, 178, 228]
    ])

first_row = np.array(
        [231, 32, 233, 161, 24, 71, 140, 245]
    )

def test_dct_library():
    print('--------------------------TEST DCT LIBRARY--------------------------')
    dct_library_result = dct_library(first_row)
    formatted_dct = ["{:.2e}".format(val) for val in dct_library_result]
    print("DCT library results: \n", formatted_dct) 

def test_dct2_library():
    print('--------------------------TEST DCT2 LIBRARY--------------------------')
    dct2_library_result = dct2_library(block_8x8)
    np.set_printoptions(precision=2, suppress=False, formatter={'float': '{:0.2e}'.format})
    print("DCT2 Library results: \n", dct2_library_result)

def test_dct_homeMade():
    print('--------------------------TEST DCT HOME MADE--------------------------')
    dct = dct_homeMade(first_row)
    formatted_dct = ["{:.2e}".format(val) for val in dct]
    print("DCT HomeMade results: \n", formatted_dct)

def test_dct2_homeMade():
    print('--------------------------TEST DCT2 HOME MADE--------------------------')
    dct2_hm = dct2_homeMade(block_8x8)
    np.set_printoptions(precision=2, suppress=False, formatter={'float': '{:0.2e}'.format})
    print("DCT2 HomeMade results: \n", dct2_hm)

# Matrix sizes for benchmarking
sizes_matrix = [50, 100, 200, 400, 800]

# Theoretical times based on complexity
homeMade_theoretical_times = [n**3 for n in sizes_matrix]
lib_theoretical_times = [n**2 * np.log(n) for n in sizes_matrix]

# Lists to store actual measured times
homeMade_times = []
lib_times = []

# Generate a random N x N matrix with values ranging from 0 to 255.
def random_matrix(N):
    return np.random.randint(low=0, high=256, size=(N, N), dtype=np.uint8)

# Measure and print the execution times for custom and library DCT2 implementations.
def get_times():
    for size in sizes_matrix:
        matrix = random_matrix(size)
        print(f'--- Matrix {len(matrix)}x{len(matrix[0])} ---')
        homeMade_times.append(timeit.timeit(lambda: dct2_homeMade(matrix), number=1))
        print(f'Executed DCT2 homemade in {homeMade_times[-1]} sec')
        lib_times.append(timeit.timeit(lambda: dct2_library(matrix), number=1))
        print(f'Executed DCT2 Library in {lib_times[-1]} sec')

# Scale theoretical times to practical times using a median-based scaling factor.
def scale_theoretical_to_practical(theoretical, practical):
    scaling_factor = np.median(np.array(practical) / np.array(theoretical))
    return [t * scaling_factor for t in theoretical]

# Plot the execution times on a semilog scale.
def plot_times():
    scaled_my_theoretical_times = scale_theoretical_to_practical(homeMade_theoretical_times, homeMade_times)
    scaled_lib_theoretical_times = scale_theoretical_to_practical(lib_theoretical_times, lib_times)
    
    plt.figure()
    plt.semilogy(sizes_matrix, scaled_my_theoretical_times, color='darkgoldenrod', label='DCT2 HomeMade theoretical time', linestyle='dashed')
    plt.semilogy(sizes_matrix, homeMade_times, color='orange', label='DCT2 HomeMade')
    
    plt.semilogy(sizes_matrix, scaled_lib_theoretical_times, color='tab:blue', label='DCT2 Library theoretical time', linestyle='dashed')
    plt.semilogy(sizes_matrix, lib_times, color='tab:blue', label='DCT2 Library')
    plt.xticks(sizes_matrix)
    
    plt.xlabel('Matrix dimension')
    plt.ylabel('Time (s)')
    plt.title('Time of DCT2 execution')
    
    plt.legend()
    plt.grid(True)

    plt.savefig('PartOne/results/time_dct_graph.png')

    plt.show()