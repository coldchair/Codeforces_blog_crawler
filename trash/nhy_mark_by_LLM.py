# -*- coding: utf-8 -*-
import os
os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'

import json
from tqdm import tqdm
import torch
import warnings
from utils.logger import logger

# 修改为镜像源
warnings.filterwarnings("ignore", message="Setting `pad_token_id` to `eos_token_id`")

jsons_dir = './jsons'

ids_all = []


# TODO: modify the following path （改成你自己的名字的 tasks）
log_file_path = './tasks/tasks_nhy.txt'
with open(log_file_path, 'r') as f:
    for line in f.readlines():
        id = line.strip()
        ids_all.append(id)

ids = ids_all
ids = sorted(ids, key=lambda x: -int(x))

# TODO: modify the range of ids（更改范围来帮助标注，你也可以设为全部一次跑完）
# ids = ids_all
# ids = ['118883', '105221', '126513', '131958'] 

from LLM.qwen_turbo_aliyun import get_output # applying API from aliyun
from transformers import AutoTokenizer
model_name = "Qwen/Qwen2.5-14B-Instruct" # Chinese
tokenizer = AutoTokenizer.from_pretrained(model_name)

# 设置最大输入长度
MAX_LENGTH = 1000000  # qwen-turbo-latest

def chunk_text(text, max_length=MAX_LENGTH):
    """将文本切割为多个片段，每个片段的token数不超过max_length"""
    # 对文本进行分词
    tokens = tokenizer.encode(text, truncation=False)
    chunks = []
    
    for i in range(0, len(tokens), max_length):
        chunk = tokens[i:i + max_length]
        chunks.append(tokenizer.decode(chunk))
    
    return chunks

for id in tqdm(ids):
    torch.cuda.empty_cache()
    d = json.load(open(f'{jsons_dir}/{id}.json'))
    content = d['content']
    comments = d['comments']
    comments = [f'comment#{i}' + c['comment'] for i, c in enumerate(comments) ]
    content = content + ' '.join(comments)

    # 判断文本长度，如果超过 MAX_LENGTH，则进行切割
    if len(tokenizer.encode(content)) > MAX_LENGTH:
        chunks = chunk_text(content)
    else:
        chunks = [content]

    for chunk in chunks:
        content = f'''请判断下面这篇博客或者博客的评论区是否讨论了两道编程题目之间有相同或相似的关系。
        '相同'是指题目在内容、解法等方面几乎一致；'相似'是指题目在内容、解法等方面相近。
        如果十分坚定地判断出有相同、相似的关系，请只回答'0'，否则，请只回答'1'。请注意，不需要解释原因，
        只回答'0'或'1'。\n 
        Blog: \n
        {chunk}'''

        content = f'''
        请判断下面这篇博客或者博客的评论区是否包含了两道不同的编程题目出现了雷同或冲突或撞题的信息 \n
        注意不是同一道题目的两份代码出现了雷同，而是两道题目是本质相同的或者相似的。 \n
        （可能有用的关键词：coincidence, conflict, similar problem, same problem）。\n
        如果出现了这样的信息，请只回答 '0'，否则，请只回答 '1'。请注意，不需要解释原因，只回答 '0' 或 '1'。\n
        Blog: \n
        {chunk}
        '''

        # TODO: 可以更改下面的 prompt
        content = f'''
        请判断下面这篇博客或者博客的评论区是否包含了两道不同的编程题目出现了雷同或冲突或撞题的信息 \n
        注意不是同一道题目的两份代码出现了雷同，而是两道题目是本质相同的或者相似的。 \n
        （可能有用的关键词：coincidence, conflict, similar problem, same problem）。\n
        如果出现了这样的信息，请指出在博客的什么地方，并指出两个题目（来源，链接）。
        Blog: \n
        {chunk}
        '''

        try:
            # 获取模型输出
            result = get_output(content)
            # print(f'id = {id} result  = {result}')
        except:
            result = '2' # error

        # logging
        logger.info(f'{id},{result}')