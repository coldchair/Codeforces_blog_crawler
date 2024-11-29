# This file is used to merge multiple log files into one file.
import pandas as pd
from tqdm import tqdm

log_file_paths = [
    'logs/my_log_20241129_115029.log',
    'logs/my_log_20241129_120438.log',
]

d = {}

for file_path in log_file_paths:
    df = pd.read_csv(file_path, sep=',', header=None)

    # enum each row
    for index, row in tqdm(df.iterrows(), desc = f'{file_path} ing...'):
        x = row[0]
        if (not x in d):
            d[x] = list(row)
        else:
            if (row[1] != 'fail'):
                d[x] = list(row)

from logger import logger
keys = list(d.keys())
keys = sorted(keys, key = lambda x: -int(x))
for k in tqdm(keys, desc = 'logging...'):
    logger.info(','.join(map(str, d[k])))
        

