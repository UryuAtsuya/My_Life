---
date: "2026-05-27"
project: "xguard"
type: project-evening-code-review
status: completed
---

# 2026-05-27 夜コードレビュー

## 結論

XGuardのpush済み正本は `3528e26 Validate API usage ledger inputs` で、`UryuAtsuya/Xguard` `origin/main` に反映済み。夜runの再pushは `Everything up-to-date`。

指定パス `/Users/uryuatsuya/XGuard/xguard` はまだ `not_writable` で、`.git/FETCH_HEAD` も更新できない。local HEAD `e750d04` はpush済み正本 `3528e26` と完全一致しないため、そのままpushしない。

## 主要レビュー指摘

1. P0: 指定パスの `e750d04` は正本 `3528e26` よりdocs/test反映が薄く、同期しないままpushすると再分岐する。
2. P1: Developer Console実画面未確認のため、X API原価、spending limit、Owned Reads適用条件を確定できない。
3. P1: in-memory ledgerの次はSupabase transaction repositoryに移し、`api_usage_events` と `backup_runs` rollup、月次上限stop ruleを一体で検証する必要がある。

## 検証

- 指定パス: `git diff --check` pass、`tsc --noEmit` pass、`vitest` pass（4 files / 11 tests）。`npm run check` は `dist/` 書き込み `EPERM` で失敗。
- 一時checkout `/private/tmp/xguard-midday-2026-05-27`: `git diff --check` pass、`tsc --noEmit` pass、`vitest` pass（4 files / 29 tests）、`npm run check` pass。
- XGuard push確認: `/private/tmp/xguard-midday-2026-05-27` で `git push -v origin main` が `Everything up-to-date`。

## 明日へ送ること

1. `/Users/uryuatsuya/XGuard/xguard` を `origin/main` `3528e26` へ同期する。
2. Developer Console実画面の単価・spending limit・Usage API・Owned Reads条件を `docs/API_COST_MODEL.md` とcompany gateへ転記する。
3. Supabase ledger transaction repositoryと月次API原価上限の超過前停止を実装する。
