---
date: "2026-06-24"
project: "xguard"
type: evening-code-review
status: completed
---

# 2026-06-24 XGuard 夜レビュー

## Branch

- mode: Wednesday midweek audit
- XGuard current branch: `feature/content-compliance-db-contract`
- staging branch: `develop`
- production branch: `main`
- staging local: `develop` = `08576f9b6ee0238f2e3030ff06c5e21472646788`
- staging remote: `origin/develop` = `bfed1c6951c25cde122d8d98a7cff641dcbc3f18`
- production local: `main` = `030a9164df301cf01a47bd5ecfbfe0033e973e9c`
- production remote: `origin/main` = `04d81dffcedfe6180da0a917df287b0058e5065c`
- branch relation: `develop...origin/develop` = `0 3`; `main...origin/main` = `0 15`; divergedなし。
- reviewed range: `08576f9b6ee0238f2e3030ff06c5e21472646788..bfed1c6951c25cde122d8d98a7cff641dcbc3f18`

## Agents

| role | mode | agent_id | base_sha | owned_paths | status | artifact | fallback_reason |
|---|---|---|---|---|---|---|---|
| Implementation | not_applicable | n/a | `08576f9` | n/a | completed | 安全な小修正対象なし | n/a |
| Review | subagent | `019ef8dd-613b-7053-ad5c-4db9f16224c8` | `08576f9` | `supabase/schema.sql`, `backend/src/__tests__/supabaseSchemaContract.test.ts`, `backend/src/__tests__/supabaseSqlContentComplianceEvents.integration.test.ts` | completed | P0/P1なし、P2 1件 | n/a |
| Verification | subagent | `019ef8dd-6401-7e12-a0fc-1d37c6f56600` | `08576f9` | verification commands | completed | targeted verification exit 0 | n/a |
| Sync planner | subagent | `019ef8dd-66e2-7261-a70a-3feef8cbffe4` | `feab064` | MyLife planning only | completed | このnote 1件のみ提案 | n/a |

## Findings

- P0: なし。
- P1: なし。
- P2: `content_compliance_events` のDB contractは、`x_account_id` と `proof_page_id` の同一account所属を検証していない。service-role bug が user A の `x_account_id` と user B の `proof_page_id` を混在させた場合、RLS上は user A 側へ audit row が見え、別proof page UUIDを含む誤った監査行になる可能性がある。`proof_pages.x_account_id = content_compliance_events.x_account_id` を composite FK、trigger、または service-role insert boundary で検証する必要がある。`tweet_snapshot_id` も同じ観点で確認する。

## Verification

| command | exit | result |
|---|---:|---|
| `git diff --check 08576f9..bfed1c6` | 0 | pass |
| `npx vitest run --configLoader runner backend/src/__tests__/supabaseSchemaContract.test.ts backend/src/__tests__/supabaseSqlContentComplianceEvents.integration.test.ts` | 0 | pass; 2 passed / 1 skipped |
| `npx tsc -p tsconfig.json --noEmit` | 0 | pass |

- 実Supabase/Postgres integrationは env gate のため skip。必要条件は `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`、`SUPABASE_DB_URL` または `POSTGRES_URL`、必要なら `PSQL_BIN`。

## Staging / Production Blocker

- staging: `origin/develop` に PR #7 `feature/content-compliance-db-contract` merge済み。ただし local `develop` は `origin/develop` に behind 3。
- production: `origin/main` に PR #8 `develop` merge済み。ただし local `main` は `origin/main` に behind 15。
- production blocker: 実DB integration、cross-account resource linkage guard、OAuth live token exchange、staging検証runbookが未完了。production昇格候補として追加作業が必要。

## Next

1. `content_compliance_events` と `proof_page_id` / `tweet_snapshot_id` の同一account linkageをDBまたはrepository boundaryで検証する。
2. 実Supabase/Postgres integration環境で `content_compliance_events` 永続化とRLS境界を確認する。
