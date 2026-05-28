---
created: "2026-05-28"
project: "xguard"
assignee: "codex"
priority: high
status: open
---

# XGuard specified path sync / cost evidence / Supabase ledger

## 内容

XGuard指定パスをpush済み正本へ同期し、Developer Console実値をcost modelへ反映し、API usage ledgerをSupabase transaction repositoryへ進める。

## 背景

- 2026-05-27昼runは `/private/tmp/xguard-midday-2026-05-27` で実装し、`3528e26 Validate API usage ledger inputs` を `UryuAtsuya/Xguard` `origin/main` へpush済み。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は2026-05-28朝runでも `writable=no`。
- 指定パスGit状態は `main...origin/main [ahead 1]`、HEAD `e750d04`。local `e750d04` は正本 `3528e26` と完全一致しないため、そのままpushしない。
- Developer Console実値確認が未完了のため、月額3,000円の原価判断を固定できない。
- 次の実装はin-memory ledgerからSupabase transaction repositoryへ移す。

## 完了条件

- [ ] `/Users/uryuatsuya/XGuard/xguard` の書き込み可否を昼run冒頭で確認する。
- [ ] 書き込み可能なら、指定パスを `origin/main` `3528e26` 以降へ同期する。
- [ ] 書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-28` の一時cloneで作業する。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [ ] `backend/src/repositories/supabaseApiUsageLedgerRepository.ts` を追加する。
- [ ] `api_usage_events` 記録、`backup_runs` rollup、`monthly_api_cost_limit_usd` 超過前停止をtransactionで検証する。
- [ ] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を実行する。
- [ ] meaningfulなXGuard実装変更を `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] MyLife側へ昼実装メモとcommit hashを報告する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
