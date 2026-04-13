import requests
from bs4 import BeautifulSoup

SOURCES = [
    {
        'name': 'innovaTopia',
        'rss':  'https://innovatopia.jp/feed/',
        'filter': '/ai/',  # AI関連記事のみ
    },
    {
        'name': 'ITmedia AI+',
        'rss':  'https://rss.itmedia.co.jp/rss/2.0/aiplus.xml',
        'filter': None,
    },
    {
        'name': 'AINOW',
        'rss':  'https://ainow.ai/feed/',
        'filter': None,
    },
    {
        'name': 'Zenn AI',
        'rss':  'https://zenn.dev/topics/ai/feed',
        'filter': None,
    },
]

def parse_rss(url, source_name, filter_path=None):
    res = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
    soup = BeautifulSoup(res.content, 'xml')
    articles = []

    for item in soup.find_all('item'):
        link  = item.find('link')
        title = item.find('title')
        date  = item.find('pubDate')
        thumb = item.find('media:thumbnail') or item.find('enclosure')

        if not link or not title:
            continue

        link_url = link.get_text(strip=True) or link.next_sibling
        if not link_url:
            continue

        # フィルタ（特定パスの記事のみ）
        if filter_path and filter_path not in link_url:
            continue

        # サムネイル取得
        thumb_url = ''
        if thumb:
            thumb_url = thumb.get('url') or thumb.get('href') or ''

        # 日付整形
        date_text = ''
        if date:
            raw = date.get_text(strip=True)
            # "Sun, 13 Apr 2026 08:00:00 +0900" → "2026年4月13日"
            try:
                from email.utils import parsedate
                from datetime import datetime
                t = parsedate(raw)
                if t:
                    date_text = f'{t[0]}年{t[1]}月{t[2]}日'
            except Exception:
                date_text = raw[:16]

        articles.append({
            'title':  title.get_text(strip=True),
            'url':    link_url,
            'thumb':  thumb_url,
            'date':   date_text,
            'source': source_name,
        })

    return articles

def get_all_news():
    all_articles = []
    for src in SOURCES:
        try:
            articles = parse_rss(src['rss'], src['name'], src.get('filter'))
            all_articles.extend(articles)
            print(f"[{src['name']}] {len(articles)}件")
        except Exception as e:
            print(f"[{src['name']}] error: {e}")

    # 日付の新しい順に並び替え
    return all_articles
