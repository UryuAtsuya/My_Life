---
date: "2026-06-07"
project: "xguard"
type: evening-code-review
status: completed-with-blockers
---

# 2026-06-07 夜レビュー

XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。朝時点の3ファイル差分とproof visibility management endpointは、`9ac4f2f Add proof visibility management route` として `UryuAtsuya/Xguard` `origin/main` へpush済み。

その後、owner-only `PATCH /api/recovery/:runId/proof/visibility` も `9ac4f2f` として反映済み。

production releaseはNo-Go継続。backup / proofのprivate defaultは前進したが、OAuth configured modeの実token exchange、実Supabase/Postgres検証、cost/compliance release gateが残っている。

## レビュー結果

- P0: OAuth configured modeが実X token exchangeなしでsessionを発行する。任意 `code` + 正しい `state` だけでprototype sessionが作れるため、productionではNo-Go。
- P1: 実Supabase/Postgres integration testがskip状態。SQL functionのrole / ownership / monthly limit境界を実DBで確認できていない。
- P1: cost/compliance release gateがCI/runtimeで機械的に止まらない。
- P1: OAuth state storeがin-memoryで、multi-instanceではcallback/replay契約が不安定。
- P2: proof visibilityをownerが通常APIで変更するrouteは実装済み。残りは監査/compliance event記録。

## 検証

- pass: `git diff --check`, `git diff --cached --check`, `npx tsc -p tsconfig.json --noEmit`, targeted `backupProofAuth.test.ts`, Verification agentの `npm run test`。
- pushed: XGuard `9ac4f2f Add proof visibility management route` -> `UryuAtsuya/Xguard` `main`。
- blocker: `npm run check` は `dist/backend/...` 書き込み `EPERM`。
- blocker: `git ls-remote` はDNS失敗。
- skipped: 実Supabase/Postgres integration test。DB URL / `psql` 条件不足。

## 明日の実装順

1.  proof visibility endpointをcommit/pushする。
2. OAuth configured modeの実token exchangeとproduction mock callback禁止。
3. 実Supabase/Postgres usage ledger integration testとcost/compliance docs更新を進める。
