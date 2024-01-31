import random
import numpy as np
from fractions import Fraction
import pandas as pd


def get_dum_pred_from_f1(gt_f__, org_f1, pred_ct, obj_list_a):
    dd_df = pd.read_csv(gt_f__)
    dd_df = dd_df.transpose()
    dd_df.columns = [x__.lower() for x__ in dd_df.iloc[0]]
    dd_df = dd_df.reindex(columns=obj_list_a).iloc[1:].transpose()
    dd_np = np.array(dd_df)

    unique, counts = np.unique(np.array(dd_df), return_counts=True)
    total_pred_c = sum(counts)
    pred_counts = dict(zip(unique, counts))
    fra_rep = [int(x) for x in str(Fraction(org_f1).limit_denominator()).split('/')]
    tp_frac = fra_rep[0] / 2
    fp_plus_fn_frac = fra_rep[1] - fra_rep[0]
    dum_pred_dfs = []
    for p_tp in range(pred_counts[1], 0, -1):
        new_dd_np = np.zeros(dd_np.shape).astype(int)
        p_fp_plus_fn = round((fp_plus_fn_frac / tp_frac) * p_tp)
        p_fn = pred_counts[1] - p_tp
        p_fp = p_fp_plus_fn - p_fn
        p_tn = total_pred_c - (p_tp + p_fn + p_fp)
        p_f1 = (2 * p_tp) / (p_tp + p_tp + p_fp + p_fn)
        p_dev = abs((p_f1 - org_f1) / p_f1)

        if p_tn < 0 or p_dev > 0.008:
            continue

        pos_posit = np.argwhere(dd_np == 1)
        pos_neg = np.argwhere(dd_np == 0)
        p_rc_samp = random.sample(range(0, pos_posit.shape[0]), p_tp)

        try:
            n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)
        except Exception as e:
            print(pos_neg.shape, p_fp)
            if p_fp < 0:
                p_fp = 0
            n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)

        tp_rrr, tp_ccc = pos_posit[:, 0][p_rc_samp], pos_posit[:, 1][p_rc_samp]
        fp_rrr, fp_ccc = pos_neg[:, 0][n_rc_samp], pos_neg[:, 1][n_rc_samp]

        new_dd_np[tp_rrr, tp_ccc] = 1
        new_dd_np[fp_rrr, fp_ccc] = 1

        new_dd_df = pd.DataFrame(new_dd_np, index=dd_df.index, columns=dd_df.columns).reset_index()
        new_dd_df = new_dd_df.rename(columns={"index": "Object"})

        dum_pred_dfs.append(new_dd_df)
        if len(dum_pred_dfs) >= pred_ct:
            break

    return dum_pred_dfs
