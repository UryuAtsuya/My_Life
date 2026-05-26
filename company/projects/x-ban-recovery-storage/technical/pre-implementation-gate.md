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
