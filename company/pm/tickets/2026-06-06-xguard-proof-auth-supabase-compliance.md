---
created: "2026-06-06"
project: "xguard"
assignee: "codex"
priority: high
status: push-blocked
handoff: "company/notes/2026-06-06-claude-code-codex-handoff.md"
handoff_at: "2026-06-06T12:45:00"
---

# XGuard proof auth / Supabase / compliance gate

## 内容

`/private/tmp/xguard-midday-2026-06-06-1331` で backup / proof APIの認証・所有権・visibility/revocation境界は `d5aa75e Guard backup proof ownership boundaries` として実装済み。pushはDNS `Could not resolve host: github.com` で未完。残りは実Supabase/Postgres検証、商用release gate docs、P2のowner management responseとHTTP境界テスト。

## 完了条件

- [x] `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で起点を確認する。
- [x] `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行し、失敗時は理由を記録する。Result: push時にDNS `Could not resolve host: github.com`。
- [x] backup / proof APIに認証済みuser境界を追加する。Evidence: XGuard `d5aa75e`
- [x] backup run / proof DTOでuser ownershipを強制する。Evidence: XGuard `d5aa75e`
- [x] private / revoked proofをAPIレスポンスから拒否または非公開化する。Evidence: XGuard `d5aa75e`
- [x] 他user backup/proof、private proof、revoked proof、存在しないrun idの拒否テストを追加する。Evidence: targeted Vitest pass
- [x] raw X API payload、token material、private/protected contentがproof DTOに混ざらないことを確認する。Evidence: private/revoked非公開境界とtargeted Vitest
- [ ] 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を確認する。
- [ ] `docs/API_COST_MODEL.md` にpay-per-usage、通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、月次上限前停止を反映する。
- [ ] `docs/COMPLIANCE.md` にEnterprise適用要否確認、24時間削除・変更追従、API access終了時の全削除runbookを反映する。
- [ ] P2: owner management responseとHTTP境界テストを整理する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、全test、build、`npm run check`, `git diff --cached --check` を実行する。Result: `tsc --noEmit`, targeted Vitest, full `npm run check`, `git diff --check`, `git diff --cached --check` pass。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。Blocked: `Could not resolve host: github.com`。
- [x] XGuardとMyLifeのcommit/push状態を分けて記録する。Evidence: `company/notes/2026-06-06-midday-xguard-implementation.md`

## 判断ルール

- v0 scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `Owned Reads` を複数顧客向けSaaSの原価前提にしない。
- `follows.read`, DM/write/follow系scope、自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は追加しない。
- 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-06` 系を使い、MyLife Vaultへproduction codeを置かない。今回の作業場所は `/private/tmp/xguard-midday-2026-06-06-1331`。

## 2026-06-06 昼run結果

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `NOT_WRITABLE`。Vaultへproduction codeを置かず、一時clone `/private/tmp/xguard-midday-2026-06-06-1331` で実装した。
- XGuard local commit: `d5aa75e Guard backup proof ownership boundaries`
- push: 未完了。`git push origin main` は `Could not resolve host: github.com`。
- 完了: backup / proof routeにprototype user header、owner check、private default proof、visibility更新、revoke、private/revoked非公開を追加。
- 完了: productionではprototype headerを拒否し、Supabase Auth/JWT + DB ownershipへ置き換えるまでbackup/proof routeをNo-Goにした。
- 完了: frontend contractを `proofPage.publicPayload` へ更新。
- 検証pass: `tsc --noEmit`, targeted Vitest, `npm run check`, `git diff --check`, `git diff --cached --check`。
- 未完了: 実Supabase/Postgres integration test、`docs/API_COST_MODEL.md`、`docs/COMPLIANCE.md`、GitHub push。

## 2026-06-06 17:00 朝会再実行後の更新

- 調査補強: X公式pricingではPost read `$0.005/resource`、User read `$0.010/resource`、`Owned Reads` はdeveloper app owner本人条件。XGuardの複数顧客原価は通常read単価で見積もる。
- 残Top 1: `d5aa75e` のpush。DNS復旧後、`git fetch` / remote先行確認をしてからpushする。
- 残Top 2: 実Supabase/Postgres integration test。実DB URL / `psql` がない場合はCIまたはwritable checkoutでの実行条件を明文化する。
- 残Top 3: `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` のrelease gate更新。
- 次の実装agentは、prototype user headerを本番認証と誤認しない。productionではSupabase Auth/JWT + DB ownershipへ置換するまでNo-Go。
