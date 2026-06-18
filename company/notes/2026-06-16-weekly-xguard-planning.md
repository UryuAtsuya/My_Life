---
date: "2026-06-16"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-16 週次 XGuard 計画

## 優先順位

XGuardを今週の最優先にする。production releaseはNo-Goを維持し、完了済みのruntime confirmation gateとproof revocation auditを新規objectiveとして複製しない。通常作業は`develop`を基準にし、実装は`feature/*`から`develop`へ統合、staging検証後に`develop`から`main`へ昇格する。

## Branch状態

- 現在checkout: `feature/content-compliance-events-repository`（local in-progress）
- 通常作業: `develop = origin/develop = cdcd5b4`
- staging: `develop = origin/develop = cdcd5b4`
- production: `main = origin/main = 030a916`
- `develop...origin/develop`: ahead 0 / behind 0
- `main...origin/main`: ahead 0 / behind 0
- 統合済み: `feature/runtime-confirmation-gates = origin/feature/runtime-confirmation-gates = f27ad55`
- 統合済み: `feature/proof-revocation-audit = origin/feature/proof-revocation-audit = 303bd34` -> `develop = cdcd5b4`

## Blocker

- `feature/runtime-confirmation-gates`は`develop`へ統合済みだが、production昇格判断は未完了。
- `content_compliance_events`は現在process-local in-memoryで、restart / multi-instance時に失われる。
- 実Supabase/Postgres検証に必要なlocal Supabase、`psql`、`DATABASE_URL`、`SUPABASE_SERVICE_ROLE_KEY`が未確認。
- OAuth live token exchangeは実X credentialsとproduction callback URLが必要。
- `output/playwright/`の未追跡成果物は既存状態として触らない。

## 今週の実装slice

1. [x] `feature/runtime-confirmation-gates`を`develop`へ統合し、stagingでruntime confirmation gateを検証する。
2. [x] `feature/proof-revocation-audit`をreview後に`develop`へ統合し、proof revoke時のcompliance event記録をstagingで確認する。
3. `content_compliance_events`永続repositoryを実装し、proof revoke stateとcompliance eventを同一transactionで保存する。
4. Supabase/Postgres integration環境を確保し、role、ownership、X account整合性、存在しないrun、負値、月次上限超過の拒否を確認する。
5. staging検証がpassした同一commitだけを`develop`から`main`へ昇格PRとして準備する。`main`への直接実装pushは行わない。

Codexへのhandoffは、各runで上記から1 sliceだけを選び、`feature/*`で実装、`develop`統合、staging検証、`main`昇格PRの順に書く。
