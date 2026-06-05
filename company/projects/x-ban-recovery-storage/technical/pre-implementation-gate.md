---
created: "2026-05-23"
project: "xguard"
type: implementation-gate
status: draft
---

# XGuard 実装前ゲート

## Gate 1: X API利用範囲

- [ ] Developer Consoleでendpoint別単価を確認する。
- [ ] `GET /2/users/me` が使えるscopeを確定する。
- [ ] `GET /2/users/:id/tweets` の取得件数、pagination、fieldsを決める。
- [ ] `GET /2/users/:id/followers` と `following` を保存対象にするか、集計値だけにするか決める。
- [ ] メディアURLとファイル本体を保存するか、URL/metadataだけにするか決める。

## Gate 2: セキュリティ

- [x] OAuth tokenは平文保存しない設計をDB draftへ入れる。Evidence: `technical/supabase-v1-schema-draft.sql`
- [x] access token / refresh token / scope / expires_at / revoked_at を `x_oauth_connections` で管理する設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [x] フロントエンドにservice role keyやtokenを返さない。Evidence: XGuard `b3bd37c` の `SupabaseTokenRepository` contractはtoken refだけを返す。
- [x] token失効時は `x_accounts.status = auth_expired` にする。Evidence: XGuard `b3bd37c` の `TokenRepository.markAuthExpired`。
- [x] token削除とユーザーデータ削除の導線を用意する。Evidence: XGuard `b3bd37c` の `TokenRepository.deleteXToken` とrevoked row read除外テスト。

## Gate 3: 規約・公開制御

- [x] 証明ページはraw payloadを直接公開しない設計を型とDB draftへ入れる。Evidence: `technical/shared-types-v1-draft.md`
- [x] 公開用DTOを `proof_pages.public_payload` として生成する設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [x] `visibility`, `published_at`, `revoked_at`, `redaction_policy_version` を持たせる設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [x] 削除・protected化・suspended・withheld・ユーザー要求に追従する `content_compliance_events` を持たせる設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [x] 自動DM、自動follow/unfollow、BAN回避と見える機能はv0に入れない。Evidence: `docs/COMPLIANCE.md`

## Gate 4: 課金・コスト

- [x] X API使用量を `api_usage_events` と `backup_runs` に残す設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [ ] ユーザー単位の月次APIコスト見積もりを作る。
- [x] Stripe webhookは `stripe_events.event_id` uniqueで冪等化する設計を作る。Evidence: `technical/supabase-v1-schema-draft.sql`
- [ ] X API spending limitに達した時の停止/通知ルールを決める。

## Gate 5: 明日の実装順

1. XGuard repo初期化。
2. `docs/X_API_SCOPE.md` を作成。
3. Supabase schema v1 draftを作成。
4. OAuth callbackとtoken repositoryのinterfaceを作成。
5. read-only backup jobのservice interfaceを作成。

## Go / No-Go

- Go: read-only接続、OAuth token安全保管、proof DTO、compliance queueまで。
- No-Go: write action、DM送信、一括follow、raw payload公開、規約未確認のLP訴求。

## 2026-05-24 midday gate update

- XGuard repo本体は存在するが、Codex実行環境からは書き込み不可。
- `supabase/schema.sql` と `shared/types.ts` へ直接配置する前段として、MyLife側に適用用draftを保存した。
- 次のGo条件は、`/Users/uryuatsuya/XGuard/xguard` をwritableにした上でdraftを実repoへ配置し、`git diff --check` とTypeScript検証を実行すること。

## 2026-05-24 evening gate update

