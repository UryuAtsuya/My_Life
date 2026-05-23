---
created: "2026-05-23"
project: "xguard"
type: evening-code-review
status: reviewed-with-blockers
---

# 2026-05-23 XGuard Evening Code Review Note

## 結論

XGuardの実装ディレクトリ `/Users/uryuatsuya/XGuard/xguard` は空で、git repoでもない。今日のレビュー対象は実装コードではなく、MyLife側に保存されたDBスキーマ、モノレポ計画、型ドラフト、要件定義になった。

現時点で明日実装へ進む前に潰すべきP0は、X API規約・料金・取得範囲の確認と、X OAuth tokenの安全な保管設計。

## 主要指摘

1. `supabase-v0-schema.sql` にX OAuth token保管・更新・失効のモデルがない。
2. X APIで取得・保存・公開できるデータ範囲が未確認のまま、raw payloadや証明ページ生成を前提にしている。
3. `tweet_snapshots` のunique制約が、architectureの「upsert」と「時系列snapshot」の両方を曖昧にしている。
4. 証明ページに公開/非公開、取り下げ、slug再生成、redaction方針がない。
5. Stripe webhookの冪等性と購読状態更新の順序が未設計。

## 明日の実装前ゲート

- X APIデータ範囲表を作る。
- OAuth token保存テーブルまたはSupabase Vault利用方針を決める。
- 証明ページ公開DTOとredaction方針を決める。
- tweet snapshotは時系列履歴か最新upsertかを決める。
- XGuard実装ルートの書き込み権限を解決する。
