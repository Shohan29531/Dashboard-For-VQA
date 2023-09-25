import pandas as pd
import random


def get_obj_list(src, e_obj=5, non_e_obj=5, total_obj=10, all_random=False):
    df_obj = pd.read_csv(src)
    # print(df_obj)
    obj_exist = []
    obj_not_exists = []

    for index, row in df_obj.iterrows():
        obj = list(row)[0]
        if 1 in list(row)[1:]:
            obj_exist.append(obj)
        else:
            obj_not_exists.append(obj)

    out_obj = []

    all_obj = obj_exist + obj_not_exists
    if all_random:
        out_obj = random.sample(all_obj, total_obj)
        return out_obj

    if len(obj_exist) <= e_obj:
        out_obj = out_obj + obj_exist
        rem_obj = e_obj + non_e_obj - len(out_obj)
        out_obj = out_obj + random.sample(obj_not_exists, rem_obj)
    elif len(obj_not_exists) <= non_e_obj:
        out_obj = out_obj + obj_not_exists
        rem_obj = e_obj + non_e_obj - len(out_obj)
        out_obj = out_obj + random.sample(obj_exist, rem_obj)
    else:
        out_obj = out_obj + random.sample(obj_exist, e_obj)
        out_obj = out_obj + random.sample(obj_not_exists, non_e_obj)

    return out_obj


if __name__ == '__main__':
    gt_path = '/Users/imrankabir/Desktop/research/vqa_accessibility/Dashboard-For-VQA/Dashboard Data/GT/video-1-segment-4.csv'
    obj_sel = get_obj_list(gt_path, e_obj=7, non_e_obj=9)
    print(obj_sel, len(obj_sel))