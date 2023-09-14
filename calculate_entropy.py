import math
import plotly.express as px


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

    return entropy, p_g_steady_state, p_r_steady_state  # , entropy2


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


def calculate_chain_entropy(h_m_row, p_g_steady, p_r_steady):
    tran_prob_matrix = [p_g_steady, p_r_steady]
    ent_sum = 0
    for i in range(len(h_m_row)):
        if i == 0:
            tmp_sum = 0
            for x in range(2):
                if tran_prob_matrix[x] == 0:
                    log_x = 0
                else:
                    log_x = math.log2(tran_prob_matrix[x])
                tmp_sum = tmp_sum + tran_prob_matrix[x] * log_x
        else:
            tmp_sum = 1
            for x1 in range(2):
                for x2 in range(2):
                    joint_prob = tran_prob_matrix[x1] * tran_prob_matrix[x2]
                    p_x2 = tran_prob_matrix[x2]
                    if p_x2 == 0 or joint_prob == 0:
                        log_x1_x2 = 0
                    else:
                        log_x1_x2 = math.log2(joint_prob/p_x2)
                    tmp_sum = tmp_sum + joint_prob * log_x1_x2

        ent_sum = ent_sum + tmp_sum

    ent_sum = 1/(len(h_m_row)-1) * ent_sum

    return ent_sum


heat_map_rows = [
    [1, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0],
]

ents = []
frms = [f'{k}' for k in range(len(heat_map_rows[0]))]

for c, heat_map_row in enumerate(heat_map_rows):
    prob_g, prob_r = get_transition_probabilities(heat_map_row)

    ent1, g_steady, r_steady = calculate_entropy(prob_g, prob_r)

    ent2 = calculate_chain_entropy(heat_map_row, g_steady, r_steady)
    # print(ent1)
    ents.append(f'row-{c}-entropy = {ent1:.3f}')


fig = px.imshow(heat_map_rows, x=frms, y=ents, text_auto=True)
fig.update_xaxes(side="bottom")
fig.update_coloraxes(showscale=False)
fig.show()

