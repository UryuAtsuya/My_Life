---
created: "2026-05-27"
project: "xguard"
assignee: "codex"
priority: high
status: planned
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

- [ ] `/Users/uryuatsuya/XGuard/xguard` の書き込み可否を昼run冒頭で確認する。
- [ ] 書き込み可能なら、指定パスを `origin/main` `c7a315c` 以降へ同期する。
- [ ] 書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-27` の一時cloneで作業する。
- [ ] `backend/src/services/apiUsageLedger.ts` に非負整数validationを追加する。
- [ ] `backend/src/__tests__/apiUsageLedger.test.ts` に負値、小数、`NaN`、`Infinity` の失敗テストを追加する。
- [ ] Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [ ] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を実行する。
- [ ] meaningfulなXGuard実装変更を `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] MyLife側へ昼実装メモとcommit hashを報告する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
