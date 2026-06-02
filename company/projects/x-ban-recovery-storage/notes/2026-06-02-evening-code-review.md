---
date: "2026-06-02"
project: "xguard"
type: project-evening-code-review
status: reviewed
---

# 2026-06-02 夜レビュー

## 結論

XGuard指定パス `/Users/uryuatsuya/XGuard/xguard` は夜run最終状態で `HEAD=origin/main=95e6392`、working tree clean。昼の `backup_run_id` / `x_account_id` 境界修正系列は `86a71fb` と `8aa0910` をmergeした `95e6392` に統合された。

ただし live GitHubの独立確認はDNS失敗で未完了。実Supabase/Postgres integration test、OAuth configured mode安全化、Developer Console原価確認も未完了のため、release gateは閉じない。

## レビュー結果

- P0: なし。
- P1: `/api/x/oauth/status` が無認証で設定状態を返すため、productionではadmin-onlyまたはdeployment-onlyへ寄せる。
- P1: OAuth configured modeは静的 `state`、plain/mock PKCE、callback未照合。
- P1: token repositoryとSupabase schemaの保存契約が未統一。
- P2: 実DB integration test未実行。
- P2: OAuth status testがExpress内部構造に依存。
- P2: CORSが全許可。

## Git状態

- XGuard HEAD: `95e6392 Merge remote-tracking branch 'origin/main'`
- local `origin/main`: `95e6392`
- remote origin: `https://github.com/UryuAtsuya/Xguard.git`
- `git ls-remote`: `Could not resolve host: github.com`
- `git fetch origin main`: `.git/FETCH_HEAD: Operation not permitted`

## 未完了

- live remote HEADの再確認。
- 実Supabase/Postgres integration test。
- OAuth state / S256 PKCE / callback validation。
- token repositoryとSupabase schema契約の一本化。
- Developer Console原価実値確認。

## 次

1. DNS/権限が通る環境で `95e6392` が `UryuAtsuya/Xguard` `main` に存在するか確認する。
2. 実DB credentialを入れてSQL integration testを走らせる。
3. OAuth production blockerを先に閉じる。
