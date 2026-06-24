# AIO URL診断プロトタイプ

URLを入力すると、対象ページと `sitemap.xml` 由来の主要ページを取得し、SEO / AIO / Entity / Structured Data の充足状況をルールベースでスコア化するローカルWebアプリです。

## セットアップ

```bash
cd Projects/ontology-aio-service/prototype
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8787
```

ブラウザで `http://127.0.0.1:8787` を開きます。

## 初期版の仕様

- 入力URLを `http` / `https` に正規化
- `/sitemap.xml` を優先して最大20URLを解析
- sitemapがない場合は入力ページ内の同一ドメインリンクを最大10URL解析
- LLM / OpenAI API は未使用
- DB保存、認証、課金、マルチテナントは未実装

## スコア

- `SEO Foundation Score`: title, meta, h1, canonical, sitemap, internal links, HTTP status
- `Entity / Ontology Score`: Organization, Service/Product, カテゴリ、対象顧客、課題、比較、証拠情報
- `Structured Data Score`: JSON-LD, schema.org type, FAQPage, BreadcrumbList など
- `Content Graph Score`: FAQ、比較、料金、事例、用語、会社情報への接続
- `AIO Readiness Score`: 上記の加重平均

スコアは絶対評価ではなく、改善優先度を決めるためのプロトタイプ指標です。
