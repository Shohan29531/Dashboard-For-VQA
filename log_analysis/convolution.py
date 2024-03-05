import numpy as np
from scipy.signal import convolve2d

# # Example matrix

# Z = [[1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0]]

# matrix = np.array(Z)


all_one_kernel = np.array([
    [1, 1, 1],
])


plus_kernel_with_ones = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
])

minus_kernel_with_ones = np.array([
    [0, 0, 0],
    [1, 1, 1],
    [0, 0, 0]
])

slash_kernel_with_ones = np.array([
    [0, 0, 1],
    [0, 1, 0],
    [1, 0, 0],
])

backslash_kernel_with_ones = np.array([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 1],
])




all_zero_kernel = np.array([
    [1, 1, 1],
])

plus_kernel_with_zeroes = np.array([
    [1, 0, 1],
    [0, 0, 0],
    [1, 0, 1]
])

minus_kernel_with_zeroes = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [1, 1, 1],
])

slash_kernel_with_zeroes = np.array([
    [1, 1, 0],
    [1, 0, 1],
    [0, 1, 1]
])

backslash_kernel_with_zeroes = np.array([
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0],
])


switch_kernel_1 = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1],
])

switch_kernel_2 = np.array([
    [0, 1, 0],
    [1, 0, 1],
    [0, 1, 0],
])


all_kernels = [
               (all_one_kernel, 3),
               (plus_kernel_with_ones, 5),
               (minus_kernel_with_ones, 3),
               (slash_kernel_with_ones, 3),
               (backslash_kernel_with_ones, 3),
               (all_zero_kernel, 0),
               (plus_kernel_with_zeroes, 4),
               (minus_kernel_with_zeroes, 6),
               (slash_kernel_with_zeroes, 6),
               (backslash_kernel_with_zeroes, 6),
               (switch_kernel_1, 5),
               (switch_kernel_2, 4)
              ]

# Perform convolution
# convolution_result = convolve2d(matrix, plus_sign_kernel_with_ones, mode='valid')

# # Check for matches (the sum of the plus sign kernel is 5)
# matches = convolution_result == 5

# if np.any(matches):
#     print("Plus sign pattern found")
#     print(matches)
# else:
#     print("Plus sign pattern not found")

name_row = [
    "All_ones",
    "Plus_with_ones",
    "Minus_with_ones",
    "Slash_with_ones",
    "Backslash_with_ones",
    "All_zeroes",
    "Plus_with_zeroes",
    "Minus_with_zeroes",
    "Slash_with_zeroes",
    "Backslash_with_zeroes",
    "Switch_pattern_ones",
    "Switch_pattern_zeroes",
    "Rating",
    "Mean-Centered_rating",
    "MC_with_MinMax"
    ]