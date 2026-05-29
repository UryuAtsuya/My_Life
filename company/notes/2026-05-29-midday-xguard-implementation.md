---
date: "2026-05-29"
type: midday-implementation
project: xguard
---

# 2026-05-29 XGuard 昼実装

## 結論

指定パス `/Users/uryuatsuya/XGuard/xguard` は今日も `XGUARD_NOT_WRITABLE` で、`git fetch origin main` も `.git/FETCH_HEAD` 書き込み不可だった。Vaultへ実装コードを置かず、指定パスのローカル `origin/main` `455718c` を元に `/private/tmp/xguard-midday-2026-05-29-localref` を作って実装した。

昨日の未push `9be85a1` はそのまま取り込まず、`455718c` / `c0a7dcd` に未反映だった production boundary の安全化だけを `3120411 Harden Supabase usage ledger boundary` として切った。pushは `fetch first` で拒否され、fetch/ls-remoteは `Could not resolve host: github.com` のため未完了。

## サブエージェント担当

- Implementation agent: 実エージェントを起動したが時間内に完了しなかったため、メイン調整役が同じスコープを直接実装した。
- Review agent: 実エージェントで2回実施。v0 scope維持、ledger実装分岐、`security definer` 公開リスク、`x_account_id` / `backup_run_id` 整合性不足を指摘。
- Verification agent: 実エージェントで検証コマンドと対象テストを確認。
- Documentation/Sync agent: 実エージェントでMyLife同期先と記録項目を確認。

## 実装内容

- `supabase/schema.sql` に `public.record_api_usage_event_with_monthly_limit` を追加した。
- `user_profiles` を `for update` でロックし、当月 `api_usage_events.estimated_cost_usd` 合計が `monthly_api_cost_limit_usd` を超える場合はinsert前に拒否する。
- `x_account_id` と `backup_run_id` が同じユーザーかつ同じXアカウントに属することをDB関数内で検証する。
- `security definer` 関数は `service_role` のみ実行可とし、`public`, `anon`, `authenticated` からは実行権限を剥がした。
- DB境界でも `resourceCount`, rate-limit counters, `estimatedCostUsd` の負値を拒否する。
- Supabase `numeric` が文字列として返る場合に備え、repository mappingで `estimated_cost_usd` を `Number(...)` に変換する。
- `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts` に numeric string mapping のテストを追加した。
- `docs/API_COST_MODEL.md` に2026-05-29のproduction boundary追記を入れた。

## Review agent の主要指摘と対応

- 指摘: v0 scopeが広がっていないか確認。対応: `tweet.read`, `users.read`, `offline.access` のまま。追加scopeなし。
- 指摘: `9be85a1` と `c0a7dcd` はledger境界が分岐しており、単純mergeは危険。対応: 既存TS `runInTransaction` interfaceは崩さず、DB関数とmapping補強だけを採用。
- 指摘: `security definer` 関数の公開リスク。対応: `REVOKE` / `GRANT service_role` と所有関係検証を追加。
- 指摘: `x_account_id` と `backup_run_id` の相互整合性不足。対応: `backup_runs.x_account_id = p_x_account_id` を関数内で必須化。
- 指摘: SQL境界で負の利用量・負のコストを拒否していない。対応: DB関数内で負値を拒否。
- 残指摘: 実Supabase/Postgres migration testは未追加。ローカル環境に実DBがないため夜以降のTODOに回す。

## Verification agent の検証結果

- `npm ci`: pass
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner backend/src/__tests__/apiUsageLedger.test.ts backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts backend/src/__tests__/api.test.ts backend/src/__tests__/tokenRepository.test.ts`: pass（4 files / 34 tests）
- `npm run check`: pass（6 files / 37 tests）
- `git diff --check`: pass
- `git diff --cached --check`: pass

## Git状態

- XGuard作業ディレクトリ: `/private/tmp/xguard-midday-2026-05-29-localref`
- XGuard local commit: `3120411 Harden Supabase usage ledger boundary`
- 反映先予定: `UryuAtsuya/Xguard` `origin/main`
- push結果: 未push。`git push origin main` は `fetch first` で拒否。`git fetch origin main` と `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com` で失敗。
- 指定パス: `/Users/uryuatsuya/XGuard/xguard` は `XGUARD_NOT_WRITABLE`、HEAD / cached `origin/main` は `455718c`。

## 未完了

- remote先行分をfetchして `3120411` をrebase/mergeし、`UryuAtsuya/Xguard` `origin/main` へpushすること。
- real OAuth configured mode確認。
- Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、実値を `docs/API_COST_MODEL.md` へ入れること。
- 実Supabase/Postgresで `record_api_usage_event_with_monthly_limit` の権限、上限超過、所有関係、負値拒否を検証すること。

## 夜レビューへ送るTODO

1. GitHub DNSが通る環境で `origin/main` をfetchし、remote先行分へ `3120411` をrebase/mergeしてpushする。
2. 実Supabase/Postgres migration testを追加し、service-role専用実行、所有関係検証、月次上限超過、負値拒否を確認する。
3. real OAuth configured modeとDeveloper Console原価確認を実施し、`docs/API_COST_MODEL.md` とcompany記録へ実値を同期する。
