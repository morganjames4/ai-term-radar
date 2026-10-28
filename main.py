import requests
import time
from collections import Counter
from bs4 import BeautifulSoup

def fetch_github_trending(url='https://github.com/trending?spoken_language_code=en'):
    headers = {'User-Agent': 'Mozilla/5.0'}
    resp = requests.get(url, headers=headers, timeout=10)
    if resp.status_code != 200:
        print(f'Error: {resp.status_code}')
        return []
    soup = BeautifulSoup(resp.text, 'html.parser')
    repos = []
    for article in soup.select('article.Box-row'):
        name = article.h2.a.get_text(strip=True).replace(' /', ':')
        desc = article.p.get_text(strip=True) if article.p else ''
        lang = article.find('span', itemprop='programmingLanguage')
        lang = lang.get_text(strip=True) if lang else 'unknown'
        repos.append({'name': name, 'desc': desc, 'lang': lang})
    return repos

def extract_ai_terms(repos, n=10):
    keywords = ['ai', 'llm', 'agent', 'model', 'gpt', 'claude', 'rag', 'pipeline', 'inference', 'embedding']
    counter = Counter()
    for repo in repos:
        text = (repo['name'] + ' ' + repo['desc']).lower()
        for kw in keywords:
            if kw in text:
                counter[kw] += 1
    return [word for word, _ in counter.most_common(n)]

def main():
    repos = fetch_github_trending()
    terms = extract_ai_terms(repos)
    data = {'date': time.strftime('%Y-%m-%d'), 'top_terms': terms, 'repo_count': len(repos)}
    print(__import__('json').dumps(data, indent=2))

if __name__ == '__main__':
    main()
