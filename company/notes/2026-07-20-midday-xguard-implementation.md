---
date: "2026-07-20"
project: "xguard"
type: midday-implementation
status: pr-updated
---

# 2026-07-20 XGuard 昼実装

## branch

- `feature/frontend-origin-separation`
- XGuard PR: `UryuAtsuya/Xguard#39`
- XGuard commit: `12ddda0`

## objective

顧客画面と管理画面の別entrypoint・別認証・別API権限の境界を、大小文字を変えたURLでも維持する。

## slice

Expressのroutingを大小文字区別に固定し、`/API/ADMIN/...` がadmin routeへ到達しながらcustomer CORS判定を受ける迂回を閉じた。

## review findings

- 修正済み: Expressの既定の大小文字非区別routingと、case-sensitiveなCORS audience判定が不整合だった。
- 追加findingなし。

## verification

- `npm run test -- --run backend/src/__tests__/adminAccess.test.ts`
- pass: 1 file / 10 tests
- `git diff --check`: pass

## PR / push

- `12ddda0` を `origin/feature/frontend-origin-separation` へpush済み。
- PR #39へfinding、修正、verificationを追記済み。

## blocker

- production deploy、Supabase schema適用、redirect URL登録、owner bootstrap、DNS接続は実値未確定のため未実施。

## 次の1手

PR #39のCI完了後、最終diff reviewを行い、staging Go/No-Goを判定する。
