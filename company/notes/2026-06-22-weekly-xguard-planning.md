---
date: "2026-06-22"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-22 週次 XGuard 計画

## 優先順位

XGuardを今週の最優先にする。production releaseはNo-Goを維持する。通常作業ブランチ、stagingともに`develop`を基準にし、実装は`feature/*`から`develop`へ統合する。staging検証後、同一commitを`develop`から`main`へ昇格PRで進める。`main`への直接実装pushは指示しない。

## Branch状態

- 現在checkout: `develop`
- 通常作業: `develop = origin/develop = cdcd5b4`
- staging: `develop = origin/develop = cdcd5b4`
- production: `main = origin/main = 030a916`
- `develop...origin/develop`: ahead 0 / behind 0
- `main...origin/main`: ahead 0 / behind 0
- 未統合feature: `feature/content-compliance-events-repository = origin/feature/content-compliance-events-repository = ce4de54`
- 既存未追跡: `output/playwright/` と `.playwright-cli/` は今回対象外として触らない。

## Blocker

- `feature/content-compliance-events-repository`はpush済みだが、`develop`へ未統合。
- 実Supabase/Postgres integration環境は未確保。`supabase` / `psql` / `DATABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` の確認が必要。
- proof page state と compliance event の同一transaction確認は、proof page永続repository統合時まで未完了。
- OAuth live token exchange は実X credentialsとproduction callback URLが必要。
- production昇格は、staging検証、実DB境界、OAuth live token exchange、runbookが揃うまでNo-Go。

## 今週の実装slice

1. `feature/content-compliance-events-repository`をreviewし、`develop`へ統合してstagingでrepository境界を確認する。
2. Supabase/Postgres integration環境を確保し、`content_compliance_events` repository mapping の実DBテストを最小追加する。
3. proof page永続repository統合時に、proof revoke state と `proof_page_revoked` compliance event を同一transaction化する。
4. 実X OAuth token exchangeのservice boundaryを追加し、production mock callback/session発行禁止を維持する。
5. stagingでpassした同一commitだけを`develop`から`main`へ昇格PRとして準備する。

Codexへのhandoffは、上記から1 sliceだけを選び、`feature/*`で実装、`develop`統合、staging検証、`main`昇格PR準備の順に書く。
