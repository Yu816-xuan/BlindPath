import pandas as pd

# 读取文件
with open('output.txt', 'r') as file:
    data = file.readlines()

# 解析数据
data_dicts = []
for line in data:
    # 移除换行符并分割
    line = line.strip().split(',')
    # 将分割后的列表转换为字典
    data_dict = {
        'Frame': int(line[0]),
        'ID': int(line[1]),
        'BB_left': float(line[2]),
        'BB_top': float(line[3]),
        'BB_width': float(line[4]),
        'BB_height': float(line[5]),
        'Class': line[6],
        'Conf': float(line[7]),
        'Ignore': int(line[8])
    }
    data_dicts.append(data_dict)

df = pd.DataFrame(data_dicts)

# 计算中心点坐标
df['center_x'] = df['BB_left'] + df['BB_width'] / 2
df['center_y'] = df['BB_top'] + df['BB_height'] / 2

# 创建滞后特征
df['center_x_lag_1'] = df['center_x'].shift(1)
df['center_y_lag_1'] = df['center_y'].shift(1)

# 计算移动距离
df['delta_x'] = df['center_x'] - df['center_x_lag_1']
df['delta_y'] = df['center_y'] - df['center_y_lag_1']
df['distance'] = (df['delta_x']**2 + df['delta_y']**2)**0.5

# 计算滑动窗口统计
df['rolling_mean_distance'] = df['distance'].rolling(window=4).mean()
df['rolling_std_distance'] = df['distance'].rolling(window=4).std()

# 识别障碍物（这里使用简单的阈值，您可以根据需要调整）
threshold = 0
df['obstacle'] = df['rolling_mean_distance'] == threshold

# 分组选择每个物体的最后一帧，并检查是否为障碍物
last_frames_obstacles = df.groupby('ID').tail(1).reset_index(drop=True)
last_frames_obstacles = last_frames_obstacles[last_frames_obstacles['obstacle']]

print(last_frames_obstacles[['Frame', 'ID', 'center_x', 'center_y', 'distance', 'rolling_mean_distance', 'rolling_std_distance', 'obstacle']])