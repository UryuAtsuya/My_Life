---
created: "2026-05-27"
project: "xguard"
assignee: "codex"
priority: high
status: partial
---

# XGuard specified path sync / ledger validation / cost evidence

## 内容

XGuard指定パスをpush済み正本へ同期し、`ApiUsageLedgerService` の入力validationを固め、Developer Console実値をcost modelへ反映する。

## 背景

- 2026-05-26昼runは `/private/tmp/xguard-midday-2026-05-26` で実装し、`c7a315c Add API usage ledger contract` を `UryuAtsuya/Xguard` `origin/main` へpush済み。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は2026-05-27朝run時点でも `writable=no`。
- 指定パスGit状態は `main...origin/main [ahead 4, behind 2]`。
- 夜レビューで `ApiUsageLedgerService` に負値・小数入力を拒否するvalidationと失敗テストが次の小修正として残った。
- Developer Console実値確認が未完了のため、月額3,000円の原価判断を固定できない。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` の書き込み可否を昼run冒頭で確認する。
- [ ] 書き込み可能なら、指定パスを `origin/main` `c7a315c` 以降へ同期する。
- [x] 書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-27` の一時cloneで作業する。
- [x] `backend/src/services/apiUsageLedger.ts` に非負整数validationを追加する。
- [x] `backend/src/__tests__/apiUsageLedger.test.ts` に負値、小数、`NaN`、`Infinity` の失敗テストを追加する。
- [ ] Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を実行する。
- [x] meaningfulなXGuard実装変更を `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [x] MyLife側へ昼実装メモとcommit hashを報告する。

## 2026-05-27 昼run結果

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `NOT_WRITABLE`。作業ツリーに未解決conflictあり。
- 実装場所: `/private/tmp/xguard-midday-2026-05-27`
- XGuard commit: `3528e26 Validate API usage ledger inputs`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 検証: `npm ci`, `./node_modules/.bin/tsc -p tsconfig.json --noEmit`, `./node_modules/.bin/vitest run --configLoader runner`（4 files / 29 tests）, `npm run check`, `git diff --check`, `git diff --cached --check` はpass。
- 未完了: Developer Console実画面確認、指定パス自体の同期、Supabase transaction repository化。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
