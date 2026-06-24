# AIO診断レポートテンプレート

## 目的

SEO / AIO の現状スコアを入口にして、既存サイト内のSEO情報を Entity / Ontology / Structured Data に変換し、AI検索に理解されやすい公式情報基盤へ改善する。

このレポートは露出保証ではなく、以下を明確にするための診断・設計資料として使う。

- 検索エンジンとLLMが理解しやすい情報が揃っているか
- 企業、商品、カテゴリ、競合、実績、専門性の関係が明確か
- AI回答で引用・比較・推薦されるための公式情報が不足していないか
- schema.org / JSON-LD / 内部リンク / FAQ / 比較ページとして何を実装すべきか

## 0. 対象情報

| 項目 | 内容 |
| --- | --- |
| 診断日 |  |
| 対象企業 / サービス |  |
| 対象URL |  |
| 業種 / カテゴリ |  |
| 主な商談対象 |  |
| 主要競合 |  |
| 重要地域 / 言語 |  |
| 診断担当 |  |

## 1. Executive Summary

### 総合判断

- AIO Readiness Score: `/100`
- SEO Foundation Score: `/100`
- Entity / Ontology Score: `/100`
- Structured Data Score: `/100`
- Content Graph Score: `/100`
- AI Answer Risk: `低 / 中 / 高`

### 主要な発見

1.
2.
3.

### 30日以内に優先すべき改善

1.
2.
3.

## 2. SEO / AIO Score

### スコアリング基準

| 領域 | 配点 | 見る情報 | 判定 |
| --- | ---: | --- | --- |
| SEO Foundation | 20 | indexability, title, meta description, heading, canonical, sitemap, robots, page speed, mobile, internal links |  |
| Entity Clarity | 15 | 企業名、サービス名、カテゴリ、対象顧客、提供価値、地域、専門性が明確か |  |
| Category Ownership | 10 | 自社がどのカテゴリの選択肢として理解されるべきかが明示されているか |  |
| Competitor Differentiation | 10 | 競合との差分、比較軸、代替手段との違いが説明されているか |  |
| Evidence Richness | 10 | 導入事例、実績、レビュー、資格、監修者、一次情報があるか |  |
| Content Graph | 15 | カテゴリ、FAQ、用語集、比較、料金、導入事例、会社情報が内部リンクで接続されているか |  |
| Structured Data | 10 | Organization, Service, Product, FAQPage, Article, Review, BreadcrumbList などが適切か |  |
| AI Answer Readiness | 10 | AI回答で引用されやすい明確な公式説明、Q&A、根拠ページがあるか |  |

### 診断結果

| 領域 | 点数 | 根拠 | 改善方針 |
| --- | ---: | --- | --- |
| SEO Foundation |  |  |  |
| Entity Clarity |  |  |  |
| Category Ownership |  |  |  |
| Competitor Differentiation |  |  |  |
| Evidence Richness |  |  |  |
| Content Graph |  |  |  |
| Structured Data |  |  |  |
| AI Answer Readiness |  |  |  |

## 3. SEO情報の棚卸し

既存SEOで使われている情報を、後続の Entity / Ontology / Structured Data へ変換するために整理する。

| SEO情報 | 現状 | Entity / Ontology への変換先 | Structured Data 候補 | 不足 / 改善 |
| --- | --- | --- | --- | --- |
| title |  | Service / Product / Category | WebPage, Service, Product |  |
| meta description |  | 公式説明 / 対象顧客 / 提供価値 | WebPage, Service |  |
| h1 / h2 |  | カテゴリ、課題、機能、対象顧客 | Article, FAQPage, Service |  |
| 主要キーワード |  | Category / Problem / Use case | DefinedTerm, Service |  |
| 会社情報 |  | Organization | Organization, LocalBusiness |  |
| サービス情報 |  | Service / Product | Service, Product |  |
| 料金情報 |  | Offer / Plan | Offer, Product |  |
| FAQ |  | Question / Answer / Risk | FAQPage |  |
| 導入事例 |  | Customer / Use case / Evidence | CreativeWork, Review, Organization |  |
| レビュー / 実績 |  | Proof / Authority | Review, AggregateRating |  |
| 監修者 / 著者 |  | Person / Expertise | Person, Article |  |
| パンくず |  | Site hierarchy | BreadcrumbList |  |
| 内部リンク |  | Entity relationship | WebPage, BreadcrumbList |  |
| 外部言及 |  | Authority / Citation source | sameAs, citation |  |

## 4. AI Answer Simulation

主要な商談・比較・導入検討 prompt を10個定義し、AI回答での扱われ方を観測する。

| # | Prompt | Intent | 自社言及 | 競合言及 | 引用URL | Sentiment | 誤認 / 不足 | 改善に使うページ |
| ---: | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 2 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 3 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 4 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 5 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 6 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 7 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 8 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 9 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |
| 10 |  | 比較 / 推薦 / 導入 / 注意点 |  |  |  |  |  |  |

## 5. Entity Map

### 主要Entity

| Entity | Type | 説明 | 根拠URL | 現状の明確さ | 改善 |
| --- | --- | --- | --- | --- | --- |
|  | Organization |  |  |  |  |
|  | Service / Product |  |  |  |  |
|  | Category |  |  |  |  |
|  | Problem |  |  |  |  |
|  | Audience |  |  |  |  |
|  | Competitor |  |  |  |  |
|  | Evidence |  |  |  |  |
|  | Expert / Author |  |  |  |  |

### Relationship Map

