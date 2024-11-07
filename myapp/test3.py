import json
import re


# 假设我们有一个包含多个帧的JSON文件
json_files = ["1.json","2.json","3.json","4.json","5.json"]  # 示例文件名，实际使用时请替换为实际文件名

# 读取所有帧的数据
all_frames = []
for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        all_frames.append(data)

def parse_tensor_string(s):
    # 使用正则表达式匹配字符串中的数字
    match = re.match(r'tensor\((\d+(?:\.\d+)?)\)', s)
    if match:
        # 将匹配到的数字部分转换为浮点数
        return float(match.group(1))
    return None

# 找到盲道的边界框
def find_blind_lane_bbox(frame):
    for detection in frame['detections']:
        if detection['class_name'] == 'blind_lane':
            # 解析bbox中的字符串为浮点数
            return [parse_tensor_string(detection['bbox'][0]), parse_tensor_string(detection['bbox'][1]),
                    parse_tensor_string(detection['bbox'][0]) + parse_tensor_string(detection['bbox'][2]),
                    parse_tensor_string(detection['bbox'][1]) + parse_tensor_string(detection['bbox'][3])]
    return None

# 定义检测两个边界框是否相交的函数
def is_intersect(blindbox1, bbox2):
    x_left = max(blindbox1[0], bbox2[0])
    y_top = max(blindbox1[1], bbox2[1])
    x_right = min(blindbox1[2], bbox2[2])
    y_bottom = min(blindbox1[3], bbox2[3])

    if x_right <= x_left or y_bottom <= y_top:
        return False  # 没有交集
    else:
        return True  # 有交集

# 筛选出与盲道坐标有交叉的物体，并按物体ID和类别组织数据
intersecting_objects = {}

for frame in all_frames:
    blind_lane_bbox = find_blind_lane_bbox(frame)
    for detection in frame['detections']:
        if detection['class_name'] != 'blind_lane':
            # 将bbox中的字符串转换为整数
            detection_bbox = [parse_tensor_string(detection['bbox'][0]), parse_tensor_string(detection['bbox'][1]),
                              parse_tensor_string(detection['bbox'][0]) + parse_tensor_string(detection['bbox'][2]),
                              parse_tensor_string(detection['bbox'][1]) + parse_tensor_string(detection['bbox'][3])]
            if blind_lane_bbox and is_intersect(blind_lane_bbox, detection_bbox):
                if detection['class_id'] not in intersecting_objects:
                    intersecting_objects[detection['class_id']] = {
                        'class': detection['class_name'],
                        'frames': []
                    }
                intersecting_objects[detection['class_id']]['frames'].append({
                    'frame_number': frame['frame_number'],
                    'bbox': detection_bbox,
                    'confidence': parse_tensor_string(detection['confidence'])  # 将置信度字符串转换为浮点数
                })

# 按照要求的格式输出到txt文件
with open('output.txt', 'w') as f:
    for class_id, obj_data in intersecting_objects.items():
        for frame_data in obj_data['frames']:
            f.write(f"{frame_data['frame_number']},{class_id},"
                    f"{frame_data['bbox'][0]},{frame_data['bbox'][1]},{frame_data['bbox'][2]},{frame_data['bbox'][3]},"
                    f"{obj_data['class']},"
                    f"{frame_data['confidence']},1\n")