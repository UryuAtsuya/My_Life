---
created: "2026-05-24"
type: evening-xguard-code-review
project: "xguard"
status: reviewed-and-pushed
---

# 2026-05-24 XGuard 夜コードレビュー

## completed

- `/Users/uryuatsuya/XGuard/xguard` の実装repoを確認し、`origin` が `https://github.com/UryuAtsuya/Xguard.git` であることを確認した。
- 昼実装で作られたbackend-first prototypeをレビューした。
  - `supabase/schema.sql`
  - `shared/types.ts`
  - `backend/src/app.ts`
  - `backend/src/repositories/tokenRepository.ts`
  - `backend/src/clients/xApiClient.ts`
  - `backend/src/services/mockBackupService.ts`
  - `backend/src/services/proofDtoBuilder.ts`
  - `backend/src/__tests__/*.test.ts`
  - `docs/API_SPEC.md`
- v0 OAuth scopeを `tweet.read`, `users.read`, `offline.access` の最小read-only範囲に寄せ、`follows.read` を初期mock scopeから外した。
- `backupRuns` の保存範囲をmodule globalから `createApp()` 単位へ閉じ、テストや複数app instance間で状態が混ざらないようにした。
- supertestがサンドボックスでlistenできない問題を避けるため、API prototype testをroute境界の純粋関数/サービス境界テストへ寄せた。
- XGuard実装repoのcommit `ba98160` を `UryuAtsuya/Xguard` の `origin/main` へpushした。

## unfinished

- `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` は未作成。
- Developer Consoleでendpoint別単価、spending limit、Usage endpointの実画面確認は未完了。
- `TokenRepository` はまだin-memoryで、Supabase service role + Vault/encryption実装ではない。
- Stripe webhook handler本体、backup transaction、API usage event永続化、rate-limit header保存は未実装。
- フロントエンド、認証画面、proof page公開UIは未着手。

## findings

1. P0: OAuth scopeが `follows.read` を初期mockに含んでいた。v0のP0は本人のプロフィールと投稿backupであり、followers/following個別一覧はP1なので、最初の同意画面に入れると規約・原価・審査範囲が広がる。
   - 対応: `V0_READ_ONLY_OAUTH_SCOPES` を `tweet.read`, `users.read`, `offline.access` に固定し、テストとdocsも同期した。
2. P1: `backupRuns` がmodule globalだと、テスト間・複数app instance間でmock backup状態が共有される。
   - 対応: `createApp()` 内のMapへ移し、prototypeでも状態境界を明確にした。
3. P1: `npm run check` は通常の確認コマンドだが、この環境では `dist/` へのemitが `EPERM` で失敗した。
   - 修正案: 明日は `tsconfig.build.json` でtest fileをbuild対象から外し、CI/ローカルで `npm run build` が実行できる状態を確認する。
4. P1: API route testがsupertestのlistenに依存していたため、このサンドボックスでは `listen EPERM 0.0.0.0` で落ちた。
   - 対応: 今回はno-listenで検証できる関数/サービス境界テストへ寄せ、`vitest` は通過。
5. P1: API原価モデルとcompliance docsが未作成のため、実装はまだ課金・規約ゲートを完全には通過していない。
   - 修正案: `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` を明日の最優先にする。
6. P2: `TokenRepository` はtoken refを返さない境界になっているが、まだSupabase/Vault実装ではない。
   - 修正案: 次のコード実装はSupabase repository interface、`auth_expired` 遷移、token削除導線から始める。

## fixes applied

- `/Users/uryuatsuya/XGuard/xguard/backend/src/app.ts`
  - `V0_READ_ONLY_OAUTH_SCOPES` を追加し、OAuth start/callbackのscopeを共通化。
  - `follows.read` を初期scopeから削除。
  - `backupRuns` をapp instance内へ移動。
- `/Users/uryuatsuya/XGuard/xguard/backend/src/__tests__/api.test.ts`
  - supertest listen依存を外し、OAuth scopeとmock backup serviceをno-listenで検証。
- `/Users/uryuatsuya/XGuard/xguard/docs/API_SPEC.md`
  - read-only scopeの説明を最小P0に合わせた。
- `/Users/uryuatsuya/XGuard/xguard/docs/X_API_SCOPE.md`
  - followers/followingをP1に下げる前提と初期scopeを同期。

## proposed fixes

1. `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を作成し、read-only境界、月次原価上限、削除/非公開化追従を明文化する。
2. `tsconfig.build.json` を追加し、production buildから `backend/src/__tests__/**` を外す。
3. `TokenRepository` のSupabase実装方針を決め、service role専用、Vault/encryption、frontend非露出、token失効時の `auth_expired` 遷移を実装する。
4. `backup_runs` と `api_usage_events` を1 transactionで書くservice層を作る。
5. Stripe webhook handlerは `stripe_events.event_id` uniqueを使い、同一eventの再送を冪等に処理する。

## verification

- `date '+%Y-%m-%d %H:%M:%S %Z (%z)'`: `2026-05-24 18:01:29 JST (+0900)`
- XGuard `git diff --check`: pass
- MyLife `git diff --check`: pass
- XGuard `npx tsc -p tsconfig.json --noEmit`: pass
- XGuard `npx vitest run --configLoader runner`: pass, 2 files / 3 tests
- XGuard `npm run check`: fail。`tsc` が `dist/` へemitしようとして `EPERM: operation not permitted`。
- XGuard `npm audit --audit-level=moderate --omit=dev`: fail。`registry.npmjs.org` DNS解決不可。
- XGuard `git push origin main`: pass。`ba98160` を `UryuAtsuya/Xguard` にpush済み。

## tomorrow handoff

1. `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を先に作り、Developer Console確認待ち項目を明示する。
2. `tsconfig.build.json` を追加し、`npm run build` と `npm run check` を通常環境で通る形にする。
3. Supabase repository層の最小実装に進む。token本文はfrontendへ返さず、service role + Vault/encryption境界を守る。
