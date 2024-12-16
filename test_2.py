import asyncio
from crawl4ai import AsyncWebCrawler, CacheMode

import os, sys
from pathlib import Path
import asyncio, time
from crawl4ai import AsyncWebCrawler

async def crawl_with_advanced_config(url: str = ""):
    async with AsyncWebCrawler(
        # Browser setup
        browser_type="chromium",
        headless=True,
        verbose=True,

        # # Identity
        user_agent="Custom User Agent",
        headers={"Accept-Language": "en-US"},

        # Proxy setup
        # proxy="http://proxy.example.com:8080"
    ) as crawler:
        url = "https://codeforces.com/problemset/problem/1/A"
        url = 'https://www.luogu.com.cn/problem/P2512'
        url = 'https://cses.fi/problemset/task/2132/'
        url = 'https://www.codechef.com/problems/FARMLEGS?'
        url = 'https://loj.ac/p/6187'
        url = 'https://www.codechef.com/problems/EQUAL2'
        url = 'https://leetcode.com/problems/count-visited-nodes-in-a-directed-graph/description/'
        url = 'https://www.geeksforgeeks.org/count-of-distinct-differences-between-two-maximum-elements-of-every-subarray/'
        url = 'https://codeforces.com/gym/105039/problem/G2'

        result = await crawler.arun(
            url=url,
            # Content handling
            process_iframes=True,
            screenshot=True,

            # # Timing
            # page_timeout=60000,
            delay_before_return_html=5.0,

            # # Anti-detection
            magic=True,
            simulate_user=True,

            # # Dynamic content
            # js_code=[
            #     "window.scrollTo(0, document.body.scrollHeight);",
            #     "document.querySelector('.load-more')?.click();"
            # ],
            # wait_for="css:.dynamic-content"
        )
        
        print(f"Successfully crawled {url}")
        print(f"Content length: {len(result.markdown)}")
        print(result.markdown)
        # print(result.cleaned_html)



if __name__ == "__main__":
    asyncio.run(crawl_with_advanced_config())