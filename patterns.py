import re
import nltk
from nltk.tokenize import sent_tokenize

essential_words = [
    'similar', 'same', 'copied',
    'coincidence', 'conflict', 'collision',
]

# 定义正则表达式模式
detect_patterns = [
    re.compile(r'(similar.*problem|problem.*similar)', re.IGNORECASE),
    re.compile(r'(same.*problem|problem.*same)', re.IGNORECASE),
    re.compile(r'(copied.*problem|problem.*copied)', re.IGNORECASE),

    re.compile(r'(similar.*idea|idea.*similar)', re.IGNORECASE),
    re.compile(r'(same.*idea|idea.*same)', re.IGNORECASE),
    re.compile(r'(copied.*idea|idea.*copied)', re.IGNORECASE),

    re.compile(r'coincidence', re.IGNORECASE),
    re.compile(r'conflict', re.IGNORECASE),
    re.compile(r'collision', re.IGNORECASE),
]

def count_words(passage):
    passage = passage.lower()
    return sum(passage.count(word) for word in essential_words)

# 下载 punkt 数据包（如果尚未下载）
nltk.download('punkt_tab')

def matchesPatterns(article):
    sentences = sent_tokenize(article)
    cnt = 0
    for sentence in sentences:
        for pattern in detect_patterns:
            if pattern.search(sentence):
                cnt += 1
    return cnt

if __name__ == '__main__':
    print(count_words('These are similar problems.'))

    # 示例文章
    article = """
    This is a sample text. It contains several sentences. Some sentences might have similar problems. 
    Other sentences might talk about the same idea. There could be a coincidence or a conflict.
    """

    print(matchesPatterns(article))