- XGuard repo本体へ `supabase/schema.sql`, `shared/types.ts`, backend prototype, `docs/API_SPEC.md` を配置し、`ba98160` まで `origin/main` へpush済み。
- v0初期OAuth scopeは `tweet.read`, `users.read`, `offline.access` に固定した。`follows.read` はP1まで入れない。
- Go継続条件:
  - `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を作る。
  - `npm run check` が通常環境で通るようにbuild設定を分ける。
  - Supabase repository層はservice role + Vault/encryption前提で実装する。
- まだNo-Go:
  - `follows.read` を初期scopeへ戻すこと。
  - 自動DM、自動follow/unfollow、自動投稿、raw payload公開。
  - Developer Console確認なしに月額3,000円の原価を確定扱いにすること。

## 2026-05-25 midday gate update

- Go継続: docs gate、build gate、token repository contractは `b3bd37c` で完了。
- `npm run check` は一時clone `/private/tmp/xguard-midday-2026-05-25` でpass。3 files / 5 tests passed。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は書き込み不可のため、夜レビューでは同パスを `b3bd37c` へ同期してから再検証する。
- 残るGate: Developer Console実画面でendpoint別単価/Spending limitを確認する。`backup_runs` + `api_usage_events` transaction serviceを実装する。Stripe webhook handlerを冪等化する。

## 2026-05-25 evening gate update

- 指定パス `/Users/uryuatsuya/XGuard/xguard` のlocal HEADは `91229db`、tracking `origin/main` は `ba98160`。昼メモ上のremote commit `b3bd37c` と夜の指定パス履歴が揃っていない。
- `git push -v origin main` はremote先行のため `fetch first` で拒否。`git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可で失敗。
- `npx vitest run --configLoader runner` はpass。`npx tsc -p tsconfig.json --noEmit` は `tokenRepository.test.ts` のmock fetch型不一致でfail。
- 次のGo条件:
  - 書き込み可能な環境でremoteをfetchし、`b3bd37c` とlocal `91229db` を統合してpushする。
  - `tokenRepository.test.ts` の型修正と `findXToken()` read path scope検査を入れ、`npm run check` をpassに戻す。
  - Developer Console実値を確認してから原価・上限・停止ルールを確定する。

## 2026-05-26 midday gate update

- `/Users/uryuatsuya/XGuard/xguard` は昼runでも `NOT_WRITABLE`。一時clone `/private/tmp/xguard-midday-2026-05-26` で実装し、Vaultへコードを迂回配置しなかった。
- XGuard `origin/main` は `c7a315c Add API usage ledger contract` までpush済み。
- Go継続: `SupabaseTokenRepository.findXToken()` のscope再検査、TypeScript検証復旧、usage/cost ledger最小contract、docs更新は完了。
- 検証: `./node_modules/.bin/tsc -p tsconfig.json --noEmit` pass、`./node_modules/.bin/vitest run --configLoader runner` pass、`npm run check` pass、`git diff --check` pass。
- 残るGate:
  - 指定パスの権限を解消し、`origin/main` `c7a315c` と作業ツリーを同期する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。
  - `ApiUsageLedgerService` のin-memory repositoryをSupabase transaction repositoryへ置き換え、`monthly_api_cost_limit_usd` 超過前停止を実装する。

## 2026-05-26 evening gate update

