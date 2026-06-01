---
date: "2026-06-01"
project: "xguard"
type: evening-code-review
status: completed_with_push
---

# 2026-06-01 夜レビュー: backup run usage境界

## 結論

前回未push扱いだった `2655267` は現在の `main` 履歴に含まれていた。今日の昼成果も `4e6258c` まで取り込まれていたため、夜レビューでは `backup_run_id` 付きusage eventの `x_account_id` 必須化だけを小さく追加し、`8aa0910 Require X account for backup usage events` を `UryuAtsuya/Xguard` `main` へpushした。

## レビュー結果

- P0: なし。
- P1: `backup_run_id` 付きusage eventで `x_account_id` がnullの場合、同一Xアカウント整合性が曖昧になる。対応済み。
- P1: OAuth configured modeはまだ静的state、mock/plain PKCE、callback未照合。実OAuth前に本実装が必要。
- P1: token repository契約とSupabase schema契約がズレている。
- P2: CORS全開、OAuth status未認証、実DB integration testがskip-by-default。

## 反映

- XGuard commit: `8aa0910 Require X account for backup usage events`
- Push先: `UryuAtsuya/Xguard` `main`
- 作業コピー: `/private/tmp/xguard-evening-20260601-5YPt9Z`
- canonical checkout: `/Users/uryuatsuya/XGuard/xguard` は `writable=no` のため直接編集不可。

## 検証

- `/private/tmp/xguard-evening-20260601-5YPt9Z`: `git diff --check`, targeted Vitest, `tsc --noEmit`, `npm run check`, `git diff --cached --check` pass。
- `/Users/uryuatsuya/XGuard/xguard`: `tsc --noEmit` と `npm run test` はpass。`npm run check` は `dist/` 書き込み `EPERM`。

## 次

1. 実Supabase/Postgres integration testを実行する。
2. OAuth state / S256 PKCE / callback validationとtoken schema整合を進める。
3. Developer Console原価実値を確認し、docsとcompany gateへ反映する。
