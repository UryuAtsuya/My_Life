---
date: "2026-05-28"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-05-28 XGuard 朝計画

## 朝会結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定パス同期、Developer Console原価確認、Supabase ledger transaction repository化に絞る。

## 現状

- XGuard実装repoの想定パス: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`, `main...origin/main [ahead 1]`, HEAD `e750d04`
- push済み正本: `/private/tmp/xguard-midday-2026-05-27` の `3528e26 Validate API usage ledger inputs`
- 判断: local `e750d04` は正本と完全一致しないため、そのままpushしない。

## 昼の実装スコープ

### 作業ディレクトリ

1. まず `/Users/uryuatsuya/XGuard/xguard` で `test -w`, `git status --short --branch`, `git rev-parse --short HEAD` を確認する。
2. 書き込み可能なら、指定パスを `origin/main` のpush済み正本 `3528e26` 以降へ同期して作業する。
3. 書き込み不可なら、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-28` を作り、`UryuAtsuya/Xguard` の一時cloneで作業する。

### 変更対象ファイル

- `docs/API_COST_MODEL.md`: Developer Console実値、credit/spending設定、Usage endpoint、Owned Reads適用条件を記録する。
- `backend/src/repositories/supabaseApiUsageLedgerRepository.ts`: Supabase transaction repositoryを追加する。
- `backend/src/services/apiUsageLedger.ts`: 月次API原価上限の超過前停止に必要なrepository境界を追加する。
- `backend/src/__tests__/apiUsageLedger.test.ts`: `api_usage_events` 記録、`backup_runs` rollup、上限超過前停止、transaction失敗時の未反映を検証する。
- `shared/types.ts`: repository入出力型が不足する場合のみ最小更新する。
- `supabase/schema.sql`: 既存の `api_usage_events`, `backup_runs`, `user_profiles.monthly_api_cost_limit_usd` で足りない制約やindexがあれば最小更新する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx vitest run --configLoader runner`
- `npm run check`
- stage後に `git diff --cached --check`

## 今日の上位TODO

1. `/Users/uryuatsuya/XGuard/xguard` の書き込み可否を再確認し、可能ならpush済み正本 `3528e26` へ同期する。
2. Developer Console実画面でendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を確認する。
3. `SupabaseApiUsageLedgerRepository` と月次API原価上限stop ruleを実装・検証する。
