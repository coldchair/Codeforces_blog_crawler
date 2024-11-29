import os
import json
from tqdm import tqdm
import asyncio
from crawl4ai import AsyncWebCrawler
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy
from tqdm.asyncio import tqdm_asyncio


async def extract_news_teasers(blog_id = 136396, verbose = False):
    schema = {
        "name": "Codeforces Blog Post",
        "baseSelector": "div#body",
        "fields": [
            {
                "name": "title",
                "selector": "div.title",
                "type": "text",
            },
            {
                'name' : 'content',
                'selector': 'div.content',
                'type' : 'text',
            },
            {
                'name' : 'comments',
                'selector': 'div.comments>div.comment',
                'type' : 'list',
                "fields" : [
                    {
                        'name' : 'comment',
                        'type' : 'text',
                    }
                ]
            },
        ],
    }

    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=verbose)

    async with AsyncWebCrawler(verbose=True) as crawler:
        result = await crawler.arun(
            url=f"https://codeforces.com/blog/entry/{blog_id}",
            extraction_strategy=extraction_strategy,
            bypass_cache=True,
            exclude_external_images=True,   # Remove external images
            verbose=verbose
        )
        if (not result.success):
            return None
        news_teasers = json.loads(result.extracted_content)
        if (len(news_teasers) == 0):
            return None
        return news_teasers[0]

from patterns import count_words
def count_blog_words(d):
    s1 = count_words(d['title'])
    s2 = count_words(d['content'])
    s3 = sum([count_words(comment['comment']) for comment in d['comments']])
    return s1, s2, s3

async def process_blog(blog_id, save_dir, lock):
    if (blog_id > 140000):
        return False

    d = await extract_news_teasers(blog_id)
    if d is None: # fail to crawl
        async with lock:
            logger.info(','.join([str(blog_id), 'fail', '0', '0', '0']))
        return False
    s1, s2, s3 = count_blog_words(d)
    yes = (s1 + s2 + s3) > 0
    async with lock:
        logger.info(','.join([str(blog_id), 'yes' if yes else 'no', str(s1), str(s2), str(s3)]))
    if yes:
        json.dump(d, open(os.path.join(save_dir, f'{blog_id}.json'), 'w'))

    return True

def get_fail_id_from_log(log_file):
    with open(log_file) as f:
        lines = f.readlines()
    fail_ids = []
    for line in lines:
        if 'fail' in line:
            fail_ids.append(int(line.split(',')[0]))
    return fail_ids

MAX_TASKS = 4
MAX_FAIL_RETRY = 3

from logger import logger

# retry the previously failed task.
async def retry_fail_task(fail_task_id_list, fail_task_retry_count):
    print(f"Retrying {len(fail_task_id_list)} failed tasks ...")
    this_success_id_list = []
    new_fail_task_id_list = []
    new_fail_task_retry_count = []

    taskid2idx = {taskid: idx for idx, taskid in enumerate(fail_task_id_list)}
    retry_success_id_list = await main(fail_task_id_list, retry = False)
    retry_results = [False] * len(fail_task_id_list)
    for taskid in retry_success_id_list:
        idx = taskid2idx[taskid]
        retry_results[idx] = True
    for idx, result in enumerate(retry_results):
        if (result):
            this_success_id_list.append(fail_task_id_list[idx])
        else:
            if (fail_task_retry_count[idx] < MAX_FAIL_RETRY):
                new_fail_task_id_list.append(fail_task_id_list[idx])
                new_fail_task_retry_count.append(fail_task_retry_count[idx] + 1)

    fail_task_id_list = new_fail_task_id_list
    fail_task_retry_count = new_fail_task_retry_count

    print(f"Retried {len(this_success_id_list)} / {len(fail_task_id_list)} tasks successfully")
    return this_success_id_list, fail_task_id_list, fail_task_retry_count

async def main(id_list, retry = True) -> list:
    taskid2idx = {taskid: idx for idx, taskid in enumerate(id_list)}
    success_task_id_list = []
    
    fail_task_id_list = []
    fail_task_retry_count = []

    lock = asyncio.Lock()
    tasks = []

    for i, x in tqdm(enumerate(id_list), desc = f'retry : {retry}', total = len(id_list)):
        tasks.append(process_blog(x, save_dir, lock))
        if len(tasks) == MAX_TASKS:
            results = await asyncio.gather(*tasks)
            tasks = []
            for idx, result in enumerate(results):
                taskid = id_list[i - (len(results) - 1) + idx]
                if (not result):
                    fail_task_id_list.append(taskid)
                    fail_task_retry_count.append(0)
                else:
                    success_task_id_list.append(taskid)
                    
            if (fail_task_id_list and any(results) and retry):
                retry_success_id_list, fail_task_id_list, fail_task_retry_count = await retry_fail_task(fail_task_id_list, fail_task_retry_count)
                success_task_id_list.extend(retry_success_id_list)
                        
    if tasks:
        results = await asyncio.gather(*tasks)
        for idx, result in enumerate(results):
            taskid = id_list[(len(id_list) - 1) - (len(results) - 1) + idx]
            if (not result):
                fail_task_id_list.append(taskid)
                fail_task_retry_count.append(0)
            else:
                success_task_id_list.append(taskid)
        while(fail_task_id_list and retry):
            # wait for 2 minutes before retrying the failed
            await asyncio.sleep(1)
            retry_success_id_list, fail_task_id_list, fail_task_retry_count = await retry_fail_task(fail_task_id_list, fail_task_retry_count)
            success_task_id_list.extend(retry_success_id_list)
    
    return success_task_id_list
        

if __name__ == "__main__":
    start_blog_id = 1
    end_blog_id = 136396
    id_list = range(end_blog_id, start_blog_id - 1, -1) # try all tasks in reverse order

    # log_file = './logs/essential_words_all.logg'
    # id_list = get_fail_id_from_log(log_file) # retry failed tasks

    save_dir = './jsons'
    os.makedirs(save_dir, exist_ok=True)

    asyncio.run(main(id_list))
