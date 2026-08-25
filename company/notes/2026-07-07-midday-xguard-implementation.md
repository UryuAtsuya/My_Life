---
date: "2026-07-07"
project: "xguard"
type: midday-implementation
status: historical-run-with-current-sync
current_status: external-runtime-blocked
last_synced: "2026-08-25T17:42:33+09:00"
---

# 2026-07-07 XGuard 昼実装

> [!note] 2026-08-25 同期
> この文書の当初の実装記録とレビュー結果は、2026-07-07 時点の履歴として残す。
> 現在の判断は、次の GitHub 同期結果を正とする。

## 2026-08-25 GitHub 同期結果

### 現状判定

- **実装済み**：X OAuth 2.0 の live token exchange、実Xアカウント照合、profileとrecent postsの保全、暗号化token store、staging deployment contractは `main` へmerge済み。
- **未確認**：実Supabase、実X Developer credential、Railway persistent volume、Sites、staging URLを使った動作は確認できていない。
- **結論**：コードとCIはgreenだが、productionはNo-Goを継続する。

### GitHub

- repository: [UryuAtsuya/Xguard](https://github.com/UryuAtsuya/Xguard)
- default branch: `main`
- `origin/main`: `81bd0d1c8ff7e12795c82668486310369d1b193d`（[PR #68](https://github.com/UryuAtsuya/Xguard/pull/68) で `develop` からpromotion済み）
- `origin/develop`: `db5c596c2b7cb4d05d3cb3cd0c9d5e108b6a18ad`
- open PR: 0件
- branch比較: `develop` は `main` に対して ahead 0、behind 11。
- branch内容: `origin/main` と `origin/develop` のtree差分は0件で、差はmerge履歴だけにある。
- 最新`main` CI: [run 32801287764](https://github.com/UryuAtsuya/Xguard/actions/runs/32801287764) はsuccess。
- CI内訳: Branch policy、Build and test、separated Sites artifacts、Backend container smokeはすべてpass。
- GitHub Environments: `staging` と `production` は存在する。
- GitHub Deployments: 0件。

### Open Issue

- [Issue #44](https://github.com/UryuAtsuya/Xguard/issues/44) はopenのP0。
  schemaとrepository境界は実装済みだが、staging Supabaseへのschema適用、RLS、service-role、transaction、Admin Auth、owner bootstrapは未確認。
- [Issue #45](https://github.com/UryuAtsuya/Xguard/issues/45) はopenのP0。
  [PR #61](https://github.com/UryuAtsuya/Xguard/pull/61) でコード実装は完了したが、実Xアカウントによるconsent、callback、backup、token非露出、Railway再起動後の復号は未確認。
- [Issue #46](https://github.com/UryuAtsuya/Xguard/issues/46) はopenのP1。
  [PR #63](https://github.com/UryuAtsuya/Xguard/pull/63) でdeployment contractとcontainer smokeは追加済みだが、customer、admin、backend、Supabase、X OAuthを接続したstaging E2Eは未実施。

### 2026-07-07レビューとの差分

- fixtureの`MockXApiClient`を使うconfigured runtimeの問題は、PR #61の`LiveXOAuthTokenExchangeService`と`LiveBackupService`へのruntime接続でコード上は解消した。
- `SupabaseApiUsageLedgerHttpStore.runInTransaction`は、現在も複数のHTTP呼び出し全体をPostgreSQL transactionにしているわけではない。
- そのため、API usage ledgerを含む実DB transaction境界は「解消済み」とせず、Issue #44のstaging integrationで確認する。

### Local checkout

- `/Users/uryuatsuya/XGuard/xguard` は `develop` 上でclean、`origin/develop` と一致している。
- local `main` は `origin/main` より3 commits behindだが、今回の状況確認ではbranch switchやfast-forwardを行っていない。

### 次の1手

- Issue #44を先に再開し、staging Supabaseへのschema適用と実DB integration testを1 sliceで実行する。
- success checkは、`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`、RLSとservice-role境界、transaction、owner bootstrapが実環境でpassすること。
- 記録するartifactは、秘密値を含まない実行結果、適用commit SHA、staging URL、Issue #44へのpassまたはblockerコメントとする。

## 2026-07-07 実装記録

### branch

- branch: `feature/media-recovery-schema`
- base SHA: `fd20f370eab97665c0dd2df3ed1e3a85aaad93ad`
- review対象 staged diff SHA: `383f046dc4d348f55995c49b6b0a22524f515dbe6057b5e07861d29d754a540c`
- slice: `backup_runs` の Supabase persistence を runtime 起動経路へ接続する最小案

### agent results

| role | mode | agent_id | base_sha | owned_paths | status | artifact | fallback_reason |
|---|---|---|---|---|---|---|---|
| Implementation | subagent -> fallback | `019f3ad9-4c36-7052-a486-6999fc924ec1` / coordinator | `d9594b617d363f3ab226f6346fc9c98f28f1a431` | `backend/src/app.ts`, `backend/src/serverApp.ts`, `backend/src/repositories/supabaseApiUsageLedgerHttpStore.ts`, tests | timed_out then completed fallback | staged adapter + runtime wiring | subagent timed out after bounded wait |
| Review | subagent | `019f3ae1-2d54-73a1-8906-54068207648b` | `fd20f370eab97665c0dd2df3ed1e3a85aaad93ad` | staged diff read-only | completed | P1 2件 | none |
| Verification | subagent | `019f3ae1-2f54-75c2-96ad-28f9298e85d4` | `fd20f370eab97665c0dd2df3ed1e3a85aaad93ad` | staged diff read-only | completed | targeted checks pass | none |
| Sync planner | subagent | `019f3ae1-320c-7d62-8cc0-3d8de312382b` | `fd20f370eab97665c0dd2df3ed1e3a85aaad93ad` | MyLife proposal only | completed | this note target proposed | none |

### changes

- `SupabaseApiUsageLedgerHttpStore` を追加し、`backup_runs` REST insert/update/list、`record_api_usage_event_with_monthly_limit` RPC、月次APIコスト取得を実装した。
- `createApp` に `apiUsageLedgerRepository` 注入を追加し、`serverApp` の Supabase mode で `SupabaseApiUsageLedgerRepository` を組み立てる案を作った。
- focused test で service-role key を error に含めないこと、timeoutを bounded error にすること、server composition を確認した。

### review findings

- P1: runtime backup path はまだ `MockXApiClient(fixtureAccount, ...)` を使うため、Supabase mode では fixture の `userId` / `xAccountId` が実DBの `user_profiles` / `x_accounts` と整合せず、`backup_runs` FK または RPC UUID/owner check で失敗しうる。
- P1: `SupabaseApiUsageLedgerHttpStore.runInTransaction` は複数REST/RPC呼び出しをDB transactionとして扱えておらず、途中失敗時に `running` backup_run などの部分永続化が残りうる。

### verification

- `git diff --cached --check`: pass
- `npm run test -- --run backend/src/__tests__/serverApp.test.ts backend/src/__tests__/supabaseApiUsageLedgerHttpStore.test.ts backend/src/__tests__/backupProofAuth.test.ts`: pass, 3 files / 28 tests
- `npm run build:api`: pass
- skipped: live Supabase/Postgres integration は credential / 副作用依存のため未実施。

### commit / push

- XGuard commit: なし。P1 review finding と、Implementation agent の遅延操作で current branch が想定 `feature/supabase-backup-run-runtime-store` から `feature/media-recovery-schema` へ変わったため停止。
- XGuard push: なし。
- MyLife commit/push: なし。既存 tracked diff (`AGENTS.md`, `CLAUDE.md`) の所有者不明のため、このnoteはlocal syncに留める。

### blocker

- 次の1手は、mock backup runtime ではなく Supabase-backed `x_accounts` / OAuth account persistence と同一DB transaction境界を先に設計すること。
- それまでは今回の local XGuard diff をそのままpushしない。
- tracked差分があるため、このrunでは branch switch / pull / rebase を追加実行しない。
