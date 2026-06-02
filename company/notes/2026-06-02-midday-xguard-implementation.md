---
date: "2026-06-02"
project: "xguard"
type: midday-implementation
status: push_blocked
---

# 2026-06-02 XGuard 昼実装

## 結論

`/Users/uryuatsuya/XGuard/xguard` は今回も `writable=no` だったため、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-06-02-1331` で作業した。

今日の実装スライスは、`backup_run_id` 付き `api_usage_events` に `x_account_id` を必須化し、同じ user 内の別Xアカウントに usage event が曖昧に紐づく余地を消すことに限定した。OAuth改修、Developer Console原価確認、自動DM/follow/write系scopeは触っていない。

## サブエージェント担当

- Implementation agent: `/private/tmp/xguard-midday-2026-06-02-1331` でSQL境界とtestを確認し、schema contract testの読み込み方式を修正した。
- Review agent: 指定パスdirty差分を読み取り、最小スライスは `backup_run_id` account境界強化が妥当と判断した。P1として caller が `backupRunId` と同時に `xAccountId` を渡すかを指摘した。
- Verification agent: coordinator側で `git diff --check`、targeted Vitest、`tsc`、API/web build代替、full testを実行した。
- Documentation/Sync agent: MyLife更新候補と夜レビューTODOを特定した。

真のサブエージェントは利用できた。最終統合、commit、push判断、MyLife同期は coordinator が実施した。

## XGuard 実装内容

- 作業ディレクトリ: `/private/tmp/xguard-midday-2026-06-02-1331`
- XGuard local commit: `33cae26 Require X account for backup usage events`
- 変更:
  - `supabase/schema.sql`: `p_backup_run_id is not null and p_x_account_id is null` を `api_usage_ledger_x_account_required_for_backup_run` で拒否する。
  - `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`: 実DB integration gateに `backup_run_id` あり / `x_account_id` なし拒否ケースを追加する。
  - `backend/src/__tests__/supabaseSchemaContract.test.ts`: 静的schema contract testを追加する。
  - `docs/API_COST_MODEL.md`, `docs/DEPLOY.md`: `backup_run_id` 付きusage eventの `x_account_id` 必須契約を追記する。

## Review agent 指摘と対応

- P0: なし。
- P1: 仕様変更により caller が `backupRunId` だけを渡すと落ちる可能性。`RecordApiUsageInput` は `xAccountId` 必須で、`MockBackupService` と既存service/repository testsも `backupRunId` と同時に `xAccountId` を渡していることを確認した。
- P2: schema contract test は静的文字列検査であり、実Supabase/Postgresのrole/grant/RLS実行を保証しない。これは継続TODOとして残した。
- P2: untracked testがcommit漏れになるリスク。`backend/src/__tests__/supabaseSchemaContract.test.ts` をcommit対象に含めた。

## Verification

Pass:

- `git diff --check`
- `git diff --cached --check`
- `npx vitest run --configLoader runner backend/src/__tests__/supabaseSchemaContract.test.ts backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts backend/src/__tests__/apiUsageLedger.test.ts backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`
  - 3 files passed / 1 skipped、27 passed / 2 skipped
- `npx tsc -p tsconfig.json --noEmit`
- `npm run build:api`
- `npx vite build --config frontend/vite.config.ts --configLoader runner`
- `npm run test`
  - 7 files passed / 1 skipped、41 passed / 2 skipped

未実施 / blocker:

- `npm run check` は `build:web` の既定Vite config loaderが symlinkした `node_modules/.vite-temp` へ書けず `EPERM`。`--configLoader runner` の代替web buildはpass。
- 実Supabase/Postgres integration test本体は `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` と `SUPABASE_DB_URL` / `POSTGRES_URL` がないためskip。
- Developer Console原価確認は未実施。

## Push 状態

- `git ls-remote origin refs/heads/main`: `Could not resolve host: github.com`
- `git push origin main`: GitHubへ到達したが `fetch first` で拒否。
- `git fetch origin main`: `Could not resolve host: github.com`

force pushはしていない。次回はremote先行分をfetchし、`33cae26` をrebase/cherry-pickしてから再検証・pushする。

## 夜レビューへ渡すTop 3

1. GitHub DNS/remote取得が通る環境で `origin/main` をfetchし、`33cae26` をremote先行分へ統合してpushする。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` / `authenticated` / ownership / `x_account_id` 必須 / 月次上限 / 負値拒否を確認する。
3. OAuth configured modeの `state` / S256 PKCE / callback validation / token schema整合と Developer Console原価確認を続ける。
