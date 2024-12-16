import os
import shutil
import csv

# 定义文件夹路径
csv_file_path = '/home/bingxing2/ailab/scx7kzd/denghan/Codeforces_blog_crawler/excel/anno_12_16.csv'  # 输入的CSV文件路径
jsons_folder = 'prompt_jsons'  # 存储json文件的文件夹
output_folder = 'jsons'  # 新文件夹，用于存放提取的json文件

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 读取CSV文件中的编号，并处理相应的JSON文件
with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    
    # 跳过标题行
    next(reader)
    
    for row in reader:
        # 假设编号在第一个列（index 0）
        problem_id = row[4]  
        
        # 构造对应的json文件路径
        json_file_path = os.path.join(jsons_folder, f'{problem_id}.json')
        
        # 检查文件是否存在，如果存在则移动到新文件夹
        if os.path.exists(json_file_path):
            shutil.copy(json_file_path, os.path.join(output_folder, f'{problem_id}.json'))
            print(f'Moved {problem_id}.json to {output_folder}')
        else:
            print(f'Warning: {problem_id}.json not found in {jsons_folder}')
