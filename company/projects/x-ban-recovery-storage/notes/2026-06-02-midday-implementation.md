---
date: "2026-06-02"
project: "xguard"
type: project-midday-implementation
status: push_blocked
---

# 2026-06-02 昼実装メモ

## 実装スライス

`backup_run_id` 付き usage event に `x_account_id` を必須化する。これにより、usage ledgerのDB境界で `backup_runs.x_account_id` と event側 `x_account_id` が一致することを常に要求する。

## 成果

- 一時作業場所: `/private/tmp/xguard-midday-2026-06-02-1331`
- XGuard local commit: `33cae26 Require X account for backup usage events`
- 変更ファイル:
  - `supabase/schema.sql`
  - `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`
  - `backend/src/__tests__/supabaseSchemaContract.test.ts`
  - `docs/API_COST_MODEL.md`
  - `docs/DEPLOY.md`

## 検証

- `git diff --check`: pass
- `git diff --cached --check`: pass
- targeted Vitest: pass、SQL integration fileはDB envなしのためskip
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npm run build:api`: pass
- `npx vite build --config frontend/vite.config.ts --configLoader runner`: pass
- `npm run test`: pass
- `npm run check`: Vite既定config loaderが symlink `node_modules/.vite-temp` へ書けず `EPERM`

## 未完了

- XGuard pushは未完了。`git push origin main` は `fetch first`、その後の `git fetch origin main` はDNS失敗。
- 実Supabase/Postgres integration test本体は未実行。
- OAuth configured mode安全化とDeveloper Console原価確認は未着手。
