---
created: "2026-06-02"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard canonical sync / OAuth / Supabase / cost gate

## 内容

`/Users/uryuatsuya/XGuard/xguard` のdirty差分とlive remote正本を照合し、実Supabase/Postgres integration test、OAuth configured mode安全化、Developer Console原価実値確認を閉じる。

## 背景

- XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。
- 2026-06-02朝run時点のlocal `HEAD` / local `origin/main` は `4e6258c`。
- 未コミット変更: `supabase/schema.sql`, `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`
- 未追跡: `backend/src/__tests__/supabaseSchemaContract.test.ts`
- `git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- 指定パスは `writable=no`。
- 昨日夜の記録では `8aa0910 Require X account for backup usage events` が `UryuAtsuya/Xguard` `main` へpush済み。ただし朝runの指定パスは未同期に見えるため、live remote確認が必要。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` のdirty差分を読み、`8aa0910` と同等か追加修正が混ざっているか判定する。昼runでは `backup_run_id` 付きusage eventの `x_account_id` 必須化スライスとして扱った。
- [ ] `git fetch origin main` または `git ls-remote origin refs/heads/main` でlive remote HEADを確認する。
- [x] 指定パスが書けない場合、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-06-02` で一時cloneを作る。実作業場所は `/private/tmp/xguard-midday-2026-06-02-1331`。
- [ ] dirty差分を巻き戻さず、必要差分だけremote正本へrebase/cherry-pickする。local commit `33cae26` は作成済みだが、remote先行とDNS失敗で未push。
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行可、`authenticated` 実行不可を確認する。
- [ ] 実Supabase/Postgresで異user、異Xアカウント、`backup_run_id` 付きで `x_account_id` なし、存在しない `backup_run`、負値、月次上限超過が拒否されることを確認する。
- [ ] OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消する。
- [ ] token repositoryとSupabase schemaの保存契約を一本化する。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、integration test、`npm run check`, `git diff --cached --check` を実行する。`npm run check` はVite既定config loaderの `EPERM` で未完、代替web buildとfull testはpass。実DB integration本体はDB envなしでskip。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。`33cae26` はlocal commit済み、pushは `fetch first` で拒否。
- [x] MyLife側へ昼実装メモ、夜レビュー、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 2026-06-02 Midday update

- XGuard local commit: `33cae26 Require X account for backup usage events`
- Push status: 未push。`git push origin main` は `fetch first`、`git fetch origin main` は `Could not resolve host: github.com`。
- Verification: targeted Vitest pass、`tsc --noEmit` pass、`build:api` pass、`vite build --configLoader runner` pass、`npm run test` pass、`git diff --check` pass、`git diff --cached --check` pass。
- Blocker: 実Supabase/Postgres credentialなし、GitHub remote fetch不可、canonical checkout `writable=no`。

## 2026-06-02 Evening update

- XGuard指定パス最終状態: `HEAD=origin/main=95e6392 Merge remote-tracking branch 'origin/main'`、working tree clean。
- `86a71fb Require X account for backup usage events` と `8aa0910 Require X account for backup usage events` は `95e6392` でmerge済み。
- `git diff --check` と `git ls-files -u` はpass / unmerged entryなし。途中でconflict疑いの報告があったが、Coordinator最終確認では未解決conflictなし。
- Verification: `npx tsc -p tsconfig.json --noEmit` pass、targeted Vitest pass、`npm run test` pass、`npm run build` pass。
- `npm run check` は `dist/backend/...` 上書きが `EPERM` で失敗。コード失敗ではなく権限ブロッカーとして扱う。
- Live remote確認: `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。次回再確認が必要。
- Review P1: `/api/x/oauth/status` はproductionでadmin-onlyまたはdeployment-onlyへ寄せる。
- 残: 実Supabase/Postgres integration test、OAuth state / S256 PKCE / callback validation、token repositoryとSupabase schema契約一本化、Developer Console原価確認。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