- push済み一時clone `/private/tmp/xguard-midday-2026-05-26` は `npm run check` pass、`tsc --noEmit` pass、`vitest` pass（4 files / 9 tests）、`git diff --check` pass。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` はlocal HEAD `0991eeb`、tracking `origin/main` `ba98160`、`main...origin/main [ahead 3]` のまま。`XGUARD_NOT_WRITABLE` かつ `.git` も書き込み不可。
- `git ls-remote origin refs/heads/main` はDNS失敗で、夜run中のlive remote確認は未完了。
- 次のGo条件:
  - 指定パスをGitHub `origin/main` の `c7a315c` 以降へ同期する。
  - `ApiUsageLedgerService` に非負整数validationと失敗テストを追加する。
  - Developer Console実値確認後、Supabase transaction repositoryと月次上限stop ruleを実装する。

## 2026-05-27 evening gate update

- XGuard push済み正本は `/private/tmp/xguard-midday-2026-05-27` の `3528e26 Validate API usage ledger inputs`。`UryuAtsuya/Xguard` `origin/main` へのpush確認は `Everything up-to-date`。
- Go継続: `ApiUsageLedgerService` の非負整数validationと失敗テストは正本で完了し、`npm run check` pass。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `not_writable`、`main...origin/main [ahead 1]`、local HEAD `e750d04`。`.git/FETCH_HEAD` は `Operation not permitted` で更新不可。
- `e750d04` は正本 `3528e26` と完全一致しないため、そのままpushしない。
- 残るGate:
  - 指定パスを `origin/main` `3528e26` へ同期する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。
  - Supabase transaction repositoryと `monthly_api_cost_limit_usd` 超過前停止を実装する。

## 2026-05-29 evening gate update

- Go継続: 指定パス `/Users/uryuatsuya/XGuard/xguard` は writable に回復し、`UryuAtsuya/Xguard` `origin/main` は `d30fc48 Harden Supabase usage ledger boundary` までpush済み。
- `record_api_usage_event_with_monthly_limit` は `service_role` 実行境界、user/X account/backup run所有関係検証、同一Xアカウント整合性、負値拒否を持つ。
- Repository boundaryはSupabase `numeric` stringをdomain DTOのnumberへ変換する。
- 検証: `git diff --check`, `tsc --noEmit`, targeted Vitest（1 file / 4 tests）, `npm run check`（6 files / 37 tests）, `git diff --cached --check` pass。
- 残るGate:
  - 実Supabase/Postgres migration testでSQL functionの権限と拒否条件を確認する。
  - real OAuth configured modeをsecret非表示で確認する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。

## 2026-05-31 midday gate update

- Go継続: 一時clone `/private/tmp/xguard-midday-2026-05-31` で `09ff660 Add OAuth status endpoint` を作成し、`GET /api/x/oauth/status` を追加した。
- `GET /api/x/oauth/status` は `mode`, `callbackUrl`, `scopes`, `clientIdConfigured`, `clientSecretConfigured`, `writesEnabled`, `missingEnv` のみ返し、`X_CLIENT_SECRET` 値、OAuth token material、`clientId` 値、`authorizationUrl` は返さない。
- v0 scopeは `tweet.read`, `users.read`, `offline.access` のみに維持した。
- 検証: `git diff --check`, targeted Vitest（1 file / 6 tests）, `tsc --noEmit`, `npm run check`（6 files / 39 tests）, `git diff --cached --check` pass。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`、`.git/FETCH_HEAD` 更新不可のため未反映。
- `git push origin main` は再試行時にremote先行で `fetch first` 拒否。その後の `git fetch origin main` は `Could not resolve host: github.com` で失敗。force pushなし。
- 最終確認では、指定パス `/Users/uryuatsuya/XGuard/xguard` はcleanで `552f2e5 Add OAuth status diagnostic endpoint`。local tracking `origin/main` も `552f2e5`。live remote再読込はDNS失敗。
- 残るGate:
  - DNS復旧後に `552f2e5` がlive remote `origin/main` と一致するか確認する。
  - 一時cloneの `09ff660` は、`552f2e5` と同等または下位差分なら破棄し、必要差分があればcherry-pickで統合する。
  - 実Supabase/Postgres migration testとDeveloper Console原価確認を閉じる。

## 2026-05-31 evening gate update

- 夜レビューでは `/Users/uryuatsuya/XGuard/xguard` がcleanで、local `HEAD` / local `origin/main` は `552f2e5 Add OAuth status diagnostic endpoint`。
- `GET /api/x/oauth/status` はsecret/token/client id値を返さず、v0 scopeは `tweet.read`, `users.read`, `offline.access` のまま。
- 検証: `git diff --check`, `tsc --noEmit`, targeted Vitestはpass。canonical pathの `npm run check` は `dist/` write `EPERM`、`/private/tmp` ローカルクローンでは `npm run check` pass（6 files / 39 tests）。
- Review gate: `/api/x/oauth/status` を本番公開する場合はadmin認証付きhealth checkまたはdeployment-only routeへ寄せる。real OAuthはまだ静的state/mock PKCE/mock callback refs段階。
- 残るGate:
  - `552f2e5` がlive remote `origin/main` に存在するかDNS/権限復旧後に確認する。
  - 一時clone `09ff660` を `552f2e5` と比較し、必要差分だけ扱う。
  - 実Supabase/Postgres migration testとDeveloper Console原価確認を閉じる。

## 2026-06-01 morning gate update

- 朝runではproduction codeを実装しない。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`、Git状態は `main...origin/main`、local `HEAD` / local `origin/main` は `2655267 Filter revoked tweet snapshots from proof DTO`。
- `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。live remote確認は未完了。
- Go継続:
  - `2655267` がlive remote `origin/main` と一致するか確認する。
  - 実Supabase/Postgres migration testでSQL functionの権限と拒否条件を確認する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。
- まだNo-Go:
  - `follows.read`, DM/write/follow系scope追加。
  - 自動DM、自動follow/unfollow、自動投稿、bulk outreach。
  - `Owned Reads` を第三者ユーザー向けSaaSの主前提にすること。

