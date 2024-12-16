import os
import shutil
import random

# 定义文件夹路径
txt_file_path = '/home/bingxing2/ailab/scx7kzd/denghan/Llama_test/out_log_all.txt'  # 输入的TXT文件路径
jsons_folder = 'jsons'  # 存储json文件的文件夹
output_folder = 'prompt_F_jsons'  # 新文件夹，用于存放复制的json文件

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取TXT文件并筛选出结果为1的ID
ids_with_result_1 = []

with open(txt_file_path, 'r', encoding='utf-8') as file:
    for line in file:
        parts = line.strip().split(',')  # 按逗号分隔
        id_part = parts[0].strip()  # 获取ID部分（如 "ID: 100074"）
        result_part = parts[1].strip()  # 获取结果部分（如 "结果: 1"）
        
        # 提取ID和结果
        id_value = id_part.split(':')[1].strip()
        result_value = int(result_part.split(':')[1].strip())
        
        # 只保留结果为1的ID
        if result_value == 1:
            ids_with_result_1.append(id_value)

# 随机抽取600个ID
random_ids = random.sample(ids_with_result_1, 600)

# 复制对应的JSON文件到新文件夹
for id_value in random_ids:
    json_file_path = os.path.join(jsons_folder, f'{id_value}.json')
    
    # 检查文件是否存在
    if os.path.exists(json_file_path):
        shutil.copy(json_file_path, os.path.join(output_folder, f'{id_value}.json'))
        print(f'Copied {id_value}.json to {output_folder}')
    else:
        print(f'Warning: {id_value}.json not found in {jsons_folder}')
