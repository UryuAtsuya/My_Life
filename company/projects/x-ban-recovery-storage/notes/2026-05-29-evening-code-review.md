---
date: "2026-05-29"
project: "x-ban-recovery-storage"
type: evening-code-review
status: completed
---

# 2026-05-29 XGuard 夜レビュー

## 結論

夜runで `/Users/uryuatsuya/XGuard/xguard` が writable に回復し、GitHub fetch/push も通った。昼runの `3120411` はそのままpushせず、remote先行の `a40d4bf` の上に必要差分だけを反映し、`d30fc48 Harden Supabase usage ledger boundary` として `UryuAtsuya/Xguard` `origin/main` へpushした。

## 反映した内容

- Supabase SQL function `record_api_usage_event_with_monthly_limit` をservice-role実行境界として強化。
- `x_account_id` / `backup_run_id` の所有関係と同一Xアカウント整合性をDB境界で検証。
- 負の利用量、負のrate-limit counter、負の推定原価をDB境界でも拒否。
- Supabase `numeric` がstringで返る場合もdomain DTOではnumberへ変換。
- `docs/API_COST_MODEL.md` に2026-05-29 production boundary follow-upを追記。

## レビュー指摘

1. P1: SQL functionの所有関係検証と負値拒否がremote先行分に不足していた。夜runで修正済み。
2. P1: Supabase `numeric` string返却時の型境界が曖昧だった。夜runで修正済み。
3. P1: Developer Console原価実値は未確認。価格・spending・Owned Reads条件は明日も未完了の最重要確認。
4. P2: real OAuth configured modeは未確認。secret非表示でconfigured URLとscopeだけを証跡化する。

## 検証

- `git diff --check`: pass
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npx vitest run --configLoader runner backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`: pass（1 file / 4 tests）
- `npm run check`: pass（build pass、Vitest 6 files / 37 tests）
- `git diff --cached --check`: pass
- `git push -v origin main`: pass。`a40d4bf..d30fc48 main -> main`

## 次

1. 実Supabase/Postgres migration testでSQL functionの権限、所有関係、月次上限超過、負値拒否を確認する。
2. real OAuth configured modeをsecret非表示で確認する。
3. Developer Console原価実値を確認し、`docs/API_COST_MODEL.md` とPM ticketへ反映する。
