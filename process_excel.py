import os
import pandas as pd
from tqdm import tqdm
import json
import asyncio

xlsx_file_path = './excel/anno_12_16.xlsx'
csv_file_path = './excel/anno_12_16.csv'

# df = pd.read_excel(xlsx_file_path, header=None, engine='openpyxl')
df = pd.read_csv(csv_file_path, header=None, usecols=[0, 1, 2])


output_dir = './prob_desc'
os.makedirs(output_dir, exist_ok=True)

tot_id = 0
url2id = {}

badid = []

from prob.get_problem import get_problem_from_url

def add_url(url):
    global badid
    global tot_id
    if url not in url2id:
        url2id[url] = tot_id
        tot_id += 1
        result = {}
        try:
            result = asyncio.run(get_problem_from_url(url))
            if(result['error']):
                badid.append(url2id[url])
        except Exception as e:
            print(f"Error in {url}: {e}")
            badid.append(url2id[url])
            result['error'] = True
        
        result['url'] = url
        
        
        with open(os.path.join(output_dir, f'{url2id[url]}.json'), 'w', encoding = 'utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"Added {url} as {url2id[url]}.json")

    return url2id[url]

result = []
for index, row in tqdm(df.iterrows()):
    id0 = add_url(row[0])
    id1 = add_url(row[1])
    result.append({'id0': id0, 'id1': id1, 'label': row[2]})

with open(os.path.join(output_dir, 'labels.json'), 'w', encoding = 'utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

with open(os.path.join(output_dir, 'badid.json'), 'w') as f:
    json.dump(badid, f, indent=2)