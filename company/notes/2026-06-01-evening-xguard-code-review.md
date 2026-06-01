---
date: "2026-06-01"
project: "xguard"
type: evening-code-review
status: completed_with_push
---

# 2026-06-01 XGuard 夜レビュー

## completed

- 日付確認: `2026-06-01 18:01:23 JST (+0900)`。
- サブエージェントは実利用した。Review agent、Verification agent、Documentation/Sync agentを並列起動し、Coordinatorが最終判断、修正採用、commit/push、MyLife同期を担当した。
- 正本は `/Users/uryuatsuya/XGuard/xguard`、反映先は `UryuAtsuya/Xguard` `https://github.com/UryuAtsuya/Xguard.git`。
- 前回未push扱いだった `2655267 Filter revoked tweet snapshots from proof DTO` は、今日の確認時点で `main` 履歴に含まれていた。
- 今日の昼run成果は `4e6258c Merge remote-tracking branch 'origin/main'` まで正本に取り込まれていた。
- 夜レビューで `backup_run_id` 付き usage event が `x_account_id = null` でも通る余地を再確認し、低リスク修正として `8aa0910 Require X account for backup usage events` を作成してpushした。

## unfinished

- `/Users/uryuatsuya/XGuard/xguard` 自体は引き続き `writable=no`。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- canonical checkoutの `npm run check` は `dist/` 書き込み `EPERM` で完走不可。
- 実Supabase/Postgres接続での `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` は未実施。
- Developer Console原価実値確認は未完了。
- OAuth configured modeはまだ静的 `state`、plain/mock PKCE、mock token refs保存段階。
- `SupabaseTokenRepository` と `supabase/schema.sql` のtoken row契約は未整合。

## findings

- P0: なし。
- P1: `backup_run_id` 付き usage event に `x_account_id` がない場合、backup runとX accountの同一性検証が曖昧になる。対応済み。
- P1: OAuth configured modeが静的 `state`、`code_challenge_method=plain`、mock PKCE、callback state未照合のまま。実OAuth接続前にランダムstate、S256 PKCE、verifier保存、callbackのワンタイム照合が必要。
- P1: `SupabaseTokenRepository` の `access_token_ref` / `refresh_token_ref` / `status` 系契約と、schemaの `encrypted_access_token` / `encrypted_refresh_token` / `revoked_at` 系契約がズレている。
- P2: `app.use(cors())` が全origin許可。cookie/session導入前に `APP_BASE_URL` または明示allowlistへ寄せる。
- P2: `/api/x/oauth/status` はsecret値を返さないが未認証で設定状態を返す。本番継続ならadmin health checkまたはdeployment-only routeへ寄せる。
- P2: Supabase SQL integration testはskip-by-defaultのため、release gateとして実DB接続の手動証跡またはCI jobが必要。

## fixes applied

- `supabase/schema.sql`
  - `p_backup_run_id is not null and p_x_account_id is null` を `api_usage_ledger_x_account_required_for_backup_run` で拒否。
  - backup run検証を `backup_runs.x_account_id = p_x_account_id` に固定。
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`
  - 実DB integration testに `backup_run_id` あり / `x_account_id` なしの拒否ケースを追加。
- `backend/src/__tests__/supabaseSchemaContract.test.ts`
  - SQL contract testを追加し、上記の契約が通常Vitestで検知されるようにした。
- XGuard commit: `8aa0910 Require X account for backup usage events`
- XGuard push先: `UryuAtsuya/Xguard` `main`

## proposed fixes

- OAuth state / S256 PKCE / verifier storage / callback validationを実装する。
- `SupabaseTokenRepository` と `supabase/schema.sql` のtoken保存契約を一本化する。
- CORSを明示allowlistへ寄せ、`/api/x/oauth/status` をproductionで無効化またはadmin-onlyにする。
- `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実Supabase/Postgres接続で走らせ、role/grant/RLS/check constraintの証跡を残す。
- Developer Consoleでendpoint別単価、credit/spending、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。

## verification

- canonical `/Users/uryuatsuya/XGuard/xguard`
  - `git diff --check`: pass
  - `npx tsc -p tsconfig.build.json --noEmit`: pass
  - `npm run test`: pass、6 files passed / 1 skipped、40 passed / 2 skipped
  - targeted integration test: skipped as designed when `RUN_SUPABASE_SQL_INTEGRATION_TESTS` / DB URLなし
  - `npm run check`: fail、`dist/` write `EPERM`。code failureではなくpermission blocker。
- push用作業コピー `/private/tmp/xguard-evening-20260601-5YPt9Z`
  - `git diff --check`: pass
  - targeted Vitest: pass、1 passed / 1 skipped
  - `npx tsc -p tsconfig.build.json --noEmit`: pass
  - `npm run check`: pass、7 files passed / 1 skipped、41 passed / 2 skipped
  - `git diff --cached --check`: pass
  - `git push origin main`: pass、`4e6258c..8aa0910 main -> main`

## tomorrow handoff

1. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行、`authenticated` 拒否、ownership、同一Xアカウント整合性、存在しない `backup_run`、月次上限超過、負値拒否を確認する。
2. OAuth configured modeのstate / S256 PKCE / callback validationとtoken schema reconciliationを進める。
3. Developer Consoleでendpoint別単価、credit/spending、Usage endpoint、Owned Reads条件を確認し、XGuard docsとcompany gateへ反映する。

## subagent findings

- Review agent: P0なし。P1はOAuth static state / mock PKCE、token repository/schema drift。P2はCORS全開、OAuth status未認証、実DB integration gate未実行。
- Verification agent: code failureなし。canonical checkoutは `dist/` write `EPERM` と `.git/FETCH_HEAD` write blockerあり。書き込みを伴わないtypecheckとVitestはpass。
- Documentation/Sync agent: evening note、project note、翌日TODO、decision、PM ticket、active projects、project README、pre-implementation gate、automation memory更新が必要と整理。
