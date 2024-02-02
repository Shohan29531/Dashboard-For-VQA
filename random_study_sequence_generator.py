import random
import os
from natsort import natsorted
from copy import deepcopy


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Dashboard Data')
EXPERIMENT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'experiments_new')
GROUND_TRUTH_DATA = os.path.join(DATA_DIR, 'GT')

files = os.listdir(GROUND_TRUTH_DATA)
all_video_files = [os.path.splitext(file)[0] for file in files if file.endswith(".csv")]
all_video_files = natsorted(all_video_files)

ignore_video = ['video-5', 'video-8', 'video-9']
ignore_video += ['video-'+str(i) for i in range(17, 25)]

ignore_vid_seg = []

trials = 24

for vid in all_video_files:
    for v in ignore_video:
        if v in vid:
            ignore_vid_seg.append(vid)
            break

for vid in ignore_vid_seg:
    del all_video_files[all_video_files.index(vid)]


for e_no in range(20):
    temp_vid_list = all_video_files + all_video_files
    print(temp_vid_list)
    csv_first_line = [
        'Model, Video, Status'
    ]

    csv_lines = []

    for x in range(trials):
        vid = random.choice(temp_vid_list)
        del temp_vid_list[temp_vid_list.index(vid)]
        model = f'Model-{x%8}'
        csv_lines.append(f'{model},{vid},')

    random.shuffle(csv_lines)

    csv_lines = csv_first_line + csv_lines

    with open(os.path.join(EXPERIMENT_DIR, f'experiment_{e_no+1}.csv'), 'w') as f:
        f.write("\n".join(csv_lines))



