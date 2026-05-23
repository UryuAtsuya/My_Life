---
created: "2026-05-23"
project: "xguard"
status: planning
tags: [monorepo, nextjs, express, supabase, stripe]
---

# XGuard モノレポ技術計画

## 目的

Next.jsフロントエンド、Express API、共通型定義、仕様書を1つの `xguard/` モノレポとして管理する。

## ローカル実装場所

- 実装ディレクトリ: `/Users/uryuatsuya/XGuard/xguard`
- MyLife Vaultの役割: 要件、調査、PM、レビュー、意思決定の正本
- XGuard実装ディレクトリの役割: 実際のNext.js/Expressコード、shared types、docs

## Daily Automation Loop

| 時間帯 | automation | 役割 | 主な成果物 |
|---|---|---|---|
| 朝 | `morning-company-business-meeting` | X BAN、X API、規約、料金、競合、市場調査。昼の実装スコープ決定。 | 調査メモ、当日Top 3、実装スコープ |
| 昼 | `midday-company-production-session` | `/Users/uryuatsuya/XGuard/xguard` でモノレポ作成・実装。 | frontend/backend/shared/docs、検証結果、実装メモ |
| 夜 | `evening-company-closeout-review` | コードレビュー、修正案、翌日TODO整理。 | review note、修正案、翌日Top 3 |

## 想定ディレクトリ

```text
xguard/
├── frontend/
├── backend/
├── shared/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── API_SPEC.md
│   └── DEPLOY.md
├── .gitignore
└── README.md
```

## frontend

- Next.js 14 App Router
- TypeScript
- Tailwind CSS
- shadcn/ui
- Supabase Authクライアント
- Stripe Checkout / Customer Portal導線

### 初期画面案

- LP
- サインアップ/ログイン
- ダッシュボード
- Xアカウント接続
- バックアップ状況
- 復元モード
- 証明ページ
- 課金管理

## backend

- Node.js
- Express
- TypeScript
- `twitter-api-v2`
- `@anthropic-ai/sdk`
- `node-cron`
- Stripe webhook
- Supabase service role client

### 初期API案

- `GET /health`
- `POST /api/x/connect`
- `POST /api/backup/run`
- `GET /api/backup/status`
- `POST /api/recovery/start`
- `GET /api/recovery/:id/proof`
- `POST /api/stripe/create-checkout-session`
- `POST /api/stripe/webhook`

## shared

`shared/types.ts` にフロントとバックエンドで共有する型を置く。

### 初期型案

- `UserProfile`
- `XAccount`
- `TweetSnapshot`
- `ProfileSnapshot`
- `AccountHealthCheck`
- `RecoverySession`
- `SubscriptionStatus`

## docs

- `ARCHITECTURE.md`: 全体構成、データフロー、ジョブ構成
- `API_SPEC.md`: API一覧、リクエスト/レスポンス、認証
- `DEPLOY.md`: Vercel、Railway、Supabase、Stripe、X API設定

## 実装順

1. `xguard/` のルート構成を作る。
2. `frontend/` をNext.js 14で初期化する。
3. `backend/` をExpress + TypeScriptで初期化する。
4. `shared/types.ts` を作る。
5. Supabaseスキーマを定義する。
6. StripeサブスクのCheckoutとwebhookを作る。
7. X APIのバックアップジョブを作る。
8. 証明ページを作る。

## 注意点

- `@anthropic-ai/sdk` は移行文生成や証明ページ文面生成に使う。v0では必須機能にしない。
- フォロワー通知は自動送信ではなく、まずは通知文生成と候補リスト表示にする。
- `node-cron` はRailway上で常駐できる前提だが、運用では単一インスタンス制御が必要。
- Stripe webhookはバックエンド側で受け、Supabaseに購読状態を保存する。
