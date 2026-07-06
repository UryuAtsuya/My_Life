---
date: "2026-07-06"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-07-06 週次 XGuard 計画

## 優先順位

XGuardを今週の最優先にする。production releaseはNo-Goを維持する。通常作業ブランチ、stagingともに`develop`を基準にし、実装は`feature/*`から`develop`へ統合する。staging検証後、同一commitを`develop`から`main`へ昇格PRで進める。`main`への直接実装pushは指示しない。

## Branch状態

- 現在checkout: `develop`
- 通常作業: `develop`
- staging: `develop`
- production: `main`
- `develop...origin/develop`: ahead 0 / behind 0
- `main...origin/main`: ahead 0 / behind 50
- local `develop`: `6e27294`
- `origin/develop`: `6e27294`
- local `main`: `030a916`
- `origin/main`: `7455cfa`
- PR #27 commit `31482ed` は `origin/develop` と `origin/main` に含まれる。
- 既存差分: `backend/src/repositories/oauthStateRepository.ts`, `backend/src/repositories/supabaseOAuthStateHttpStore.ts`, `.playwright-cli/`, `output/playwright/` は今回対象外として触らない。

## Blocker

- local `main` が `origin/main` より遅れているため、production branchのlocal確認前に同期が必要。
- `develop`上にOAuth state repository系の未コミット差分があるため、次の実装前に所有権とPR対象を確認する必要がある。
- PR #27 `feature/supabase-proof-page-transaction-store` はremote上で `develop` / `main` に含まれるが、実DB migration / RPC検証は未完了。
- `npm run check` は前回、標準timeoutで `frontend/src/App.test.tsx` 2件がtimeout。targeted extended testはpassしているが、標準check pass扱いにはしない。
- production昇格は、staging検証、実Supabase/Postgres integration evidence、OAuth live token exchange、runbookが揃うまでNo-Go。

## 今週の実装slice

1. `develop`上のOAuth state repository系未コミット差分の所有権を確認し、PR対象にするか分離するか決める。
2. Supabase/Postgres環境で `update_proof_page_visibility_and_record_content_compliance_event` RPC のmigration適用とtransaction保存を検証する。
3. `npm run check` の標準timeout失敗を、frontend test cleanup / wait / async handleの観点で恒久修正する。
4. OAuth live token exchange とproduction callback URLの確認をrunbook化し、mock callback/session発行禁止を維持する。
5. `origin/main` に入ったPR #27以降のproduction Go/No-Goを、staging evidence、実DB evidence、OAuth evidenceの3条件で判定する。

Codexへのhandoffは、上記から1 sliceだけを選び、`feature/*`で実装、`develop`統合、staging検証、`main`昇格PR準備の順に書く。
