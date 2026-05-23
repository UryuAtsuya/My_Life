---
created: "2026-05-23"
project: "xguard"
type: memo
source: user
---

# XGuard モノレポ開発想定メモ

## ユーザーからの想定

Xアカウント保護サービス「XGuard」をフルスタックで開発する想定。

## サービス概要

XでBANリスクのあるクリエイター向けに、投稿・フォロワーデータを毎日自動バックアップし、BAN発生時に本人証明ページの発行とフォロワーへの移行通知を行うSaaSサービス。月額3,000円のサブスクリプション課金。

## 技術スタック想定

- フロントエンド: Next.js 14 App Router + TypeScript + Tailwind CSS + shadcn/ui
- バックエンド: Node.js + Express + TypeScript
- DB: Supabase PostgreSQL
- 認証: Supabase Auth
- 決済: Stripe 月額3,000円サブスク
- X API: `twitter-api-v2`
- AI: `@anthropic-ai/sdk`
- スケジューラ: `node-cron`
- デプロイ想定: フロントVercel / バックエンドRailway

## プロジェクト構成想定

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

## 初期作業想定

1. 上記のディレクトリ構成を作成する。
2. `frontend/` にNext.js 14プロジェクトを初期化する。
3. `backend/` にExpress + TypeScriptプロジェクトを初期化する。
4. `shared/types.ts` に共通の型定義を作成する。
5. `docs/ARCHITECTURE.md` にシステム全体図と仕様を記載する。
6. ルートに `.gitignore` と `README.md` を作成する。

## 現時点の扱い

- このメモは実装指示ではなく、XGuard開発想定の保存として扱う。
- 実際の `xguard/` モノレポ生成は、次に明示的に開発開始するときに行う。
- 先にX API規約、料金、取得可能データを確認してから実装に入る。
