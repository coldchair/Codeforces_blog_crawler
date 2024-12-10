import os

log_file_path = './logs/qwen_turbo_20k_filted_results.log'

names = ['dh', 'zhx', 'nhy']
radios = [0.5, 0.25, 0.25]

ids_all = []
with open(log_file_path, 'r') as f:
    for line in f.readlines():
        id, ok = line.strip().split(',')
        if (ok == '0'):
            ids_all.append(id)

# random shuffle
import random

random.seed(0)

ids_all = random.sample(ids_all, len(ids_all))
ids_all_length = len(ids_all)

for name, radio in zip(names, radios):
    length = int(ids_all_length * radio)
    ids = ids_all[:length]
    ids_all = ids_all[length:]
    ids = sorted(ids, key = lambda x: -int(x))

    output_file_path = f'tasks/tasks_{name}.txt'
    with open(output_file_path, 'w') as f:
        for id in ids:
            f.write(f'{id}\n')
