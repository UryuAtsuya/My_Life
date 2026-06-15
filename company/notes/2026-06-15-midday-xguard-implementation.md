---
date: "2026-06-15"
project: "xguard"
type: midday-implementation
status: completed
---

# Proof revocation compliance event

## 実装

- Branch: `feature/proof-revocation-audit`
- Base SHA: `030a9164df301cf01a47bd5ecfbfe0033e973e9c`
- Commit: `303bd34 Record proof revocation compliance events`
- proof の初回 revoke 成功時に `proof_page_revoked` event を1件記録する。
- 同一 proof の再 revoke、未認証、不正 visibility、存在しない run、他 owner の拒否操作では event を記録しない。
- 対象: `backend/src/app.ts`, `backend/src/__tests__/backupProofAuth.test.ts`
- Scope: prototype in-memory。Supabase 永続化は production 向け別 slice。

## Review

- Final diff SHA-256: `e32bf32c3aa019ef2728064964df67bb21cef4368b5ee51725b6e8aa02ddaa25`
- Findings: なし

## Verification

- `git diff --check`: exit 0
- `npx tsc -p tsconfig.json --noEmit`: exit 0
- `npx vitest run --configLoader runner backend/src/__tests__/backupProofAuth.test.ts`: exit 0、13/13 pass
- 全体 test / frontend build: 今回の targeted slice 外のため未実施

## Push

- `origin/feature/proof-revocation-audit` へ push 済み
- `main` への直接 push なし

## Blocker

- Supabase CLI / Postgres integration 環境は未確保のため、実 DB integration test は継続 blocker。
