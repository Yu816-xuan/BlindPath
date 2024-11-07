import pandas as pd
import mysql.connector
from datetime import datetime

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
        'B_top': float(line[3]),
        'B_width': float(line[4]),
        'B_height': float(line[5]),
        'Class': line[6],
        'Conf': float(line[7]),
        'Ignore': int(line[8])
    }
    data_dicts.append(data_dict)

df = pd.DataFrame(data_dicts)

# 计算中心点坐标
df['center_x'] = df['B_left'] + df['B_width'] / 2
df['center_y'] = df['B_top'] + df['B_height'] / 2

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
# 假设 last_frames_obstacles 是包含障碍物信息的DataFrame

# 为障碍物添加额外信息
current_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 计算当前时间
obstacles_data = last_frames_obstacles[['Frame', 'ID', 'center_x', 'center_y', 'distance', 'rolling_mean_distance', 'rolling_std_distance', 'obstacle']]
obstacles_data['alarm_time'] = current_time  # 添加检测到障碍物的时间
obstacles_data['obstacle_type'] = obstacles_data['Class']  # 障碍物类型
obstacles_data['is_processed'] = 0  # 是否处理，这里设置为0
obstacles_data['monitor_id'] = 0  # 监控编号，这里设置为0
obstacles_data['notes'] = None  # 备注，这里设置为None

# 连接到MySQL数据库
conn = mysql.connector.connect(
    host="your_host",
    user="your_user",
    password="your_password",
    database="your_database"
)

# 插入数据到数据库
obstacles_data.to_sql('myapp_alarm', conn, if_exists='append', index=False)

# 提交事务
conn.commit()


# 关闭数据库连接
conn.close()