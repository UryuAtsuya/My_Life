---
created: "2026-06-01"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard live remote / Supabase / cost verification

## 内容

`/Users/uryuatsuya/XGuard/xguard` のlive remote状態を確認し、実Supabase/Postgres migration test、Developer Console原価実値確認、OAuth診断endpointの公開条件整理を閉じる。

## 背景

- XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。
- 2026-06-01朝run時点のlocal `HEAD` / local `origin/main` は `2655267 Filter revoked tweet snapshots from proof DTO`。
- `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- `git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- 指定パスは `writable=no`。昼runでは最初にwrite/fetch/live remote確認を行う。
- `GET /api/x/oauth/status` はsecret/token/client id値を返さないが、本番公開前にadmin認証付きhealth checkまたはdeployment-only routeへ寄せる。
- 残る最重要は、実Supabase/Postgres migration test、Developer Console原価実値確認。

## 完了条件

- [ ] `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/live remote HEADを昼run冒頭で確認する。
- [ ] `2655267` が `UryuAtsuya/Xguard` live remote `origin/main` と一致するか確認する。
- [ ] 一時clone `09ff660 Add OAuth status endpoint` を `2655267` 系列と比較し、必要差分がなければ破棄、必要差分があればcherry-pickで統合する。
- [x] local schema contract testで `record_api_usage_event_with_monthly_limit` の `security definer`、`search_path`、`service_role` grant、`authenticated` revoke、ownership、月次上限、負値拒否を検知できるようにする。Evidence: XGuard local commit `8cf029c`。
- [ ] 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の `service_role` 実行可、`authenticated` 実行不可を確認する。
- [ ] 実Supabase/Postgres migration testで異user、異Xアカウント、`backup_run_id` 付きで `x_account_id` なし、存在しない `backup_run`、負値、月次上限超過が拒否されることを確認する。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [x] `/api/x/oauth/status` の本番公開条件をadmin認証付きhealth checkまたはdeployment-only routeとしてdocsへ反映する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, `git diff --cached --check` を実行する。
- [x] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。Evidence: `8aa0910 Require X account for backup usage events`
- [ ] MyLife側へ昼実装メモ、夜レビュー、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 2026-06-01 昼実装結果

- `/Users/uryuatsuya/XGuard/xguard` は `writable=no`。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`、`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- 実装場所は `/private/tmp/xguard-midday-2026-06-01-1331`。Vaultへ実装コードは置いていない。
- XGuard local commit: `8cf029c Harden usage ledger schema contract`。
- XGuard push: 未完了。`git push origin main` は `Could not resolve host: github.com`。
- 検証: `git diff --check`、targeted Vitest、`npx tsc -p tsconfig.json --noEmit`、`npm run check`（7 files / 43 tests）、`git diff --cached --check` pass。

## 2026-06-01 夜レビュー結果

- `2655267 Filter revoked tweet snapshots from proof DTO` は現在の `main` 履歴に含まれていた。
- `4e6258c Merge remote-tracking branch 'origin/main'` まで正本に取り込まれていたため、夜レビューでは `backup_run_id` 付きusage eventの `x_account_id` 必須化だけを追加した。
- XGuard commit: `8aa0910 Require X account for backup usage events`
- XGuard push: 完了。`UryuAtsuya/Xguard` `main` へ `4e6258c..8aa0910` を反映。
- 検証: `/private/tmp/xguard-evening-20260601-5YPt9Z` で `git diff --check`、targeted Vitest、`tsc --noEmit`、`npm run check`（7 files passed / 1 skipped、41 passed / 2 skipped）、`git diff --cached --check` pass。
- canonical `/Users/uryuatsuya/XGuard/xguard` は `writable=no` のまま。`npm run check` は `dist/` write `EPERM`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
