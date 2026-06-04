---
created: "2026-06-04"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard diagnostic / compliance / OAuth / Supabase gate

## 内容

`/Users/uryuatsuya/XGuard/xguard` の `6024667 Restrict production CORS origins` を起点に、診断endpoint制限、実Supabase/Postgres integration test、OAuth安全化、商用compliance gateを閉じる。

## 完了条件

- [x] `deployment_diagnostic` 有効時の `/api/x/oauth/status` を32文字以上のheader secret必須に限定する。
- [x] `/api/x/oauth/status` の無効、token未設定、header欠落、不一致、成功をHTTPテストとsandbox fallbackで確認する。
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を確認する。
- [ ] OAuth configured modeの一回限り `state`、S256 PKCE、callback validationを実装する。
- [ ] token repositoryとSupabase schemaの保存契約を一本化する。
- [ ] `docs/API_COST_MODEL.md` に通常read単価、`Owned Reads` 非適用、Usage、spending limitを反映する。
- [ ] `docs/COMPLIANCE.md` にEnterprise適用要否確認、24時間削除・変更追従、API access終了時の全削除runbookを反映する。
- [ ] `git diff --check`, `tsc`, targeted Vitest、実DB test、全test、build、`npm run check`, `git diff --cached --check` を実行する。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] XGuardとMyLifeのcommit/push状態を分けて記録する。

## 判断ルール

- v0 scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `Owned Reads` を複数顧客向けSaaSの原価前提にしない。
- `follows.read`, DM/write/follow系scope、自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は追加しない。
- 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-04` を使い、MyLife Vaultへproduction codeを置かない。

## 2026-06-04 midday update

- [x] `/private/tmp/xguard-midday-2026-06-04-UdD2dZ` で診断endpointのheader secret gateを実装した。
- [x] 32文字未満の診断tokenをruntime config errorで拒否し、SHA-256 digestと `timingSafeEqual` で比較する。
- [x] 成功・拒否responseの両方へ `Cache-Control: no-store` を追加した。
- [x] 最終ReviewはP0/P1/P2なし。`npm run check` はpass。
- [ ] XGuard commit `e31510b Guard OAuth deployment diagnostic` はDNS解決失敗で未push。force pushしない。
- [ ] 実Supabase/Postgres、OAuth安全化、token schema、cost/compliance docsは未完了。
