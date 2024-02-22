import random
import numpy as np
from fractions import Fraction
import pandas as pd
from natsort import natsorted
if __name__ == '__main__':
    from get_prec_rec_f1 import calculate_model_ap_ar_af1 as get_f1
    from tqdm import tqdm
else:
    from .get_prec_rec_f1 import calculate_model_ap_ar_af1 as get_f1
import os


object_list = [
    "Accent Paving", "Barrier Post", "Barrier Stump", "Bench", "Bicycle", "Bridge",
    "Building", "Bus", "Bus Stop", "Car", "Chair", "Closed Sidewalk", "Counter",
    "Crosswalk", "Curb", "Dog", "Driveway(flat)", "Elevator", "Escalator", "Fence",
    "Fire hydrant", "Flush Door", "Foldout Sign", "Fountain", "Gate", "Guide dog",
    "Gutter", "Hose", "Lamp Post", "Mail box", "Maintenance Vehicle", "Motorcycle",
    "Parallel Parking Spot", "Paratransit vehicle", "Pedestrian Crossing", "Person",
    "Person with a disability", "Pillar", "Pole", "Puddle", "Push button", "Railing",
    "Raised Entryway", "Retaining Wall", "Road", "Road Divider", "Road Shoulder",
    "Roadside Parking", "Sidewalk", "Sidewalk pits", "Sign", "Sign Post", "Sloped Driveway",
    "Slopped Curb", "Snow", "Stairs", "Stop sign", "Street Vendor", "Table", "Tactile Paving",
    "Traffic Signals", "Train Platform", "Train Tracks", "Trash bins", "Trash on roads", "Tree",
    "Turnstile", "Uncontrolled Crossing", "Uneven Stairs", "Unpaved Road", "Unpaved Sidewalk",
    "Vegetation", "Wall", "Water leakage", "Water Pipes", "Wet surface", "Wheelchair",
    "White Cane", "Yard Waste"
]
object_list = [ooo.lower() for ooo in object_list]


