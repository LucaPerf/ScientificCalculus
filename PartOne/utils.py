import numpy as np
from scipy.fft import dct


def dct2_homeMade(matrix):
    N, M = matrix.shape
    #assert N == M, "The matrix must be square to ensure O(N^3) complexity."

    # Application of DCT to each row
    result = np.copy(matrix.astype('float64'))
    for i in range(N):
        result[i, :] = dct_homeMade(result[i, :])
    
    # Application of DCT to each column
    for j in range(M):
        result[:, j] = dct_homeMade(result[:, j])
    
    return result

def dct_homeMade(input_vector):
    return dct_transform(len(input_vector), input_vector)

def dct_transform(n, vector):
    N = n
    base = np.zeros((N, N))
    for k in range(N):
        for i in range(N):
            base[k, i] = np.cos((k * np.pi * (2 * i + 1)) / (2 * N))

    coeff = np.dot(base, vector)
    coeff[0] = coeff[0] / np.sqrt(N)
    coeff[1:] = coeff[1:] * np.sqrt(2 / N)
    
    return coeff

def dct_library(x):
    return dct(x.T, norm='ortho')

def dct2_library(matrix):
    return dct(dct(matrix.T, norm='ortho').T, norm='ortho')
