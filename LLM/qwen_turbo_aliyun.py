import os
from openai import OpenAI

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # api key 找 denghan 要
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

def get_output(prompt):
    completion = client.chat.completions.create(
        model="qwen-turbo", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content':  prompt}],
        )
    # print(completion.choices[0].message.content)
    # print(completion.model_dump_json()['choices'][0]['message'['content']])
    return completion.choices[0].message.content