---
date: "2026-06-24"
project: "xguard"
type: midday-implementation
status: pr-ready
---

# 2026-06-24 XGuard 昼実装

## Branch / Slice

- base SHA: `08576f9b6ee0238f2e3030ff06c5e21472646788`
- branch: `feature/content-compliance-db-contract`
- XGuard commits:
  - `e9aa6e1 Add content compliance schema contract`
  - `6045125 Add content compliance DB contract test`
- PR: `https://github.com/UryuAtsuya/Xguard/pull/7` -> `develop`
- slice: `content_compliance_events` の Supabase/Postgres integration contract を最小追加。

## 変更概要

- `supabase/schema.sql` の `content_compliance_events` table / enum / index / RLS read policy を静的schema contractで確認するようにした。
- 実Supabase/Postgres向けの skip-by-default integration test を追加し、明示フラグとDB URLがある時だけ次を確認できるようにした。
  - authenticated user の直接insert拒否
  - service-role による `proof_page_revoked` event insert
  - authenticated user の own event read と other event 非表示

## Verification

- `git diff --check`: pass
- `git diff --no-index --check -- /dev/null backend/src/__tests__/supabaseSqlContentComplianceEvents.integration.test.ts`: whitespace outputなし
- `npx vitest run --configLoader runner backend/src/__tests__/supabaseSchemaContract.test.ts backend/src/__tests__/supabaseSqlContentComplianceEvents.integration.test.ts`: pass, 2 passed / 1 skipped
- `npx tsc -p tsconfig.json --noEmit`: pass

## Review / Agents

- Implementation: completed。新規 integration test を追加。
- Review: initial P2 2件を指摘。authenticated own-account insert拒否と authenticated read policy 検証を追加後、再reviewは no findings。
- Verification: completed。実DB integration は env gate のため未実行。
- Sync planner: completed。このnoteのみ作成を提案。

## Remaining

- 実Supabase/Postgres integrationは未実行。実行には `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`、`SUPABASE_DB_URL` または `POSTGRES_URL`、必要なら `PSQL_BIN` が必要。
- production No-Go継続。実DBでの `content_compliance_events` 永続化確認、OAuth live token exchange、staging検証、runbookが未完了。
- 既存未追跡の `.playwright-cli/` と `output/playwright/` は今回対象外として未変更。
