---
date: "2026-06-01"
project: "xguard"
type: midday-implementation
status: completed_with_push_blocked
---

# 2026-06-01 昼実装: usage ledger schema contract

## 作業場所

- 正本確認: `/Users/uryuatsuya/XGuard/xguard`
- 正本状態: local `HEAD` / local `origin/main` は `2655267 Filter revoked tweet snapshots from proof DTO`
- 正本の問題: `writable=no`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`
- live remote確認: `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`
- 実装場所: `/private/tmp/xguard-midday-2026-06-01-1331`
- XGuard local commit: `8cf029c Harden usage ledger schema contract`
- XGuard push: 未完了。`git push origin main` は `Could not resolve host: github.com`

## 変更

`record_api_usage_event_with_monthly_limit` のmigration前提を、実DBなしでもCIで壊れにくくするため、local schema contract testを追加した。

- `backup_run_id` 付き usage event は `x_account_id` 必須に変更。
- `backup_runs.x_account_id = p_x_account_id` を常に要求。
- `api_usage_events` と `backup_runs` のcost / metering系にnon-negative `check` を追加。
- `backend/src/__tests__/supabaseSchemaUsageLedger.test.ts` でrole grant、revoke、ownership、monthly limit、負値拒否のschema契約を検証。
- `docs/API_COST_MODEL.md` と `docs/DEPLOY.md` にlocal contract testと実DB未検証の境界を追記。

## Review agent

- P0: なし。
- P1: 当初SQLでは `backup_run_id` ありでも `p_x_account_id is null` を許し、同一Xアカウント検証を実質スキップできた。対応済み。
- P1: 追加テストが未追跡でcommit漏れするリスク。stageしてcommit済み。
- P2: schema contract testは文字列検査中心で、Postgres上の権限解決や関数実行までは保証しない。未完として継続。

## Verification agent

- `git diff --check`: pass
- `git diff --cached --check`: pass
- targeted Vitest: pass
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npm run check`: pass、7 files / 43 tests

## 次

1. DNS復旧後に `8cf029c` を `UryuAtsuya/Xguard` へpushする。force pushしない。
2. 実Supabase/Postgresで `service_role` / `authenticated` のrole別RPCと拒否条件を確認する。
3. Developer Console原価確認を `docs/API_COST_MODEL.md` とcompany gateへ反映する。
