import PartOne.test as test

test.test_dct_library()
test.test_dct2_library()
test.test_dct_homeMade()
test.test_dct2_homeMade()
times_scipy_dct, times_my_dct, matrix_dimensions = test.test_N()
test.plot_dct_times(times_scipy_dct, times_my_dct, matrix_dimensions)
