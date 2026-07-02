---
date: "2026-07-02"
project: "xguard"
type: implementation-sync
status: pushed-pr
---

# 2026-07-02 XGuard proof page revocation transaction

- XGuard branch: `feature/proof-page-revocation-transaction`
- XGuard commit: `6041afd`
- PR: `https://github.com/UryuAtsuya/Xguard/pull/23`
- slice: proof page visibility revoke と `proof_page_revoked` content compliance event の同一 store transaction boundary

## 変更

- `SupabaseProofPageStore` に `updateProofPageVisibilityAndRecordContentComplianceEvent` contract を追加した。
- proof page revocation route は、transaction 対応 repository では visibility update と compliance event insert を同一 store operation に渡す。
- `CONTENT_COMPLIANCE_EVENT_REPOSITORY=supabase` なのに proof page transaction store がない構成は startup error にした。
- in-memory prototype path は従来通り proof page repository と compliance event repository を分けるが、Supabase production-facing partial-write 構成には進めない。

## 検証

- `git diff --check`
- `npm test -- --run backend/src/__tests__/proofPageRepository.test.ts backend/src/__tests__/backupProofAuth.test.ts backend/src/__tests__/serverApp.test.ts`
- `npm run check`

## 残り

- Production No-Go は継続。
- real Supabase proof page transaction store implementation は未接続。
- PR label `codex` / `codex-automation` は repository に存在せず付与できなかった。
