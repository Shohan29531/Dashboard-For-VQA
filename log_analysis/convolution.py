import numpy as np
from scipy.signal import convolve2d

# # Example matrix

# Z = [[1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 1], [0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1], [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0], [1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1], [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 0]]

# matrix = np.array(Z)


all_one_kernel = np.array([
    [1, 1, 1, 1, 1, 1],
])


# plus_kernel_with_ones = np.array([
#     [0, 1, 0],
#     [1, 1, 1],
#     [0, 1, 0]
# ])

# minus_kernel_with_ones = np.array([
#     [0, 0, 0],
#     [1, 1, 1],
#     [0, 0, 0]
# ])

# slash_kernel_with_ones = np.array([
#     [0, 0, 1],
#     [0, 1, 0],
#     [1, 0, 0],
# ])

# backslash_kernel_with_ones = np.array([
#     [1, 0, 0],
#     [0, 1, 0],
#     [0, 0, 1],
# ])




all_zero_kernel = np.array([
    [0, 0, 0, 0, 0, 0],
])

# plus_kernel_with_zeroes = np.array([
#     [1, 0, 1],
#     [0, 0, 0],
#     [1, 0, 1]
# ])

# minus_kernel_with_zeroes = np.array([
#     [1, 1, 1],
#     [0, 0, 0],
#     [1, 1, 1],
# ])

# slash_kernel_with_zeroes = np.array([
#     [1, 1, 0],
#     [1, 0, 1],
#     [0, 1, 1]
# ])

# backslash_kernel_with_zeroes = np.array([
#     [0, 1, 1],
#     [1, 0, 1],
#     [1, 1, 0],
# ])


isolated_one = np.array([
    [0, 0, 1, 0, 0]
])

isolated_zero = np.array([
    [1, 1, 0, 1, 1]
])

island_ones_1 = np.array([
    [0, 1, 1, 0]
])

island_ones_2 = np.array([
    [0, 1, 1, 1, 0]
])

island_ones_3 = np.array([
    [0, 1, 1, 1, 1, 0]
])


island_zeroes_1 = np.array([
    [1, 0, 0, 1]
])

island_zeroes_2 = np.array([
    [1, 0, 0, 0, 1]
])

island_zeroes_3 = np.array([
    [1, 0, 0, 0, 0, 1]
])




switch_kernel_1 = np.array([
    [1, 0, 1, 0, 1, 0]
])

switch_kernel_2 = np.array([
    [0, 1, 0, 1, 0, 1]
])

switch_kernel_3 = np.array([
    [1, 1, 0, 0, 1, 1]
])

switch_kernel_4 = np.array([
    [1, 0, 1, 1, 0, 1]
])


all_kernels = [
               (all_one_kernel, "all_one_kernel", 6),
               (all_zero_kernel, "all_zero_kernel", 6),
               (switch_kernel_1, "switch_kernel_1", 6),
               (switch_kernel_2, "switch_kernel_2", 6),
               (switch_kernel_3, "switch_kernel_3", 6),
               (switch_kernel_4, "switch_kernel_4", 6),
               (isolated_one, "isolated_one", 3),
               (isolated_zero, "isolated_zero", 3),
               (island_ones_1, "island_ones_1", 4),
               (island_ones_2, "island_ones_2", 5),
               (island_ones_3, "island_ones_3", 6),
               (island_zeroes_1, "island_zeroes_1", 4),
               (island_zeroes_2, "island_zeroes_2", 5),
               (island_zeroes_3, "island_zeroes_3", 6),
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
    "All_zeroes",
    "Switch_pattern_1",
    "Switch_pattern_2",
    "Switch_pattern_3",
    "Switch_pattern_4",
    "isolated_one",
    "isolated_zero",
    "island_ones_1",
    "island_ones_2",
    "island_ones_3",
    "island_zeroes_1",
    "island_zeroes_2",
    "island_zeroes_3",
    "Rating",
    "Mean-Centered_rating",
    "MC_with_MinMax",
    ]