## 2026-06-01 midday gate update

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は昼runでも `writable=no`。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`、`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- Vaultへ実装コードを置かず、`/private/tmp/xguard-midday-2026-06-01-1331` で作業した。
- XGuard local commit は `8cf029c Harden usage ledger schema contract`。`git push origin main` はDNS失敗で未push。
- Go継続:
  - `record_api_usage_event_with_monthly_limit` のlocal schema contract testを追加し、`service_role` grant、`public` / `anon` / `authenticated` revoke、user profile lock、monthly cost-limit insert前拒否、ownership、backup run同一Xアカウント整合性、負値拒否を検知できるようにした。
  - `backup_run_id` 付き usage event は `x_account_id` 必須にした。
  - `api_usage_events` と `backup_runs` のcost / metering系にnon-negative `check` を追加した。
- 検証: `git diff --check`, targeted Vitest（1 file / 3 tests）, `tsc --noEmit`, `npm run check`（7 files / 43 tests）, `git diff --cached --check` pass。
- 残るGate:
  - GitHub DNS復旧後、`8cf029c` をfetch/rebase確認してpushする。
  - 実Supabase/Postgres migration testでrole別RPC、grant/revoke、RLS、check constraint、拒否条件を確認する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。

## 2026-06-01 evening gate update

- Go継続: `8aa0910 Require X account for backup usage events` を `UryuAtsuya/Xguard` `main` へpush済み。
- `backup_run_id` 付きusage eventは `x_account_id` 必須とし、`backup_runs.x_account_id = p_x_account_id` を常に要求する。
- 検証: `/private/tmp/xguard-evening-20260601-5YPt9Z` で `git diff --check`, targeted Vitest, `tsc --noEmit`, `npm run check`, `git diff --cached --check` pass。
- まだNo-Go:
  - 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行しないままreleaseすること。
  - OAuth configured modeを静的state/plain PKCE/mock callback refsのまま実運用へ出すこと。
  - token repositoryとSupabase schemaの保存契約がズレたまま実Supabase storeへ接続すること。
- 残るGate:
  - 実Supabase/Postgres integration test。
  - OAuth state / S256 PKCE / callback validation。
  - Developer Console原価実値確認。

## 2026-06-02 morning gate update

- 朝runではproduction codeを実装しない。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`、Git状態は `main...origin/main`、local `HEAD` / local `origin/main` は `4e6258c`。
- 未コミット変更は `supabase/schema.sql`, `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`。未追跡は `backend/src/__tests__/supabaseSchemaContract.test.ts`。
- `git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`、`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。live remote確認は未完了。
- Go継続:
  - dirty差分を読み、昨日push済み記録 `8aa0910` とlive remote正本の関係を確認する。
  - 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、SQL functionの権限と拒否条件を確認する。
  - OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消する。
  - token repositoryとSupabase schemaの保存契約を一本化する。
  - Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認する。
- まだNo-Go:
  - dirty差分を読まずに巻き戻すこと。
  - `follows.read`, DM/write/follow系scope追加。
  - 自動DM、自動follow/unfollow、自動投稿、bulk outreach。
  - `Owned Reads` を第三者ユーザー向けSaaSの主前提にすること。

## 2026-06-02 midday gate update

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は昼runでも `writable=no`。Vaultへ実装コードを置かず、`/private/tmp/xguard-midday-2026-06-02-1331` で作業した。
- XGuard local commit は `33cae26 Require X account for backup usage events`。
- Go継続:
  - `backup_run_id` 付きusage eventは `x_account_id` を必須とし、`backup_runs.x_account_id = p_x_account_id` を常に要求する。
  - SQL integration gateに `backup_run_id` あり / `x_account_id` なし拒否ケースを追加した。
  - 静的schema contract testを追加し、該当SQL guardの削除や旧条件の復帰を検知できるようにした。
- 検証: `git diff --check`, targeted Vitest, `tsc --noEmit`, `build:api`, `vite build --configLoader runner`, `npm run test`, `git diff --cached --check` pass。
- `npm run check` は Vite既定config loaderが symlink `node_modules/.vite-temp` へ書けず `EPERM`。代替web buildはpass。
- XGuard pushは未完了。`git push origin main` は `fetch first`、`git fetch origin main` は `Could not resolve host: github.com`。force pushなし。
- 残るGate:
  - `33cae26` をremote先行分へrebase/cherry-pickしてpushする。
  - 実Supabase/Postgres integration testをcredential付きで実行する。
  - OAuth state / S256 PKCE / callback validationとDeveloper Console原価実値確認を閉じる。

## 2026-06-02 evening gate update

