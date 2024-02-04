import random
import numpy as np
from fractions import Fraction
import pandas as pd
from natsort import natsorted


def get_dum_pred_from_f1(gt_f__, org_f1, obj_list_all, limit_frame_count=-1):
    obj_list_all = natsorted(obj_list_all)
    obj_dfs = []
    for obj in obj_list_all:
        obj_list_a = [obj]
        dd_df = pd.read_csv(gt_f__)
        dd_df = dd_df.transpose()
        if limit_frame_count > 0:
            if len(list(dd_df.columns)) > limit_frame_count:
                dd_df = dd_df.iloc[:, :limit_frame_count]
        dd_df.columns = [x__.lower() for x__ in dd_df.iloc[0]]
        dd_df = dd_df.reindex(columns=obj_list_a).iloc[1:].transpose()
        dd_np = np.array(dd_df)

        unique, counts = np.unique(np.array(dd_df), return_counts=True)
        total_pred_c = sum(counts)
        pred_counts = dict(zip(unique, counts))
        fra_rep = [int(x) for x in str(Fraction(org_f1).limit_denominator()).split('/')]
        tp_frac = fra_rep[0] / 2
        fp_plus_fn_frac = fra_rep[1] - fra_rep[0]

        try:
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

                new_dd_df = pd.DataFrame(new_dd_np, index=dd_df.index, columns=dd_df.columns)  # .reset_index()
                # new_dd_df = new_dd_df.rename(columns={"index": "Object"})

                obj_dfs.append(new_dd_df)

                break
        except:
            obj_dfs.append(dd_df)

    if len(obj_dfs) > 1:
        dum_pred_dfs = [pd.concat(obj_dfs).reset_index().rename(columns={"index": "Object"})]
    else:
        dum_pred_dfs = [obj_dfs[0].reset_index().rename(columns={"index": "Object"})]

    return dum_pred_dfs


if __name__ == '__main__':
    object_list = [
        "Building", "Bus", "Bus Stop", "Car", "Motorcycle", "Person",
        "Person with a disability", "White Cane", "Yard Waste"
    ]
    object_list = [ooo.lower() for ooo in object_list]
    shadows = get_dum_pred_from_f1(
        gt_f__='/Users/ibk5106/Desktop/research/vqa_accessibility/Dashboard-For-VQA/Dashboard Data/GT_N/video-1-segment-4.csv',
        org_f1=0.6,
        obj_list_all=object_list,
        limit_frame_count=-1
    )
    print(shadows)
