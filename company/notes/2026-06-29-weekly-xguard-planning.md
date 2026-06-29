---
date: "2026-06-29"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-29 週次 XGuard 計画

## 優先順位

XGuardを今週の最優先にする。production releaseはNo-Goを維持する。通常作業ブランチ、stagingともに`develop`を基準にし、実装は`feature/*`から`develop`へ統合する。staging検証後、同一commitを`develop`から`main`へ昇格PRで進める。`main`への直接実装pushは指示しない。

## Branch状態

- 現在checkout: `feature/supabase-integration-preflight = origin/feature/supabase-integration-preflight = c2522e8`
- 通常作業: `develop = origin/develop = 3c56003`
- staging: `develop = origin/develop = 3c56003`
- production: local `main = 030a916`、`origin/main = e710788`
- `develop...origin/develop`: ahead 0 / behind 0
- local `main...origin/main`: ahead 0 / behind 18
- `origin/develop...origin/main`: ahead 0 / behind 4。`origin/develop` は `origin/main` に含まれている。
- 未統合feature: `feature/supabase-integration-preflight = origin/feature/supabase-integration-preflight = c2522e8`
- 既存未追跡: `.playwright-cli/` と `output/playwright/` は今回対象外として触らない。

## Blocker

- `feature/supabase-integration-preflight` はpush済みだが、`develop`へ未統合。
- 実Supabase/Postgres integration環境は未確保。preflightでは `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`、DB URL、`psql` が不足している。
- OAuth live token exchange、staging smoke/runbook evidence、production昇格は未完了。
- production昇格は、staging検証、実DB境界、OAuth live token exchange、runbookが揃うまでNo-Go。

## 今週の実装slice

1. PR #11 `feature/supabase-integration-preflight` をreviewし、`develop`へ統合してpreflightをstaging作業の入口にする。
2. preflightが `PASS` になる環境を用意し、`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` で実Supabase/Postgres integrationを1回通す。
3. stagingで `CONTENT_COMPLIANCE_EVENT_REPOSITORY=supabase` を使い、`proof_page_revoked` eventが実DBへ永続化されることを確認する。
4. 実X OAuth token exchangeを追加し、production mock callback/session発行禁止を維持したままlive credentialsで検証する。
5. stagingでpassした同一commitだけを`develop`から`main`へ昇格PRとして準備する。

Codexへのhandoffは、上記から1 sliceだけを選び、`feature/*`で実装、`develop`統合、staging検証、`main`昇格PR準備の順に書く。
