import os
import json
output_dir = './prob_desc'

for file in os.listdir(output_dir):
    if file.endswith(".json"):
        file_path = os.path.join(output_dir, file)

        data = json.load(open(file_path, 'r', encoding = 'utf-8'))

        if ('error' in data and data['error']):
            print('badid :', file)