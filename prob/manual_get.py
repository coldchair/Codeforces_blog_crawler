from openai import OpenAI
import os

id = 219
url = 'https://www.codechef.com/CRK32020/problems/KEVIN'

problem = '''
Sure, here is the content converted into Markdown format:
# Kevin and Array
## Problem Statement
Kevin has an array `a` consisting of `n` elements. He defines an operation `f` as maximum of absolute difference between the adjacent elements of the array. If 0 <= n <= 1 then f is 0. He wants to minimize the value of `f` for the array `a`. For this, he is allowed to replace at most `k` elements of the array with any integer. Help Kevin to find the minimum value of `f` for the array.
## Input:
First line consists of two space separated integers `n` and `k`.
Second line contains `n` space separated integers of the array `a_1, a_2, ..., a_n`.
## Output:
Print minimum value of `f` for the array.
## Constraints:
1 ≤ k ≤ n ≤ 2000  
-10^9 ≤ a_i ≤ 10^9 (where a_i refers to the element of the array).
## Sample input:
5 2
4 7 4 4 4
## Sample output:
0
## Explanation:
In the first sample Kevin can change the second and fourth elements and get array: 4, 4, 4, 4, 4.
In the third sample he can get array: 1, 2, 3, 4, 5, 6
Accepted
4
Submissions
39
Accuracy
10.26
This markdown will render the text in a structured way suitable for documentation or sharing on platforms that support markdown formatting.
'''

str0 = f'''
Here is the content from the URL:
<url>{url}</url>

<url_content>
'''

str1 = '''
</url_content>

The user has made the following request for what information to extract from the above content:

<user_request>
From the crawled content, extract all parts of the problem, including title, description, input, output, examples, note, tags
                Do not miss any models in the entire content. One extracted model JSON format should look like this: 
                {'title' : 'A. Theatre Square',
                'description' : 'Theatre Square in the capital city of Berland has a rectangular shape with the size $n$ ×  $m$ meters.
                On the occasion of the city's anniversary, a decision was taken to pave the Square with square granite flagstones. Each flagstone is of the size $a$ × $a$.
                What is the least number of flagstones needed to pave the Square? It's allowed to cover the surface larger than the Theatre Square, but the Square has to be covered.
                It's not allowed to break the flagstones.
                The sides of flagstones should be parallel to the sides of the Square.',
                'input' : 'The input contains three positive integer numbers in the first line: $n$, $m$ and $a$ (1 ≤  $n$ ,  $m$ ,  $a$ ≤ 10^9).',
                'output' : 'Write the needed number of flagstones.',
                'examples' : '
                Input
                ```
                6 6 4
                ```
                Output
                ```
                4
                ```',
                'notes' : 'Example',
                'tags' : 'math, *1000'}.
                If the problem have 'Constraints', please include them in the 'Input' section.
                Please ensure that the mathematical formula is in LaTeX or markdown format. 
                If some sections are missing, please set them to None.
                
</user_request>

<schema_block>
{
  "properties": {
    "title": {
      "description": "Title of the problem.",
      "title": "Title",
      "type": "string"
    },
    "description": {
      "description": "Description of the problem.",
      "title": "Description",
      "type": "string"
    },
    "input": {
      "description": "Input of the problem.",
      "title": "Input",
      "type": "string"
    },
    "output": {
      "description": "Output of the problem.",
      "title": "Output",
      "type": "string"
    },
    "examples": {
      "description": "Examples of the problem.",
      "title": "Examples",
      "type": "string"
    },
    "notes": {
      "description": "Notes of the problem.",
      "title": "Notes",
      "type": "string"
    },
    "tags": {
      "description": "Tags of the problem.",
      "title": "Tags",
      "type": "string"
    }
  },
  "required": [
    "title",
    "description",
    "input",
    "output",
    "examples",
    "notes",
    "tags"
  ],
  "title": "CodeforcesProblemDescription",
  "type": "object"
}
</schema_block>

Please carefully read the URL content and the user's request. If the user provided a desired JSON schema in the <schema_block> above, extract the requested information from the URL content according to that schema. If no schema was provided, infer an appropriate JSON schema based on the user's request that will best capture the key information they are looking for.

Extraction instructions:
Return the extracted information as a list of JSON objects, with each object in the list corresponding to a block of content from the URL, in the same order as it appears on the page. Wrap the entire JSON list in <blocks>...</blocks> XML tags.

Quality Reflection:
Before outputting your final answer, double check that the JSON you are returning is complete, containing all the information requested by the user, and is valid JSON that could be parsed by json.loads() with no errors or omissions. The outputted JSON objects should fully match the schema, either provided or inferred.

Quality Score:
After reflecting, score the quality and completeness of the JSON data you are about to return on a scale of 1 to 5. Write the score inside <score> tags.

Avoid Common Mistakes:
- Do NOT add any comments using "//" or "#" in the JSON output. It causes parsing errors.
- Make sure the JSON is properly formatted with curly braces, square brackets, and commas in the right places.
- Do not miss closing </blocks> tag at the end of the JSON output.
- Do not generate the Python coee show me how to do the task, this is your task to extract the information and return it in JSON format.

Result
Output the final list of JSON objects, wrapped in <blocks>...</blocks> XML tags. Make sure to close the tag properly.
'''



client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # api key 找 denghan 要
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

prompt_with_variables = str0 + problem + str1

response = client.chat.completions.create(
    model="qwen-turbo", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
    messages=[
        {'role': 'system', 'content': 'You are a helpful assistant.'},
        {'role': 'user', 'content': prompt_with_variables}],
)

content = response.choices[0].message.content
# 提取 <blocks> 中的内容
content = content[content.find('<blocks>') + len('<blocks>'):content.find('</blocks>')]
# print(content)
# 转 json
import json
content = json.loads(content)
content = content[0]
content['error'] = False
content['url'] = url

print(content)

if (content['error']):
    print("Error in extracting content")
    exit(1)

with open(f'./prob_desc/{id}.json', 'w', encoding = 'utf-8') as f:
    json.dump(content, f, indent=2, ensure_ascii=False)