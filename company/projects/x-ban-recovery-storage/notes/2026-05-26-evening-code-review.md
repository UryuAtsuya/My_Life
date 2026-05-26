---
created: "2026-05-26"
project: "xguard"
type: evening-code-review
status: specified-path-sync-blocked
---

# 2026-05-26 XGuard 夜レビュー要約

## 今日の実装repo状態

- Canonical pushed workspace: `/private/tmp/xguard-midday-2026-05-26`
- Pushed HEAD: `c7a315c Add API usage ledger contract`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 指定パス: `/Users/uryuatsuya/XGuard/xguard`
- 指定パスlocal HEAD: `0991eeb Add API usage ledger contract`
- 指定パスtracking `origin/main`: `ba98160 Document minimum OAuth scope`
- 指定パス状態: `main...origin/main [ahead 3]`, `XGUARD_NOT_WRITABLE`, `.git`も `XGUARD_GIT_NOT_WRITABLE`

## レビュー結論

昼のpush済みコードは検証上green。`ApiUsageLedgerService` とmock backupのledger接続は入っており、`npm run check` も通った。

ただし、指定パスcheckoutはまだpush済み一時cloneと同期できていない。明日は新規機能を広げる前に、指定パスをGitHub `origin/main` の `c7a315c` 以降へ揃え、次回レビュー対象を一本化する。

## 主要指摘

1. P0: 指定パスcheckoutがpush済み状態と同期していない。
   - Status: blocked by workspace write permission and DNS failure for live remote check.
2. P1: usage ledgerに負値・小数入力を拒否するvalidationとテストがない。
   - Status: proposed fix for tomorrow.
3. P1: Developer Console実値が未確認。
   - Status: carry over.
4. P1: Supabase transaction repositoryと `monthly_api_cost_limit_usd` stop ruleは未実装。
   - Status: next implementation boundary.
5. P2: Stripe webhook冪等handlerは未実装。
   - Status: after ledger persistence.

## 検証

- `npm run check`: pass, 4 files / 9 tests
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner`: pass, 4 files / 9 tests
- `git diff --check && git diff --cached --check`: pass
- `git ls-remote origin refs/heads/main`: fail, `Could not resolve host: github.com`

## 明日

1. `/Users/uryuatsuya/XGuard/xguard` を `origin/main` `c7a315c` 以降へ同期する。
2. `ApiUsageLedgerService` の非負整数validationと失敗テストを追加する。
3. Developer Console実値確認後、Supabase transaction repositoryと月次上限stop ruleへ進む。
