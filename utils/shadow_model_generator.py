import random
import numpy as np
from fractions import Fraction
import pandas as pd
from natsort import natsorted


def get_dum_pred_from_f1(gt_f__, org_f1, pred_ct, obj_list_a, limit_frame_count=-1):
    obj_list_a = natsorted(obj_list_a)
    dd_df = pd.read_csv(gt_f__)
    if limit_frame_count > 0:
        if len(list(dd_df.columns)) > limit_frame_count:
            dd_df = dd_df.iloc[:, :limit_frame_count]
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


def get_dum_pred_from_f1_eq_swap(gt_f__, pred_f___, org_f1, pred_ct, obj_list_a, limit_frame_count=-1):
    dd_df__ = pd.read_csv(pred_f___)
    if limit_frame_count > 0:
        if len(list(dd_df__.columns)) > limit_frame_count:
            dd_df__ = dd_df__.iloc[:, :limit_frame_count]

    dd_df__ = dd_df__.transpose()
    dd_df__.columns = [x__.lower() for x__ in dd_df__.iloc[0]]
    dd_df__ = dd_df__.reindex(columns=obj_list_a).iloc[1:].transpose()
    dd_np__ = np.array(dd_df__)
    unique__, counts__ = np.unique(dd_np__, return_counts=True)
    pred_counts__ = dict(zip(unique__, counts__))
    # print(pred_counts__)
    # tp_m__ = int(org_prec * pred_counts__[1])
    # print(tp_m__)

    dd_df = pd.read_csv(gt_f__)
    if limit_frame_count > 0:
        if len(list(dd_df.columns)) > limit_frame_count:
            dd_df = dd_df.iloc[:, :limit_frame_count]

    dd_df = dd_df.transpose()
    dd_df.columns = [x__.lower() for x__ in dd_df.iloc[0]]
    dd_df = dd_df.reindex(columns=obj_list_a).iloc[1:].transpose()
    dd_np = np.array(dd_df)

    unique, counts = np.unique(np.array(dd_df), return_counts=True)
    total_pred_c = sum(counts)
    pred_counts = dict(zip(unique, counts))

    cf_np = (2 * dd_np) + (-1 * dd_np__)
    cf_unique, cf_counts = np.unique(cf_np, return_counts=True)
    cf_stat = dict(zip(cf_unique, cf_counts))

    # fra_rep = [int(x) for x in str(Fraction(org_f1).limit_denominator()).split('/')]
    # if len(fra_rep) == 1:
    #     fra_rep.append(1)
    # tp_frac = fra_rep[0]/2
    # fp_plus_fn_frac = fra_rep[1] - fra_rep[0]
    dum_pred_dfs = []
    # for p_tp in range(pred_counts[1], 1, -1):
    # for p_tp in range(pred_counts[1]//6, pred_counts[1], 5):
    # starter = [pred_counts[1]//4, pred_counts[1]//8, 0, 0][strt_i]
    # for p_tp in range(pred_counts[1]-starter, 0, -1):
    # st_tp = pred_counts[1]
    # for p_tp in range(pred_counts[1], pred_counts[1]-1, -1):
    # for p_tp in range(1, pred_counts[1]+1, 1):
    # for p_tp in range(pred_counts[1]//3, pred_counts[1], 1):
    # for p_tp in range(pred_counts[1]//3, pred_counts[1], 1):
    # for p_tp in range(min([tp_m__+1, pred_counts[1]]), max([tp_m__-1, 1]), -1):
    # for p_tp in range(pred_counts[1]//4, pred_counts[1]+1, 1):
    new_dd_np = np.zeros(dd_np.shape).astype(int)
    # p_fp_plus_fn = round((fp_plus_fn_frac/tp_frac) * p_tp)
    # p_fn = pred_counts[1] - p_tp
    # p_fp = p_fp_plus_fn - p_fn
    # p_tn = total_pred_c - (p_tp + p_fn + p_fp)

    # print(cf_stat)

    p_tp = cf_stat[1] if 1 in cf_stat.keys() else 0
    p_tn = cf_stat[0] if 0 in cf_stat.keys() else 0
    p_fn = cf_stat[2] if 2 in cf_stat.keys() else 0
    p_fp = cf_stat[-1] if -1 in cf_stat.keys() else 0

    p_f1 = (2 * p_tp) / (p_tp + p_tp + p_fp + p_fn)
    p_dev = abs((p_f1 - org_f1) / p_f1)

    # print(f'TP:{p_tp}, TN:{p_tn}, FP:{p_fp}, FN:{p_fn}, TotP:{pred_counts[1]}')

    # if p_fp < 0:
    #     continue

    if p_tn < 0 or p_dev > 0.005:
        print(p_dev)
        # continue

    pos_posit = np.argwhere(dd_np == 1)
    pos_neg = np.argwhere(dd_np == 0)

    pos_fp = np.argwhere(cf_np == -1)

    p_rc_samp = random.sample(range(0, pos_posit.shape[0]), p_tp)

    # try:
    # n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)
    # except:
    #     print(pos_neg.shape, p_fp)
    # continue
    # if p_fp < 0:
    #     p_fp = 0
    # n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)

    tp_rrr, tp_ccc = pos_posit[:, 0][p_rc_samp], pos_posit[:, 1][p_rc_samp]
    # fp_rrr, fp_ccc = pos_neg[:, 0][n_rc_samp], pos_neg[:, 1][n_rc_samp]
    fp_rrr, fp_ccc = pos_fp[:, 0], pos_fp[:, 1]

    new_dd_np[tp_rrr, tp_ccc] = 1
    new_dd_np[fp_rrr, fp_ccc] = 1

    new_dd_df = pd.DataFrame(new_dd_np, index=dd_df.index, columns=dd_df.columns).reset_index()
    new_dd_df = new_dd_df.rename(columns={"index": "Object"})

    dum_pred_dfs.append(new_dd_df)
    # if len(dum_pred_dfs) >= pred_ct:
    #     break

    return dum_pred_dfs
