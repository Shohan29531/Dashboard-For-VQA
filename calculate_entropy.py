import math


def calculate_entropy(p_g_transition, p_r_transition):
    p_g_steady_state = (p_r_transition - 1) / (p_g_transition + p_r_transition - 2)
    p_r_steady_state = (p_g_transition - 1) / (p_g_transition + p_r_transition - 2)

    if p_g_steady_state == 0:
        log_p_g_ss = 0
    else:
        log_p_g_ss = math.log2(p_g_steady_state)

    if p_r_steady_state == 0:
        log_p_r_ss = 0
    else:
        log_p_r_ss = math.log2(p_r_steady_state)

    entropy = - p_g_steady_state * log_p_g_ss - p_r_steady_state * log_p_r_ss

    transition_matrx = [
        [p_g_transition, 1-p_r_transition],
        [1-p_g_transition, p_r_transition]
    ]

    steady_state_matrix = [p_g_steady_state, p_r_steady_state]

    sum_en = 0

    for i, row in enumerate(transition_matrx):
        for j, col in enumerate(row):
            if col == 0:
                log_col = 0
            else:
                log_col = math.log2(col)

            sum_en = sum_en + steady_state_matrix[i]*col*log_col

    entropy2 = -1 * sum_en

    return entropy, entropy2

