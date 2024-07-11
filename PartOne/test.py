import numpy as np
import utils
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
    dct_library_result = utils.dct_library(first_row)
    formatted_dct = ["{:.2e}".format(val) for val in dct_library_result]
    print("DCT library results: \n", formatted_dct) 

def test_dct2_library():
    print('--------------------------TEST DCT2 LIBRARY--------------------------')
    dct2_library_result = utils.dct2_library(block_8x8)
    np.set_printoptions(precision=2, suppress=False, formatter={'float': '{:0.2e}'.format})
    print("DCT2 Library results: \n", dct2_library_result)

def test_dct_homeMade():
    print('--------------------------TEST DCT HOME MADE--------------------------')
    dct = utils.dct_homeMade(first_row)
    formatted_dct = ["{:.2e}".format(val) for val in dct]
    print("DCT HomeMade results: \n", formatted_dct)

def test_dct2_homeMade():
    print('--------------------------TEST DCT2 HOME MADE--------------------------')
    dct2_homeMade = utils.dct2_homeMade(block_8x8)
    np.set_printoptions(precision=2, suppress=False, formatter={'float': '{:0.2e}'.format})
    print("DCT2 HomeMade results: \n", dct2_homeMade)

def test_N(): 
    # Dimensioni delle matrici NxN (da 50 a 900 con passo 50)
    matrix_dimensions = list(range(200, 1000, 50))

    times_scipy_dct = []
    times_my_dct = []

    for n in matrix_dimensions:
        print("Dimension: ", n)

        # Creazione di una matrice random
        np.random.seed(5)
        matrix = np.random.uniform(low=0.0, high=255.0, size=(n, n))

        # Calcolo del tempo di esecuzione con scipy DCT2
        time_scipy = timeit.timeit(lambda: utils.dct2_library(matrix), number=1)
        times_scipy_dct.append(time_scipy)

        # Calcolo del tempo di esecuzione con la tua DCT2
        time_my_dct = timeit.timeit(lambda: utils.dct2_homeMade(matrix), number=1)
        times_my_dct.append(time_my_dct)

    return times_scipy_dct, times_my_dct, matrix_dimensions

def plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions):
    # Dividiamo per 10^6 in modo da visualizzare le righe di comparazione vicino alla riga 
    n3 = [n**3 /1e5 for n in matrix_dimensions]    
    n2_logn = [n**2 * np.log(n) / 1e8 for n in matrix_dimensions]

    plt.figure(figsize=(10, 6))
    plt.semilogy(matrix_dimensions, times_scipy_dct, label='Library DCT2', color="tab:green")
    plt.semilogy(matrix_dimensions, n2_logn, label='n^2 * log(n)', color="tab:green", linestyle='dashed')
    plt.semilogy(matrix_dimensions, times_my_dct, label='DCT2 created', color="tab:blue")
    plt.semilogy(matrix_dimensions, n3, label='n^3', color="tab:blue", linestyle='dashed')
    
    plt.xlabel('Dimensione N')
    plt.ylabel('Tempo di esecuzione in secondi')
    plt.title('Tempi di esecuzione della DCT2 al variare della dimensione N')
    plt.legend()
    plt.grid(True)

    # Salva l'immagine del grafico
    #plt.savefig('Prima Parte/grafico_dct_times.png')

    plt.show()