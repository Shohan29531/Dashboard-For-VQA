import math
import plotly.express as px
import numpy as np


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

    return entropy, p_g_steady_state, p_r_steady_state  # , entropy2


def get_steady_state_probabilities(h_m_row):
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


def calculate_chain_entropy(h_m_row, p_g_steady, p_r_steady):
    tran_prob_matrix = [p_g_steady, p_r_steady]
    ent_sum = 0
    for i in range(1, len(h_m_row)):
        tmp_sum = 0
        for x1 in range(2):
            for x2 in range(2):
                joint_prob = tran_prob_matrix[x1] * tran_prob_matrix[x2]
                p_x1 = tran_prob_matrix[x2]
                if p_x1 == 0 or joint_prob == 0:
                    log_x1_x2 = 0
                else:
                    log_x1_x2 = math.log2(p_x1/joint_prob)
                tmp_sum = tmp_sum + joint_prob * log_x1_x2

        ent_sum = ent_sum + tmp_sum

    ent_sum = 1/(len(h_m_row)-1) * ent_sum

    return ent_sum


heat_map_rows_1 = [
    [1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

heat_map_rows_2 = [
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


ents = []
frms = [f'{k}' for k in range(len(heat_map_rows_1[0]))]

out_hm = []

ent_arr_1 = []
ent_arr_2 = []

prob_g, prob_r = get_transition_probabilities(np.array(heat_map_rows_1))

ent1, g_steady, r_steady = calculate_entropy(prob_g, prob_r)

ent2 = calculate_chain_entropy(heat_map_row, g_steady, r_steady)

ents.append(f'row-{c}-entropy = {ent1:.3f}')
out_hm.append(heat_map_row)
ents.append(f'row-{c}-chain_entropy = {ent2:.3f}')
out_hm.append(heat_map_row)


fig = px.imshow(out_hm, x=frms, y=ents, text_auto=True)
fig.update_xaxes(side="bottom")
fig.update_coloraxes(showscale=False)
fig.show()

