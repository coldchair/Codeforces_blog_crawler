# Codeforces blog 爬虫


logs/essential_words_all.log 中记录用关键词筛选的结果，大约还剩 2w 个。

logs/pattern_filted_all.log 记录了进一步用正则表达式进行筛选的结果，大约还剩下 1w 个。

fail 表示爬取失败，yes 表示通过筛选，no 表示没有通过筛选，后面三个数字分别表示 title, content, comments 通过筛选的次数。

第一步关键词筛选后的所有 blog 见：
https://cloud.tsinghua.edu.cn/f/5798f243ff9e4c7298cf/

想要运行爬虫请 pip install -r requirements.txt

然后运行 main.py 

## LLM 模型筛选：
