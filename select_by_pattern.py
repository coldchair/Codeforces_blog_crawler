import os
import json
from tqdm import tqdm
from logger import logger
from patterns import matchesPatterns

jsons_dir = './jsons'

# 列出所有文件
files = []
for file in os.listdir(jsons_dir):
    if file.endswith('.json'):
        files.append(file)

for file in tqdm(files):
    d = json.load(open(os.path.join(jsons_dir, file)))
    s1 = matchesPatterns(d['title'])
    s2 = matchesPatterns(d['content'])
    s3 = sum([matchesPatterns(comment['comment']) for comment in d['comments']])

    output = [file.split('.')[0], 'yes' if (s1 + s2 + s3 > 0) else 'no', s1, s2, s3]

    logger.info(','.join(map(str, output)))