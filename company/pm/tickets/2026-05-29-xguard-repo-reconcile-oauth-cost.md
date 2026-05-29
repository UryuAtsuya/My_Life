---
created: "2026-05-29"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard repo reconcile / OAuth configured mode / cost evidence

## 内容

XGuard実装repoの指定パスと昨日の一時cloneを比較し、ledger実装の重複・未push分を整理したうえで、real OAuth configured modeとDeveloper Console原価確認を進める。

## 背景

- 2026-05-29朝run時点で `/Users/uryuatsuya/XGuard/xguard` は `exists=yes`, `writable=no`, `main...origin/main`, HEAD `455718c`。
- 指定パスには `455718c Add XGuard frontend prototype` と `c0a7dcd Add Supabase usage ledger repository boundary` がある。
- 昨日の一時clone `/private/tmp/xguard-midday-2026-05-28` は `main...origin/main [ahead 1]`, HEAD `9be85a1 Add Supabase API usage ledger repository`。
- `9be85a1` はremote先行/DNS問題で未pushだったが、指定パス側に近いledger実装が入っている可能性がある。
- Developer Console実値確認とreal OAuth configured mode確認が未完了のため、月額3,000円の原価判断とOAuth実利用の入口がまだ固定できない。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/remote HEADを昼run冒頭で確認する。
- [x] 指定パスの `455718c` がcached `origin/main` と一致していることを確認する。remote live確認はDNS失敗で未完了。
- [x] `/private/tmp/xguard-midday-2026-05-28` の `9be85a1` と指定パスの `c0a7dcd` を比較する。
- [x] `9be85a1` はそのまま取り込まず、未反映のproduction boundaryだけを `3120411` として整理する。
- [ ] real envを使って `/api/x/oauth/start` のconfigured modeを確認する。secret値はログやcompany文書に残さない。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check`, `git diff --cached --check` を実行する。
- [x] meaningfulなXGuard実装変更を `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。Evidence: `d30fc48 Harden Supabase usage ledger boundary`, push success。
- [x] MyLife側へ昼実装メモ、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。

## 2026-05-29 昼run結果

- 指定パス `/Users/uryuatsuya/XGuard/xguard`: `XGUARD_NOT_WRITABLE`。`git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可。
- 作業コピー: `/private/tmp/xguard-midday-2026-05-29-localref`
- XGuard local commit: `3120411 Harden Supabase usage ledger boundary`
- 実装: `record_api_usage_event_with_monthly_limit`、service-role専用実行、所有関係と同一Xアカウント検証、負値拒否、Supabase numeric string mapping。
- 検証: `npm ci`, `tsc --noEmit`, targeted Vitest（4 files / 34 tests）, `npm run check`（6 files / 37 tests）, `git diff --check`, `git diff --cached --check` pass。
- push: 未完了。`git push origin main` は `fetch first`、`git fetch origin main` / `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- 残: real OAuth configured mode、Developer Console原価確認、実Supabase/Postgres migration test。

## 2026-05-29 夜レビュー結果

- 指定パス `/Users/uryuatsuya/XGuard/xguard`: 夜runで `XGUARD_WRITABLE` / `.git writable` に回復。`git fetch origin main` 成功。
- remote先行: `d6b5b17 Add Supabase ledger cost-limit function`, `a40d4bf Translate docs to Japanese`。
- 判断: 昼runの `3120411` はそのままpushせず、remote先行分の上に必要差分だけを反映した。
- XGuard commit: `d30fc48 Harden Supabase usage ledger boundary`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- Push結果: 成功。`a40d4bf..d30fc48 main -> main`
- 夜run修正: SQL functionの所有関係検証、同一Xアカウント整合性、負値拒否、`service_role` grant、Supabase numeric string mapping、API cost model追記。
- 夜run検証: `git diff --check`, `tsc --noEmit`, targeted Vitest（1 file / 4 tests）, `npm run check`（6 files / 37 tests）, `git diff --cached --check` pass。
- 残: real OAuth configured mode、Developer Console原価確認、実Supabase/Postgres migration test。
