from flask import Flask, render_template, jsonify
from scraper import get_all_news
import threading, time

app = Flask(__name__)

# キャッシュ（30分ごとに更新）
_cache = {'articles': [], 'updated_at': ''}

def refresh_cache():
    while True:
        try:
            articles = get_all_news()
            _cache['articles'] = articles
            _cache['updated_at'] = time.strftime('%Y年%m月%d日 %H:%M')
            print(f"[cache] {len(articles)}件取得")
        except Exception as e:
            print(f"[cache] error: {e}")
        time.sleep(1800)  # 30分

# バックグラウンドで定期更新
t = threading.Thread(target=refresh_cache, daemon=True)
t.start()

@app.route('/')
def index():
    if not _cache['articles']:
        # 初回アクセス時は同期取得
        _cache['articles'] = get_all_news()
        _cache['updated_at'] = time.strftime('%Y年%m月%d日 %H:%M')
    return render_template('index.html',
                           articles=_cache['articles'],
                           updated_at=_cache['updated_at'])

@app.route('/api/news')
def api_news():
    return jsonify(_cache['articles'])

if __name__ == '__main__':
    app.run(debug=True)
