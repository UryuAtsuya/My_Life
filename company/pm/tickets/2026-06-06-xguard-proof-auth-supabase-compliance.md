---
created: "2026-06-06"
project: "xguard"
assignee: "codex"
priority: high
status: in-progress
handoff: "company/notes/2026-06-06-claude-code-codex-handoff.md"
handoff_at: "2026-06-06T12:45:00"
---

# XGuard proof auth / Supabase / compliance gate

## 内容

`/Users/uryuatsuya/XGuard/xguard` の `2b96993 Add OAuth state and PKCE guard` を起点に、backup / proof APIの認証・所有権・visibility/revocation境界を閉じ、実Supabase/Postgres検証と商用release gate docsを完了する。

## 完了条件

- [ ] `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で起点を確認する。
- [ ] `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行し、失敗時は理由を記録する。
- [ ] backup / proof APIに認証済みuser境界を追加する。
- [ ] backup run / proof DTOでuser ownershipを強制する。
- [ ] private / revoked proofをAPIレスポンスから拒否または非公開化する。
- [ ] 他user backup/proof、private proof、revoked proof、存在しないrun idの拒否テストを追加する。
- [ ] raw X API payload、token material、private/protected contentがproof DTOに混ざらないことを確認する。
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を確認する。
- [ ] `docs/API_COST_MODEL.md` にpay-per-usage、通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、月次上限前停止を反映する。
- [ ] `docs/COMPLIANCE.md` にEnterprise適用要否確認、24時間削除・変更追従、API access終了時の全削除runbookを反映する。
- [ ] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、実DB test、全test、build、`npm run check`, `git diff --cached --check` を実行する。実行できないものは環境理由を明記する。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [ ] XGuardとMyLifeのcommit/push状態を分けて記録する。

## 判断ルール

- v0 scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `Owned Reads` を複数顧客向けSaaSの原価前提にしない。
- `follows.read`, DM/write/follow系scope、自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は追加しない。
- 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-06` を使い、MyLife Vaultへproduction codeを置かない。