- Go継続: 指定パス `/Users/uryuatsuya/XGuard/xguard` は夜run最終状態で `HEAD=origin/main=95e6392`、working tree clean。
- `86a71fb` と `8aa0910` の `backup_run_id` / `x_account_id` 境界修正系列は `95e6392 Merge remote-tracking branch 'origin/main'` で統合済み。
- 検証: `git diff --check`, `git ls-files -u`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest, `npm run test`, `npm run build` pass。
- `npm run check` は `dist/backend/...` 上書きが `EPERM` で失敗。コード失敗ではなく、このsandboxの権限ブロッカーとして扱う。

- live GitHub確認は未完了。`git ls-remote origin refs/heads/main` はDNS失敗、`git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可。
- まだNo-Go:
  - `/api/x/oauth/status` を無認証production endpointとして公開すること。
  - 実Supabase/Postgres integration testなしでSQL boundaryを完了扱いにすること。
  - OAuth configured modeを静的 `state` / plain PKCE / callback未照合のまま実運用へ出すこと。
- 残るGate:
  - `95e6392` のlive remote確認。
  - 実Supabase/Postgres integration test。
  - OAuth state / S256 PKCE / callback validation。
  - token repositoryとSupabase schema契約一本化。
  - Developer Console原価実値確認。

## 2026-06-03 morning gate update

- 朝runではproduction codeを実装しない。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`、Git状態は `main...origin/main`、local `HEAD` / local `origin/main` は `95e6392`。
- Go継続:
  - `95e6392` がlive remote `origin/main` と一致するか確認する。
  - 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、SQL functionの権限と拒否条件を確認する。
  - OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消する。

## 2026-06-03 midday gate update

- Go継続: `/api/x/oauth/status` はproductionで `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` と `x-xguard-diagnostic-token` header一致時だけstatus responseを返すようにした。
- XGuard local commit: `9e8b7c5 Guard OAuth status diagnostic in production`。
- 作業場所: `/private/tmp/xguard-midday-2026-06-03-1339`。指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no` のため直接編集していない。
- 検証: `git diff --check`, `git diff --cached --check`, targeted Vitest, `tsc --noEmit`, `build:api`, runner版 `build:web`, `npm run test` pass。
- `npm run check` は Vite既定config loaderの `node_modules/.vite-temp` write `EPERM` で失敗。runner版web buildと全体testはpass。
- XGuard pushは未完了。`git push origin main` は `fetch first`、fetch/ls-remoteはDNS失敗。force pushしない。
- 最終確認で指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled` へ進んでいた。`03ecd2f` は `X_OAUTH_STATUS_EXPOSURE` 未設定時にstatus endpointを404にし、`deployment_diagnostic` 明示時だけ有効化する方式。`9e8b7c5` は丸ごとpushせず、必要差分だけ比較する。
- 残るGate:
  - `03ecd2f` と `9e8b7c5` の差分を確認し、必要差分だけ扱う。
  - 実Supabase/Postgres integration test。
  - OAuth `state` / S256 PKCE / callback validation。
  - token repositoryとSupabase schema契約一本化。
  - Developer Console原価実値確認。
- まだNo-Go:
  - `/api/x/oauth/status` を無認証production endpointとして公開すること。
  - `follows.read`, DM/write/follow系scope追加。
  - 自動DM、自動follow/unfollow、自動投稿、bulk outreach。
  - `Owned Reads` を第三者ユーザー向けSaaSの主前提にすること。

## 2026-06-03 evening gate update

