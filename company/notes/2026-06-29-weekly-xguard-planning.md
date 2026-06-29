---
date: "2026-06-29"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-29 週次 XGuard 計画

## 優先順位

XGuardを今週の最優先にする。通常作業ブランチとstagingは`develop`、productionは`main`として扱う。実装は`feature/*`から`develop`へ統合し、staging検証後に`develop`から`main`へ昇格PRを準備する。`main`への直接実装pushは指示しない。

## Branch状態

- 現在checkout: `feature/supabase-integration-preflight`
- 通常作業: `develop = origin/develop = 3c56003`
- staging: `develop = origin/develop = 3c56003`
- production: local `main = 030a916` / `origin/main = e710788`
- `develop...origin/develop`: ahead 0 / behind 0
- `main...origin/main`: ahead 0 / behind 18
- `origin/main`はPR #10で`develop`の`3c56003`まで取り込み済み。local `main`は古いため、production判断では`origin/main`を確認対象にする。
- 現在branch: `feature/supabase-integration-preflight` は未統合。既存未追跡の `.playwright-cli/` と `output/playwright/` は今回対象外として触らない。

## Blocker

- Supabase/Postgres integration環境はまだblocked。`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`、`SUPABASE_DB_URL` または `POSTGRES_URL`、`psql`、`supabase/schema.sql` の全PASSが解除条件。
- proof revoke state と `proof_page_revoked` compliance event の真の同一transaction確認は、proof page永続repository統合時まで未完了。
- OAuth live token exchangeは実X credentialsとproduction callback URLが必要。
- production昇格は、staging検証、実DB境界、OAuth live token exchange、runbook確認が揃うまでNo-Go。

## 今週の実装slice

1. `feature/supabase-integration-preflight`をreviewし、`develop`へ統合してintegration環境不足時のpreflight failureが明確に止まることを確認する。
2. Supabase/Postgres integration環境を確保し、`content_compliance_events` repository mappingの実DBテストを有効化する。
3. proof page永続repository統合時に、proof revoke state と `proof_page_revoked` compliance event を同一transaction化する。
4. 実X OAuth token exchangeのservice boundaryをlive credentialsで検証し、production mock callback/session発行禁止を維持する。
5. stagingでpassした同一commitだけを`develop`から`main`へ昇格PRとして準備する。

Codexへのhandoffは、上記から1 sliceだけを選び、`feature/*`で実装、`develop`統合、staging検証、`main`昇格PR準備の順に書く。
