import os
import requests
import asyncio
from prob.get_problem import get_problem_from_url
import json
from tqdm import tqdm
cf_api_url = 'https://codeforces.com/api/problemset.problems?tags=implementation'

content = requests.get(cf_api_url).json()

print(content.keys())
print(content['result']['problems'])

output_dir = './prob_desc_cf'

os.makedirs(output_dir, exist_ok=True)

n = 2000

prob_list = content['result']['problems']
# 把 prob_list 随机打乱
import random
random.seed(0)
random.shuffle(prob_list)

tot_id = 0

for p in tqdm(prob_list[:n]):
    print(p)
    url = f"https://codeforces.com/contest/{p['contestId']}/problem/{p['index']}"

    result = {}
    try:
        result = asyncio.run(get_problem_from_url(url))
        if(result['error']):
            continue
    except Exception as e:
        continue
    result['url'] = url
    with open(os.path.join(output_dir, f'{tot_id}.json'), 'w', encoding = 'utf-8') as f:
        json.dump(result, f, indent=2, ensure_ascii=False)
    tot_id += 1