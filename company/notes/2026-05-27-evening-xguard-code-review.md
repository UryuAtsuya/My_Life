---
date: "2026-05-27"
project: "xguard"
type: evening-code-review
status: completed
---

# 2026-05-27 XGuard 夜コードレビュー

## completed

- システム日付を `2026-05-27 18:02:34 JST (+0900)` と確認した。
- 今日の昼実装メモ、PMチケット、decision、XGuard planning files、MyLife/XGuard双方のGit状態を確認した。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は読み取り可能だが、`test -w` は `not_writable`。`.git/FETCH_HEAD` も `Operation not permitted` で更新できない。
- push済み正本 `/private/tmp/xguard-midday-2026-05-27` は `3528e26 Validate API usage ledger inputs` で、`UryuAtsuya/Xguard` `origin/main` へ反映済み。夜runの `git push -v origin main` は `Everything up-to-date`。
- 昨日の主要指摘だった `ApiUsageLedgerService` の非負整数validationは、push済み正本で実装・検証済み。

## unfinished

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `main...origin/main [ahead 1]`、HEAD `e750d04 Validate API usage ledger quantities` のまま。push済み正本 `3528e26` とは完全一致していない。
- Developer Consoleでのendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件の実画面確認は未完了。
- `ApiUsageLedgerService` はまだin-memory repository。Supabase transaction repository化と `monthly_api_cost_limit_usd` 超過前停止は未実装。

## findings

1. P0: 指定パスのlocal commit `e750d04` は、push済み正本 `3528e26` と同一内容ではない。`docs/API_SPEC.md` のvalidation追記が欠け、`docs/API_COST_MODEL.md` / `docs/ARCHITECTURE.md` の説明と失敗テストの網羅も正本より薄い。指定パスからそのままpushすると、remote正本と履歴・内容が再分岐する。
2. P1: API原価の実値がDeveloper Console未確認のため、月額3,000円の利益率、spending limit、Owned Reads前提を確定できない。現状は保守的な通常read単価を実装デフォルトにする判断を維持する。
3. P1: Supabase repository化前に、`api_usage_events` insertと `backup_runs` rollupを同一transactionへ閉じる設計が必要。今のin-memory prototypeだけでは、途中失敗時の二重記録・rollup欠落・月次上限超過前停止を検証できない。
4. P2: 指定パスはbuild output `dist/` へ書き込めないため、同パスでの `npm run check` は環境要因で失敗する。通常検証は一時checkoutまたは権限復旧後の指定パスで行う。

## fixes applied

- 夜runではXGuard実装コードへ追加修正は入れていない。
- push済み正本 `/private/tmp/xguard-midday-2026-05-27` で `npm run check` を再実行し、`3528e26` が検証済みであることを確認した。
- 指定パスの `e750d04` は正本との差分があるため、pushせず同期課題として残した。

## proposed fixes

1. 書き込み可能な環境で `/Users/uryuatsuya/XGuard/xguard` を `origin/main` `3528e26` へ揃える。`e750d04` は正本に対する重複・不足commitとして扱い、必要なら破棄ではなく差分確認後に正本へ合わせる。
2. Developer Console実画面からendpoint別単価、monthly spending limit、Usage API可否、Owned Reads条件を `docs/API_COST_MODEL.md` とcompany gateへ転記する。
3. `SupabaseApiUsageLedgerRepository` を作り、`backup_runs` 作成、`api_usage_events` 追加、summary rollup、月次API原価上限チェックをtransactionで扱う。

## verification

| Command | Path | Result |
|---|---|---|
| `date '+%Y-%m-%d %H:%M:%S %Z (%z)'` | MyLife | pass: `2026-05-27 18:02:34 JST (+0900)` |
| `git status --short --branch` | MyLife | pass: `main...origin/main`。未追跡Vault noiseのみ |
| `git status --short --branch` | `/Users/uryuatsuya/XGuard/xguard` | pass: `main...origin/main [ahead 1]` |
| `test -w /Users/uryuatsuya/XGuard/xguard` | MyLife | blocked: `not_writable` |
| `git fetch origin main` | `/Users/uryuatsuya/XGuard/xguard` | blocked: `.git/FETCH_HEAD` が `Operation not permitted` |
| `git diff --check` | `/Users/uryuatsuya/XGuard/xguard` | pass |
| `./node_modules/.bin/tsc -p tsconfig.json --noEmit` | `/Users/uryuatsuya/XGuard/xguard` | pass |
| `./node_modules/.bin/vitest run --configLoader runner` | `/Users/uryuatsuya/XGuard/xguard` | pass: 4 files / 11 tests |
| `npm run check` | `/Users/uryuatsuya/XGuard/xguard` | fail: `dist/` 書き込み `EPERM` |
| `git diff --check` | `/private/tmp/xguard-midday-2026-05-27` | pass |
| `./node_modules/.bin/tsc -p tsconfig.json --noEmit` | `/private/tmp/xguard-midday-2026-05-27` | pass |
| `./node_modules/.bin/vitest run --configLoader runner` | `/private/tmp/xguard-midday-2026-05-27` | pass: 4 files / 29 tests |
| `npm run check` | `/private/tmp/xguard-midday-2026-05-27` | pass: build + vitest 4 files / 29 tests |
| `git push -v origin main` | `/private/tmp/xguard-midday-2026-05-27` | pass: `Everything up-to-date` |
| `git diff --check` | MyLife | pass |

## tomorrow handoff

1. P0: `/Users/uryuatsuya/XGuard/xguard` をpush済み正本 `3528e26` へ同期する。`e750d04` はそのままpushしない。
2. P1: Developer Console実画面でX API単価、spending limit、Usage endpoint、Owned Reads条件を確認し、XGuard docsとcompany gateへ反映する。
3. P1: `SupabaseApiUsageLedgerRepository` と月次API原価上限の超過前停止を実装する。
