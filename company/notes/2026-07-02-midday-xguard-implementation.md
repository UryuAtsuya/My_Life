---
date: "2026-07-02"
project: "xguard"
type: midday-implementation
status: pushed
---

# 2026-07-02 XGuard 昼実装

## Branch / Slice

- base SHA: `a9db5b52f8173cbb8f82d38d0af2789b55128872`
- branch: `feature/proof-page-revocation-transaction`
- XGuard commit: `6041afdfa04b10428e6c89a49b9469a49057113a`
- PR: https://github.com/UryuAtsuya/Xguard/pull/23 -> `develop`
- slice: proof page revoke state と `proof_page_revoked` compliance event を repository/store transaction 境界へ寄せた。

## State

- `ProofPageRepository` に revocation event 付き更新の専用methodを追加した。
- `SupabaseProofPageRepository` は `updateProofPageVisibilityAndRecordContentComplianceEvent` を必須store境界として使う。
- in-memory proof page repository も event 記録失敗時に visibility 更新を巻き戻す。
- app route は revoke event を proof page repository 更新へ渡し、proof page state と audit event の分離書き込みfallbackを削除した。
- server composition は Supabase compliance mode で transaction-capable proof page store がない場合に起動拒否する。

## Verification

- `git diff --check`: pass
- targeted Vitest: `backend/src/__tests__/proofPageRepository.test.ts`, `backend/src/__tests__/backupProofAuth.test.ts`, `backend/src/__tests__/serverApp.test.ts` pass
- `npm run build:api`: pass
- `npm run check`: pass
- Final Review agent: no findings

## Remaining

- 実 Supabase/Postgres store の `updateProofPageVisibilityAndRecordContentComplianceEvent` 接続と実DB transaction検証は未完了。
- production No-Go 継続。実DB transaction、OAuth live token exchange、staging検証、runbookが未完了。
- 既存未追跡の `.playwright-cli/` と `output/playwright/` は今回対象外として未変更。

## Next Slice

- Supabase/Postgres store 実装で proof page visibility update と `content_compliance_events` insert を同一 transaction として実DB検証する。
