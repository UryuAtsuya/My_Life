---
date: "2026-05-28"
type: midday-implementation
project: xguard
---

# 2026-05-28 XGuard 昼実装

## 結論

指定パス `/Users/uryuatsuya/XGuard/xguard` は今日は書き込み可能で、`origin/main` の `3528e26` とローカル `e750d04` の分岐をmergeしてから、prototypeのOAuth開始URLを環境変数対応へ進めた。

XGuard実装repoは `UryuAtsuya/Xguard` `origin/main` へ `18676f0 Add runtime OAuth configuration` としてpush済み。

## 実装内容

- `backend/src/config/runtimeConfig.ts` を追加し、`PORT`, `APP_BASE_URL`, `X_CLIENT_ID`, `X_CALLBACK_URL`, `X_CLIENT_SECRET` のruntime config境界を作った。
- `/api/x/oauth/start` は `X_CLIENT_ID` がある場合にconfigured modeのX OAuth URLを返す。未設定ならmock modeのまま動く。
- `/health` に `xOAuthMode` を追加し、runtimeがmock/configuredどちらで動いているか確認できるようにした。
- `dotenv/config` をserver entrypointで読み込み、ローカル `.env` 導入後にprototypeをそのまま起動できる形にした。
- merge時にledger validationの正本 `3528e26` を取り込み、重複helperと衝突を整理した。

## 検証

- `git diff --check`: pass
- `git diff --cached --check`: pass
- `npm run check`: pass
- Vitest: 4 files / 30 tests pass
- XGuard push: `18676f0` -> `UryuAtsuya/Xguard` `origin/main`

## 未完了

- `X_CLIENT_ID` / `X_CALLBACK_URL` / `X_CLIENT_SECRET` の実値導入。
- OAuth callbackで実token exchangeを行う処理。
- Supabase-backed `ApiUsageLedgerRepository` と月次API原価上限stop rule。
- Developer Console実画面でendpoint別単価、Usage endpoint、Owned Reads条件を確認して `docs/API_COST_MODEL.md` へ反映すること。

## 次の上位TODO

1. `X_CLIENT_ID`, `X_CALLBACK_URL`, `X_CLIENT_SECRET` をローカルまたはRailway backend runtimeへ入れ、`/api/x/oauth/start` がconfigured modeになることを確認する。
2. Developer Console実画面で単価・spending/credit・Owned Reads条件を確認し、XGuard docsとcompany gateへ反映する。
3. `SupabaseApiUsageLedgerRepository` を実装し、`backup_runs` / `api_usage_events` / `monthly_api_cost_limit_usd` 超過前停止をtransactionで検証する。

## 13:40 追記: Supabase ledger repository

この実行環境からは指定パス `/Users/uryuatsuya/XGuard/xguard` が `writable=no` だったため、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-28` の一時作業コピーで進めた。

### 追加実装

- `backend/src/repositories/supabaseApiUsageLedgerRepository.ts` を追加し、`ApiUsageLedgerService` とSupabase row境界のmappingを作った。
- `supabase/schema.sql` に `record_api_usage_event_with_monthly_limit` を追加した。`user_profiles` を `for update` でロックし、当月 `api_usage_events` 合計が `monthly_api_cost_limit_usd` を超える場合はinsert前に拒否する。
- `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts` を追加し、Supabase row mapping、backup summary rollup、月次原価上限超過時にusage eventが永続化されないことを検証した。
- `docs/API_COST_MODEL.md`, `docs/ARCHITECTURE.md`, `docs/API_SPEC.md`, `docs/DEPLOY.md` にSupabase transaction boundaryとdeploy gateを追記した。

### 検証

- `npm ci`: pass
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`: pass（1 file / 2 tests）
- `npm run check`: pass（5 files / 32 tests）
- `git diff --check`: pass
- `git diff --cached --check`: pass

### Git状態

- XGuard local commit: `9be85a1 Add Supabase API usage ledger repository`
- 作業コピー: `/private/tmp/xguard-midday-2026-05-28`
- push先予定: `UryuAtsuya/Xguard` `origin/main`
- push結果: 未push。`git push origin main` は `fetch first` で拒否され、続く `git fetch origin main` / `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com` で失敗した。force pushは行っていない。

### 夜レビューへ送るTODO

1. GitHub DNSが通る環境で `origin/main` の先行commitをfetchし、`9be85a1` をrebase/mergeしてpushする。
2. Developer Console実画面でendpoint別単価、spending/credit、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ実値を入れる。
3. `record_api_usage_event_with_monthly_limit` を実Supabase client storeから呼ぶ実装へ進め、backup workerから直接insertできないようにする。
