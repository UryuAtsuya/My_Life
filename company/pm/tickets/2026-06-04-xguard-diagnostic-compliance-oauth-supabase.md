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
- [ ] backup / proof APIに認証、user ownership、proof visibility/revocation境界を追加する。
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

## 2026-06-04 evening update

- [x] 指定パスの確定状態は `HEAD=origin/main=394a3c3 Add OAuth diagnostic HTTP boundary tests`、working tree clean。
- [x] 診断endpointの無認証公開は解消済み。昼記録の `e31510b` 未push状態は、指定パスへ統合済みの `fe4b13f` を正として訂正する。
- [x] 診断endpointの `supertest` HTTP境界2件とAPI仕様の認証列を `394a3c3` として `UryuAtsuya/Xguard` `origin/main` へpushした。
- [x] `git diff --check`, `git diff --cached --check`, `tsc --noEmit`, `npm run test` はpass。全testは `50 passed / 4 skipped`。
- [ ] `npm run build` / `npm run check` は `dist/backend/...` write `EPERM`。
- [ ] Review P1: OAuth CSRF/replay防止、backup/proof認証・所有権、実DB、商用compliance gate。
- [ ] production releaseはNo-Goを維持する。
