import requests
from bs4 import BeautifulSoup
from datetime import datetime

SOURCES = [
    {
        'name': 'innovaTopia',
        'url': 'https://innovatopia.jp/ai/ai-news/',
        'base': 'https://innovatopia.jp',
    }
]

def scrape_innovatopia(url, base):
    res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.text, 'html.parser')
    articles = []

    for tag in soup.find_all(['h2', 'h3']):
        a = tag.find('a', href=True)
        if not a or 'innovatopia.jp' not in a['href']:
            continue

        title = a.get_text(strip=True)
        link  = a['href']

        # サムネイル
        img_tag = tag.find_previous('img') or tag.find_next('img')
        thumb = img_tag['src'] if img_tag and img_tag.get('src') else ''

        # 日付
        parent = tag.parent
        date_text = ''
        for text in parent.stripped_strings:
            if '年' in text and '月' in text:
                date_text = text
                break

        if title and link:
            articles.append({
                'title': title,
                'url':   link,
                'thumb': thumb,
                'date':  date_text,
                'source': 'innovaTopia',
            })

    return articles

def get_all_news():
    all_articles = []
    for src in SOURCES:
        try:
            articles = scrape_innovatopia(src['url'], src['base'])
            all_articles.extend(articles)
        except Exception as e:
            print(f"[{src['name']}] scrape error: {e}")
    return all_articles