def get_dum_pred_from_f1(gt_f__, mod_f__, gt_fol, gt_file, model_fol, obj_list_all, limit_frame_count=-1):
    obj_list_all = natsorted(obj_list_all)
    obj_dfs = []
    for obj in obj_list_all:
        random.seed(object_list.index(obj))
        obj_list_a = [obj]

        _, _, org_f1, _ = get_f1(
            gt_fol, gt_file,
            model_fol,
            obj_list=obj_list_a,
            limit_frame_count=limit_frame_count,
            avg_typ='micro'
        )

        dd_df = pd.read_csv(gt_f__)
        if limit_frame_count > 0:
            if len(list(dd_df.columns)) > limit_frame_count:
                dd_df = dd_df.iloc[:, :limit_frame_count]
        dd_df = dd_df.transpose()
        dd_df.columns = [x__.lower() for x__ in dd_df.iloc[0]]
        dd_df = dd_df.reindex(columns=obj_list_a).iloc[1:].transpose()
        dd_np = np.array(dd_df)

        md_df = pd.read_csv(mod_f__)
        if limit_frame_count > 0:
            if len(list(md_df.columns)) > limit_frame_count:
                md_df = md_df.iloc[:, :limit_frame_count]
        md_df = md_df.transpose()
        md_df.columns = [x__.lower() for x__ in md_df.iloc[0]]
        md_df = md_df.reindex(columns=obj_list_a).iloc[1:].transpose()
        md_df.columns = [cap_col.lower().replace('-', '_') for cap_col in md_df.columns]

        unique, counts = np.unique(np.array(dd_df), return_counts=True)
        total_pred_c = sum(counts)
        pred_counts = dict(zip(unique, counts))
        fra_rep = [int(x) for x in str(Fraction(org_f1).limit_denominator()).split('/')]

        if len(fra_rep) == 1:
            fra_rep = [1, 1]

        tp_frac = fra_rep[0] / 2
        fp_plus_fn_frac = fra_rep[1] - fra_rep[0]

        try:
            df_created = False
            for p_tp in range(pred_counts[1], 0, -1):
                df_created = False
                new_dd_np = np.zeros(dd_np.shape).astype(int)
                p_fp_plus_fn = round((fp_plus_fn_frac / tp_frac) * p_tp)
                p_fn = pred_counts[1] - p_tp
                p_fp = p_fp_plus_fn - p_fn
                p_tn = total_pred_c - (p_tp + p_fn + p_fp)
                p_f1 = (2 * p_tp) / (p_tp + p_tp + p_fp + p_fn)
                p_dev = abs((p_f1 - org_f1) / p_f1)

                if p_tn < 0 or p_dev > 0.008:
                    # print(obj, pred_counts, p_tn, p_dev)
                    continue

                pos_posit = np.argwhere(dd_np == 1)
                pos_neg = np.argwhere(dd_np == 0)
                p_rc_samp = random.sample(range(0, pos_posit.shape[0]), p_tp)

                try:
                    n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)
                except Exception as e:
                    # print(pos_neg.shape, p_fp)
                    if p_fp < 0:
                        p_fp = 0
                    n_rc_samp = random.sample(range(0, pos_neg.shape[0]), p_fp)

                tp_rrr, tp_ccc = pos_posit[:, 0][p_rc_samp], pos_posit[:, 1][p_rc_samp]
                fp_rrr, fp_ccc = pos_neg[:, 0][n_rc_samp], pos_neg[:, 1][n_rc_samp]

                new_dd_np[tp_rrr, tp_ccc] = 1
                new_dd_np[fp_rrr, fp_ccc] = 1

                new_dd_df = pd.DataFrame(new_dd_np, index=dd_df.index, columns=dd_df.columns)  # .reset_index()
                df_created = True
                # new_dd_df = new_dd_df.rename(columns={"index": "Object"})
                break

            if df_created:
                obj_dfs.append(new_dd_df)
                # print(f'success: {obj}')
            else:
                obj_dfs.append(md_df)
                # print(f'fail: {obj}')
        except:
            obj_dfs.append(md_df)
            # print(f'fail: {obj}')

    if len(obj_dfs) > 1:
        dum_pred_dfs = [pd.concat(obj_dfs).reset_index().rename(columns={"index": "Object"})]
    else:
        dum_pred_dfs = [obj_dfs[0].reset_index().rename(columns={"index": "Object"})]

    # print(dum_pred_dfs[0]['Object'])

    return dum_pred_dfs


if __name__ == '__main__':
    print("***************************")
    # object_list = [
    #     "Building", "Bus", "Bus Stop", "Car", "Motorcycle", "Person",
    #     "Person with a disability", "White Cane", "Yard Waste"
    # ]
    # object_list = [ooo.lower() for ooo in object_list]
    # shadows = get_dum_pred_from_f1(
    #     gt_f__='/Users/ibk5106/Desktop/research/vqa_accessibility/Dashboard-For-VQA/Dashboard Data/GT_N/video-1-segment-4.csv',
    #     org_f1=0.6,
    #     obj_list_all=object_list,
    #     limit_frame_count=-1
    # )
    # print(shadows)

    model_list = ['BLIP', 'GPV-1', 'GPT4V', 'LLaVa']
    dataset_dir = "../Dashboard Data/"
    gt_dir = os.path.join(dataset_dir, "GT_N")

    gts = natsorted(os.listdir(gt_dir))
    skip_list = [
        "video-10-segment-1.csv", "video-9-segment-2.csv"
    ]

    gts = [x.split('.')[0] for x in gts if
           x.endswith('.csv') and int(x.split('-')[1]) <= 16 and x not in skip_list]  # [:1]

    for model in tqdm(model_list):
        for gt in gts:
            shadow_df = get_dum_pred_from_f1(
                gt_f__=os.path.join(gt_dir, f'{gt}.csv'),
                mod_f__=os.path.join(dataset_dir, model, f'{gt}.csv'),
                gt_fol=gt_dir,
                gt_file=[f'{gt}.csv'],
                model_fol=os.path.join(dataset_dir, model),
                obj_list_all=object_list,
                limit_frame_count=17
            )[0]
            shadow_df.to_csv(os.path.join(dataset_dir, f'{model}@Shadow', f'{gt}.csv'), index=False)



