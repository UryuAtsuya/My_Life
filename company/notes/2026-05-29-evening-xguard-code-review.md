---
date: "2026-05-29"
type: evening-code-review
project: xguard
status: completed
---

# 2026-05-29 XGuard 夜コードレビュー

## completed

- 確認時刻: `2026-05-29 18:43 JST`
- サブエージェント割当:
  - Review agent: `typescript-reviewer` に依頼したが、利用上限で失敗。
  - Verification agent: `default` に依頼したが、利用上限で失敗。
  - Documentation/Sync agent: メイン coordinator が実施。
  - Implementation agent: メイン coordinator が小修正のみ実施。
- 代替: サブエージェントは実行完了できなかったため、Review / Verification / Documentation-Sync / Implementation を順次ロール分担で実施した。
- 今日の正本: `/Users/uryuatsuya/XGuard/xguard`。夜run時点で writable に回復し、`origin/main` は `a40d4bf` までfetch済みだった。
- 昼runの `/private/tmp/xguard-midday-2026-05-29-localref` `3120411` をそのままpushせず、remote先行分 `d6b5b17`, `a40d4bf` の上に必要差分だけを反映した。
- XGuard commit: `d30fc48 Harden Supabase usage ledger boundary`
- XGuard push先: `UryuAtsuya/Xguard` `origin/main`

## unfinished

- real OAuth configured mode の実env確認は未完了。secret値を扱うため、明日、ログに残さない手順で確認する。
- Developer Consoleでのendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件の実画面確認は未完了。
- 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の権限、所有関係、月次上限超過、負値拒否を確認する作業は未完了。

## findings

1. P1: 昼runの production boundary がremote先行分に完全には入っていなかった。`supabase/schema.sql` の `record_api_usage_event_with_monthly_limit` は月次上限だけを見ており、`x_account_id` / `backup_run_id` の所有関係、同一Xアカウント整合性、負値拒否、`service_role` grant が不足していた。
2. P1: Supabase `numeric` が string で返る場合、`estimated_cost_usd` がdomain DTOでnumberにならない可能性があった。backup-run rollupやcost比較で型境界が崩れるリスクがある。
3. P1: Developer Console実値が未確認のため、月額3,000円モデルの原価判断はまだ確定扱いにできない。`Owned Reads` discount も第三者SaaS適用確認までは主前提にしない。
4. P2: real OAuth configured mode が未確認のため、`X_CLIENT_ID` 設定時の入口は実envでの疎通証拠がない。scopeは `tweet.read`, `users.read`, `offline.access` のまま維持されている。

## fixes applied

- `supabase/schema.sql`:
  - `record_api_usage_event_with_monthly_limit` に `x_account_id` 所有者検証を追加。
  - `backup_run_id` が同じuserかつ同じXアカウントに属することを検証。
  - `resource_count`, `rate_limit_limit`, `rate_limit_remaining`, `estimated_cost_usd` の負値拒否を追加。
  - `public`, `anon`, `authenticated` から `revoke all` し、`service_role` だけに `grant execute`。
- `backend/src/repositories/supabaseApiUsageLedgerRepository.ts`:
  - Supabase `numeric` の `number | string` を受け、domain DTOでは `Number(...)` に揃える。
- `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`:
  - Supabase numeric string返却時も `estimatedCostUsd` がnumberになるテストを追加。
- `docs/API_COST_MODEL.md`:
  - 2026-05-29 production boundary follow-upを追記。

## proposed fixes

- 実Supabase/PostgresでSQL functionのmigration testを追加し、`service_role` だけが実行できること、`authenticated` では実行不可であることを確認する。
- real OAuth configured modeをsecret非表示で確認し、`/api/x/oauth/start` のconfigured URL、scope、callback URLだけを証跡化する。
- Developer Console実値を `docs/API_COST_MODEL.md` に転記し、保守単価と確定単価を分ける。

## verification

- `git diff --check`: pass
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npx vitest run --configLoader runner backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`: pass（1 file / 4 tests）
- `npm run check`: pass（build pass、Vitest 6 files / 37 tests）
- `git diff --cached --check`: pass
- `git push -v origin main`: pass。`a40d4bf..d30fc48 main -> main`

## tomorrow handoff

1. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` のservice-role権限、所有関係、月次上限超過、負値拒否を確認する。
2. real OAuth configured modeをsecret非表示で確認し、scopeが `tweet.read`, `users.read`, `offline.access` のままかを証跡化する。
3. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` とcompany記録へ反映する。

## subagent findings

- Review agent: 利用上限で完了できず。メイン coordinator がレビュー観点を引き継いだ。
- Verification agent: 利用上限で完了できず。メイン coordinator が検証コマンドを実行した。
- Documentation/Sync agent: メイン coordinator が実施した。
- Implementation agent: メイン coordinator が小修正のみ実施した。
