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

    # log_p_r_sstransition_matrx = [
    #     [p_g_transition, 1-p_r_transition],
    #     [1-p_g_transition, p_r_transition]
    # ]
    #
    # steady_state_matrix = [p_g_steady_state, p_r_steady_state]
    #
    # sum_en = 0
    #
    # for i, row in enumerate(transition_matrx):
    #     for j, col in enumerate(row):
    #         if col == 0:
    #             log_col = 0
    #         else:
    #             log_col = math.log(col)
    #
    #         sum_en = sum_en + steady_state_matrix[i]*col*log_col
    #
    # entropy2 = -1 * sum_en

    return entropy  # , entropy2


def get_transition_probabilities(h_m_row):
    g_to_g = 0
    s_from_g = 0
    r_to_r = 0
    s_from_r = 0

    for i in range(len(h_m_row)-1):
        st = h_m_row[i]
        end = h_m_row[i+1]

        if st == 1:
            s_from_g += 1
            if end == 1:
                g_to_g += 1
        else:
            s_from_r += 1
            if end == 0:
                r_to_r += 1

    if s_from_g == 0:
        p_g = 0
    else:
        p_g = g_to_g/s_from_g

    if s_from_r == 0:
        p_r = 0
    else:
        p_r = r_to_r/s_from_r

    return p_g, p_r


# heat_map_row = [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1]
# heat_map_row = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
# heat_map_row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0]
heat_map_row = [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

prob_g, prob_r = get_transition_probabilities(heat_map_row)

ent1 = calculate_entropy(prob_g, prob_r)

print(prob_g, prob_r)

print(ent1)
