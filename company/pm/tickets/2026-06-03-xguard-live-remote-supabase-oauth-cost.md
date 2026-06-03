---
created: "2026-06-03"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard live remote / Supabase / OAuth / cost gate

## 内容

`/Users/uryuatsuya/XGuard/xguard` のlive remote状態を確認し、実Supabase/Postgres integration test、OAuth configured mode安全化、Developer Console原価実値確認を閉じる。

## 背景

- XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。
- 2026-06-03朝run時点のlocal `HEAD` / local `origin/main` は `95e6392`。
- 指定パスは `main...origin/main` で、朝runからは `writable=no`。
- 前回夜レビューでは `HEAD=origin/main=95e6392`、working tree clean。
- live GitHubの独立確認はDNS失敗で未完了。次回 `git ls-remote origin refs/heads/main` と `git fetch origin main` を再確認する。

## 完了条件

- [ ] `git fetch origin main` または `git ls-remote origin refs/heads/main` でlive remote HEADを確認する。
- [ ] `/Users/uryuatsuya/XGuard/xguard` が書けない場合、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-06-03` で作業する。
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行可、`authenticated` 実行不可を確認する。
- [ ] 実Supabase/Postgresで異user、異Xアカウント、`backup_run_id` 付きで `x_account_id` なし、存在しない `backup_run`、負値、月次上限超過が拒否されることを確認する。
- [ ] OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消する。
- [ ] token repositoryとSupabase schemaの保存契約を一本化する。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [ ] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、integration test、`npm run test`, `npm run build`, `npm run check`, `git diff --cached --check` を実行する。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] MyLife側へ昼実装メモ、夜レビュー、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。

## 2026-06-03 midday update

- [x] `/Users/uryuatsuya/XGuard/xguard` は昼runでも `writable=no`。Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-06-03-1339` で作業した。
- [x] `/api/x/oauth/status` をproductionで `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` と `x-xguard-diagnostic-token` header一致時だけ返すdiagnostic endpointへ寄せた。
- [x] `docs/API_SPEC.md` / `docs/DEPLOY.md` にproduction access条件とbackend runtime secretを反映した。
- [x] XGuard local commit `9e8b7c5 Guard OAuth status diagnostic in production` を作成した。
- [ ] `9e8b7c5` は未push。`git push origin main` は `fetch first`、その後の `git fetch origin main` / `git ls-remote origin refs/heads/main` はDNS失敗。
- [x] 最終確認で指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled`。`03ecd2f` を正として扱い、`9e8b7c5` は丸ごとpushしない。
- [ ] 実Supabase/Postgres integration test、OAuth `state` / S256 PKCE / callback validation、token schema契約、Developer Console原価確認は未完了。