| Source Entity | Relationship | Target Entity | 根拠 | 追加すべき公式情報 |
| --- | --- | --- | --- | --- |
| 自社 | provides | サービス |  |  |
| サービス | belongs_to | カテゴリ |  |  |
| サービス | solves | 課題 |  |  |
| サービス | serves | 対象顧客 |  |  |
| サービス | differs_from | 競合 |  |  |
| 事例 | proves | 提供価値 |  |  |
| 著者 / 監修者 | has_expertise_in | 専門領域 |  |  |

## 6. Ontology / Structured Data 変換案

### Organization

| 項目 | 現状 | 推奨値 | 根拠URL |
| --- | --- | --- | --- |
| name |  |  |  |
| url |  |  |  |
| logo |  |  |  |
| description |  |  |  |
| sameAs |  |  |  |
| areaServed |  |  |  |
| knowsAbout |  |  |  |

### Service / Product

| 項目 | 現状 | 推奨値 | 根拠URL |
| --- | --- | --- | --- |
| name |  |  |  |
| serviceType / category |  |  |  |
| description |  |  |  |
| provider |  |  |  |
| audience |  |  |  |
| offers |  |  |  |
| areaServed |  |  |  |
| hasOfferCatalog |  |  |  |

### FAQPage

| Question | Answer要約 | 根拠URL | AI回答での不足 |
| --- | --- | --- | --- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### Article / Expert Content

| 項目 | 現状 | 推奨値 | 根拠URL |
| --- | --- | --- | --- |
| headline |  |  |  |
| author |  |  |  |
| datePublished / dateModified |  |  |  |
| about |  |  |  |
| mentions |  |  |  |
| citation |  |  |  |

### JSON-LD 下書き

実装前に、事実確認済みの値だけを入れる。推測値は入れない。

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://example.com/#organization",
      "name": "",
      "url": "",
      "description": "",
      "sameAs": []
    },
    {
      "@type": "Service",
      "@id": "https://example.com/#service",
      "name": "",
      "provider": {
        "@id": "https://example.com/#organization"
      },
      "serviceType": "",
      "description": "",
      "audience": ""
    }
  ]
}
```

## 7. Content Gap

| Gap | 影響するAI回答 | 必要なページ / セクション | 優先度 | 理由 |
| --- | --- | --- | --- | --- |
| カテゴリ定義が弱い |  | カテゴリページ / サービスページ | 高 / 中 / 低 |  |
| 競合との差分が弱い |  | 比較ページ / FAQ | 高 / 中 / 低 |  |
| 導入判断の根拠が弱い |  | 事例 / 実績 / レビュー | 高 / 中 / 低 |  |
| 専門性の根拠が弱い |  | 監修者 / 著者 / 会社情報 | 高 / 中 / 低 |  |
| 料金・対象顧客が曖昧 |  | 料金ページ / FAQ | 高 / 中 / 低 |  |
| よくある質問が不足 |  | FAQPage | 高 / 中 / 低 |  |

## 8. Content Graph 改善案

### 推奨ページ構成

| Page | Role | 接続すべきEntity | 内部リンク先 | Structured Data |
| --- | --- | --- | --- | --- |
| トップページ | 公式説明 / 信頼 | Organization, Service | サービス, 事例, FAQ | Organization, WebSite |
| サービスページ | 提供価値 | Service, Audience, Problem | 料金, FAQ, 事例 | Service, Product |
| カテゴリページ | カテゴリ所有 | Category, Problem | 比較, 用語, FAQ | Article, DefinedTerm |
| 比較ページ | 競合差分 | Competitor, Feature | サービス, 料金, 事例 | Article, FAQPage |
| FAQ | 導入不安の解消 | Question, Risk | サービス, 料金 | FAQPage |
| 事例 | 証拠 | Customer, Evidence | サービス, 業種ページ | Article, Review |
| 用語集 | 意味定義 | DefinedTerm | カテゴリ, FAQ | DefinedTerm, Article |

## 9. 30日実装Backlog

| 優先度 | 施策 | 対象URL | 成果物 | 期待効果 | 工数 | 担当 |
| --- | --- | --- | --- | --- | --- | --- |
| P0 |  |  |  |  |  |  |
| P0 |  |  |  |  |  |  |
| P1 |  |  |  |  |  |  |
| P1 |  |  |  |  |  |  |
| P2 |  |  |  |  |  |  |

### P0の実装指示

1.
2.
3.

## 10. 次に自動化する候補

このテンプレートを3件以上で使った後、繰り返し作業だけをツール化する。

| 自動化候補 | 優先度 | 理由 | 入力 | 出力 |
| --- | --- | --- | --- | --- |
| prompt結果の表形式整理 | 高 | 手動集計が重く、レポート品質に直結する | AI回答、引用URL、競合名 | mention / citation / risk表 |
| SEO情報の抽出 | 高 | title, h見出し, schema, FAQを毎回見るため | URL | SEO棚卸し表 |
| Entity候補抽出 | 中 | 人間レビュー前提で効率化できる | ページ本文 | Entity Map草案 |
| schema.org草案生成 | 中 | 実装指示に変換しやすい | Entity Map, ページ種別 | JSON-LD下書き |
| PDF / 提案資料化 | 低 | 価値検証後でよい | Markdown | PDF / Slides |

## 注意事項

- AI検索での表示や引用を保証する表現は使わない。
- `llms.txt` や特殊schemaだけでAIOが改善するような説明は避ける。
- Structured Data は、ページ上に実在する情報と一致させる。
- LLM出力は観測結果であり、事実確認済みの情報として扱わない。
- スコアは絶対評価ではなく、改善優先度を決めるための相対指標として扱う。
