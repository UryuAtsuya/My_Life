---
created: "2026-05-26"
project: "xguard"
assignee: "codex"
priority: high
status: completed
---

# XGuard remote sync / validation recovery / cost ledger

## 内容

XGuard指定パスとremoteの分岐を解消し、TypeScript検証を復旧した上で、X API usage/cost ledgerの最小contractを入れる。

## 背景

- 朝run確認では `/Users/uryuatsuya/XGuard/xguard` は存在するが `writable=no`。
- 指定パスのGit状態は `main...origin/main [ahead 2]`。
- 前日昼のpush済みcommitは `b3bd37c Add token repository contract and docs gates`。
- 前日夜の指定パスlocal HEADは `91229db Exclude revoked token refs`。
- `npx tsc -p tsconfig.json --noEmit` は `tokenRepository.test.ts` のmock fetch型不一致で失敗していた。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` の書き込み可否を昼run冒頭で確認する。Evidence: `NOT_WRITABLE`
- [x] 書き込み不可なら `/private/tmp/xguard-midday-2026-05-26` の一時cloneで作業する。Evidence: temp clone作成
- [x] remote `b3bd37c` とlocal `f60be3e`/`91229db` 相当の差分を統合し、`origin/main` へpushする。Evidence: `c7a315c Add API usage ledger contract`, push success
- [x] `backend/src/__tests__/tokenRepository.test.ts` のmock fetch型を修正する。Evidence: 現行 `origin/main` 側の分割repository構成で `tsc --noEmit` passへ復旧
- [x] `SupabaseTokenRepository.findXToken()` のread pathで `assertReadOnlyXScopes(row.scope)` を呼ぶ。Evidence: `backend/src/repositories/supabaseTokenRepository.ts`
- [x] `backup_runs` + `api_usage_events` transaction serviceまたは最小contractを追加する。Evidence: `backend/src/services/apiUsageLedger.ts`
- [x] `docs/API_COST_MODEL.md` にDeveloper Console確認値、spending limit、Usage endpoint確認結果または未確認理由を追記する。Evidence: 実画面未確認理由、保守的read単価、Owned Reads保留を追記
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を実行する。Evidence: `git diff --check` pass, `./node_modules/.bin/tsc -p tsconfig.json --noEmit` pass, `./node_modules/.bin/vitest run --configLoader runner` pass, `npm run check` pass

## 昼run完了メモ

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は引き続き `NOT_WRITABLE`。実装は `/private/tmp/xguard-midday-2026-05-26` で行った。
- XGuard commit: `c7a315c Add API usage ledger contract`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 実装範囲: scope再検査、usage/cost ledger最小contract、mock backupへのusage event接続、docs更新。
- 残り: 指定パスの権限解消と `c7a315c` 同期、Developer Console実値確認、Supabase transaction repository化、Stripe webhook冪等化。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
