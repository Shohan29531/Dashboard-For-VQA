import pandas as pd

# Load the combined CSV
df = pd.read_csv('../Logs/trimmed_logs/all.csv')

# Specify the directory
dir = 'E:\\Projects\\Dashboard-For-VQA\\Dashboard Data - New\\GT_N\\'

# Initialize a list to hold the number of columns (frames) for each video
frames_count = []

# Iterate through each row in the DataFrame
for video in df['video']:
    # Construct the file path for the current video's CSV
    file_path = f"{dir}{video}.csv"
    video_df = pd.read_csv(file_path)
    frames_count.append(video_df.shape[1] - 1 if video_df.shape[1] <=17 else 16)


df['frames'] = frames_count

df.to_csv('../Logs/trimmed_logs/all_latest.csv', index=False)
