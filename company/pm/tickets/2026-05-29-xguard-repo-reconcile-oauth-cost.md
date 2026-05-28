---
created: "2026-05-29"
project: "xguard"
assignee: "codex"
priority: high
status: open
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

- [ ] `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/remote HEADを昼run冒頭で確認する。
- [ ] 指定パスの `455718c` がremote最新か、localのみかを確認する。
- [ ] `/private/tmp/xguard-midday-2026-05-28` の `9be85a1` と指定パスの `c0a7dcd` を比較する。
- [ ] `9be85a1` の未反映分があれば、remote最新へrebase/mergeして取り込む。重複なら明示的にclose判断する。
- [ ] real envを使って `/api/x/oauth/start` のconfigured modeを確認する。secret値はログやcompany文書に残さない。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [ ] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check`, `git diff --cached --check` を実行する。
- [ ] meaningfulなXGuard実装変更を `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] MyLife側へ昼実装メモ、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
