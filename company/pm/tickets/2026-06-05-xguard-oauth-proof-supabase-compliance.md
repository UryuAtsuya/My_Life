---
created: "2026-06-05"
project: "xguard"
assignee: "codex"
priority: high
status: in-progress
---

# XGuard OAuth / proof ownership / Supabase / compliance gate

## 内容

`/Users/uryuatsuya/XGuard/xguard` の `394a3c3 Add OAuth diagnostic HTTP boundary tests` を起点に、OAuth configured modeのCSRF/replay防止、backup / proof APIの認証・所有権境界、実Supabase/Postgres検証、商用compliance gateを閉じる。

## 完了条件

- [ ] `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で `394a3c3` 起点を確認する。
- [ ] `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行し、失敗時は理由を記録する。
- [ ] OAuth configured modeで一回限り `state`、S256 PKCE、callback validation、TTL、replay防止を実装する。
- [ ] forged / expired / replay callback、scope維持、token material非返却のHTTP境界テストを追加する。
- [ ] backup / proof APIに認証、user ownership、proof visibility/revocation境界を追加する。
- [ ] 他user backup/proof、private proof、revoked proofの拒否テストを追加する。
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を確認する。
- [ ] `docs/API_COST_MODEL.md` に通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、月次上限前停止を反映する。
- [ ] `docs/COMPLIANCE.md` にEnterprise適用要否確認、24時間削除・変更追従、API access終了時の全削除runbookを反映する。
- [ ] `git diff --check`, `tsc`, targeted Vitest、実DB test、全test、build、`npm run check`, `git diff --cached --check` を実行する。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] XGuardとMyLifeのcommit/push状態を分けて記録する。

## 昼実装フォーカス（12:45 handoff）

**昼は Top 1 のみに集中する。** 詳細指示は下記を参照。

- 実装指示書: `company/notes/2026-06-05-claude-code-codex-handoff.md`
- 理由: OAuth CSRF/replay 防止は P1 セキュリティ要件であり、Top 2 backup/proof 認証の前提になる。

## 判断ルール

- v0 scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `Owned Reads` を複数顧客向けSaaSの原価前提にしない。
- `follows.read`, DM/write/follow系scope、自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は追加しない。
- 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-05` を使い、MyLife Vaultへproduction codeを置かない。