- Go継続: 指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled`、working tree clean。
- `03ecd2f` は `X_OAUTH_STATUS_EXPOSURE` 未設定時に `/api/x/oauth/status` を404へ倒すため、既定公開blockerは解消した。
- ただし `deployment_diagnostic` 明示時の診断endpointは無認証のままなので、header secret、admin auth、private health checkのいずれかで制限するまでrelease gateは閉じない。
- 検証: `git diff --check`, `git diff --cached --check`, targeted Vitest, `tsc --noEmit`, `npm run test` pass。`build:api` / `build:web` は `dist/` write/rm `EPERM`。
- XGuard push: local差分なし。live remote確認は `.git/FETCH_HEAD` 権限とDNS blockerで未完了。
- 残るGate:
  - `deployment_diagnostic` 有効時の診断endpoint制限。
  - 実Supabase/Postgres integration test。
  - OAuth `state` / S256 PKCE / callback validation。
  - token repositoryとSupabase schema契約一本化。
  - Developer Console原価実値確認。
- 最終追記: `6024667 Restrict production CORS origins` を検出。production CORSは `APP_BASE_URL` / `CORS_ORIGINS` ベースへ寄せる方向で進展済み。

## 2026-06-04 morning gate update

- 朝runではproduction codeを実装しない。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`、Git状態は `main...origin/main`、local `HEAD` / local `origin/main` は `6024667 Restrict production CORS origins`。
- `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- Go継続:
  - `deployment_diagnostic` 有効時の `/api/x/oauth/status` を認証・secret付きまたはprivate health checkに限定する。
  - 実Supabase/Postgres integration testでSQL functionの権限と拒否条件を確認する。
  - OAuth configured modeの固定 `state`、plain/mock PKCE、callback未照合を解消する。
  - `docs/API_COST_MODEL.md` で通常read単価を使い、`Owned Reads` を複数顧客向け原価前提から外す。
  - 公開有料ローンチ前にEnterprise適用要否を確認する。
  - X Content削除・変更追従の24時間SLAと、API access終了時の全削除runbookを用意する。
- まだNo-Go:
  - `deployment_diagnostic` 有効時に診断endpointを無認証公開すること。
  - 実Supabase/Postgres integration testなしでDB境界を完了扱いにすること。
  - `Owned Reads` を複数顧客向けXGuardの主原価前提にすること。
  - `follows.read`, DM/write/follow系scope、自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線を追加すること。

## 2026-06-04 midday gate update

- Go継続: `deployment_diagnostic` 有効時の `/api/x/oauth/status` は32文字以上の `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` と `x-xguard-diagnostic-token` header一致時だけ応答する。
- disabled、token未設定、header欠落、token不一致は同じ404へ寄せ、成功・拒否responseは `Cache-Control: no-store` を返す。
- 比較はSHA-256 digestと `timingSafeEqual` を使い、診断token、client ID、client secret、token materialをresponseやlogへ出さない。
- Review最終判定: P0/P1/P2なし。`npm run check` pass。
- XGuard local commit: `e31510b Guard OAuth deployment diagnostic`。DNS解決失敗のため未push。
- 残るNo-Go:
  - 実Supabase/Postgres integration testなしでDB境界を完了扱いにすること。
  - OAuth configured modeを固定 `state` / plain PKCE / callback未照合のまま実運用へ出すこと。
  - DNS復旧後のlive remote照合なしで `e31510b` をpush済み扱いにすること。

## 2026-06-04 evening gate update

- 指定パスは `HEAD=origin/main=394a3c3 Add OAuth diagnostic HTTP boundary tests`、working tree clean。診断endpointの無認証公開は解消済みとして扱う。
- HTTP境界テストとAPI仕様の認証列を追加し、`UryuAtsuya/Xguard` `origin/main` へpush済み。
- 検証: `git diff --check`, `git diff --cached --check`, `tsc --noEmit`, `npm run test` pass。全testは `50 passed / 4 skipped`。build/checkは `dist/` write `EPERM`。
- まだNo-Go:
  - OAuth configured modeを固定 `state` / plain PKCE / callback未照合のまま実運用へ出すこと。
  - backup / proof APIを認証・user ownership・proof visibility/revocation境界なしで実データへ接続すること。
  - 実Supabase/Postgres integration testなしでDB境界を完了扱いにすること。
  - 24時間削除・変更追従、API access終了時の全削除runbook、Enterprise適用要否を閉じずに公開有料ローンチすること。

## 2026-06-05 midday gate update

- Go継続: 一時clone `/private/tmp/xguard-midday-2026-06-05` で `9374f4e Add one-time OAuth state and S256 PKCE` を作成した。
- OAuth configured modeは一回限り `state`、S256 PKCE、TTL、callback state validation、replay拒否を持つ。
- `code_verifier` はbackend repositoryに保存し、API responseへ返さない。v0 scopeは `tweet.read`, `users.read`, `offline.access` に維持した。
- 検証: `git diff --check`, `git diff --cached --check`, `tsc --noEmit`, targeted Vitest, 全Vitest, `npm run build`, `build:api`, runner指定web buildはpass。
- `npm run check` は symlinked `node_modules/.vite-temp` 書き込み `EPERM` で未完。通常writable checkoutまたはCIで再実行する。
- pushは未完。`git push origin main` は `Could not resolve host: github.com`。
- 残るGate:
  - `9374f4e` をremote先行分確認後にpushする。
  - backup / proof APIの認証、user ownership、proof visibility/revocation境界を実装する。
  - 実Supabase/Postgres integration testとDeveloper Console原価確認、cost/compliance docs更新を閉じる。
