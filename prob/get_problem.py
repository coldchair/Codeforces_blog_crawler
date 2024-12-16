import os
# os.environ['OPENAI_BASE_URL'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from pydantic import BaseModel, Field

class OpenAIModelFee(BaseModel):
    model_name: str = Field(..., description="Name of the OpenAI model.")
    input_fee: str = Field(..., description="Fee for input token for the OpenAI model.")
    output_fee: str = Field(..., description="Fee for output token for the OpenAI model.")

class CodeforcesProblemDescription(BaseModel):
    title: str = Field(..., description="Title of the problem.")
    description: str = Field(..., description="Description of the problem.")
    input: str = Field(..., description="Input of the problem.")
    output: str = Field(..., description="Output of the problem.")
    examples: str = Field(..., description="Examples of the problem.")
    notes: str = Field(..., description="Notes of the problem.")
    tags: str = Field(..., description="Tags of the problem.")


from crawl4ai.extraction_strategy import ExtractionStrategy
from abc import ABC, abstractmethod
from typing import Any, List, Dict, Optional, Union
from crawl4ai.config import *
from crawl4ai.utils import *
from crawl4ai.prompts import *
from openai import OpenAI

# aliyun API
client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # api key 找 denghan 要
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

class LLMExtractionStrategy_v2(LLMExtractionStrategy):
    def extract(self, url: str, ix:int, html: str) -> List[Dict[str, Any]]:
        # print("[LOG] Extracting blocks from URL:", url)
        print(f"[LOG] Call LLM for {url} - block index: {ix}")
        variable_values = {
            "URL": url,
            "HTML": escape_json_string(sanitize_html(html)),
        }
        
        prompt_with_variables = PROMPT_EXTRACT_BLOCKS
        if self.instruction:
            variable_values["REQUEST"] = self.instruction
            prompt_with_variables = PROMPT_EXTRACT_BLOCKS_WITH_INSTRUCTION
            
        if self.extract_type == "schema" and self.schema:
            variable_values["SCHEMA"] = json.dumps(self.schema, indent=2)
            prompt_with_variables = PROMPT_EXTRACT_SCHEMA_WITH_INSTRUCTION

        for variable in variable_values:
            prompt_with_variables = prompt_with_variables.replace(
                "{" + variable + "}", variable_values[variable]
            )
        
        # response = perform_completion_with_backoff(
        #     self.provider, 
        #     prompt_with_variables, 
        #     self.api_token, 
        #     base_url=self.api_base or self.base_url,
        #     extra_args = self.extra_args
        #     ) # , json_response=self.extract_type == "schema")

        # print(prompt_with_variables)

        response = client.chat.completions.create(
            model="qwen-turbo", # 模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
            messages=[
                {'role': 'system', 'content': 'You are a helpful assistant.'},
                {'role': 'user', 'content': prompt_with_variables}],
        )

        try:
            blocks = extract_xml_data(["blocks"], response.choices[0].message.content)['blocks']
            blocks = json.loads(blocks)
            for block in blocks:
                block['error'] = False
        except Exception as e:
            parsed, unparsed = split_and_parse_json_objects(response.choices[0].message.content)
            blocks = parsed
            if unparsed:
                blocks.append({
                    "index": 0,
                    "error": True,
                    "tags": ["error"],
                    "content": unparsed
                })
        
        if self.verbose:
            print("[LOG] Extracted", len(blocks), "blocks from URL:", url, "block index:", ix)
        return blocks
    
async def get_problem_from_url(url):
    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=url,
            delay_before_return_html=2.0, # 对于 Luogu 和 Codechef 是必要的
            word_count_threshold=1,
            extraction_strategy=LLMExtractionStrategy_v2(
                # Here you can use any provider that Litellm library supports, for instance: ollama/qwen2
                # provider="ollama/qwen2", api_token="no-token", 
                provider="qwen-turbo",
                api_token=os.getenv("DASHSCOPE_API_KEY"), 
                schema=CodeforcesProblemDescription.schema(),
                extraction_type="schema",
                instruction="""From the crawled content, extract all parts of the problem, including title, description, input, output, examples, note, tags
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
                """
            ),            
            cache_mode=CacheMode.BYPASS,
        )
        # print(result.extracted_content)
        json_result = json.loads(result.extracted_content)[0]
        if (json_result['description'] == None or json_result['examples'] == None):
            json_result['error'] = True
        return json_result

if __name__ == "__main__":
        url = 'https://codeforces.com/problemset/problem/2039/B'
        url = 'https://cses.fi/problemset/task/2132/'
        url = 'https://atcoder.jp/contests/abc250/tasks/abc250_g'
        url = 'https://codeforces.com/gym/101471/problem/A'
        url = 'https://www.codechef.com/problems/FARMLEGS?'
        result = asyncio.run(get_problem_from_url(url))
        print(type(result))
        print(result)