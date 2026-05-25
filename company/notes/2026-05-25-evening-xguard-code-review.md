---
created: "2026-05-25"
type: evening-xguard-code-review
project: "xguard"
status: reviewed-with-push-blocked
---

# 2026-05-25 XGuard 夜コードレビュー

## completed

- システム日付を `2026-05-25 18:01:22 JST` として確認した。
- `CLAUDE.md`, `company/sync-policy.md`, automation memory, 今日のTODO、朝会メモ、昼実装メモ、今日のdecision、PM ticket、XGuard計画ファイル、MyLife/XGuard両方のgit statusを確認した。
- `/Users/uryuatsuya/XGuard/xguard` の `origin` が `https://github.com/UryuAtsuya/Xguard.git` であることを確認した。
- XGuard実装repoの現在HEADが `91229db Exclude revoked token refs`、`origin/main` trackingが `ba98160 Document minimum OAuth scope` で、ローカルが2コミットaheadであることを確認した。
- 昼メモ上のpush済みcommit `b3bd37c Add token repository contract and docs gates` は、現在の指定パス作業ツリーには取り込まれていない。`git push -v origin main` はremoteに先行commitがあるため `fetch first` で拒否された。
- `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md`, build分離、Supabase token repository周辺の実装内容をレビューした。

## unfinished

- XGuard指定パスのローカル履歴とGitHub `origin/main` の同期は未完了。`git fetch origin main` は `.git/FETCH_HEAD` への書き込みが `Operation not permitted` で失敗した。
- XGuard `npm run check` はこのサンドボックスでは `dist/` へのemitが `EPERM` で失敗した。
- 書き込み不要の `npx tsc -p tsconfig.json --noEmit` も、`backend/src/__tests__/tokenRepository.test.ts` のmock `fetchImpl` 型不一致で失敗した。
- Developer Consoleでendpoint別単価、spending limit、Usage endpointの実画面確認は未完了。
- Stripe webhook handler本体、`backup_runs` + `api_usage_events` transaction service、rate-limit header永続化は未実装。

## findings

1. P0: 指定パスのXGuard履歴がremoteと分岐しており、夜レビュー時点ではpushできない。
   - Evidence: `git push -v origin main` は `! [rejected] main -> main (fetch first)`。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
   - 修正案: 書き込み可能な環境で `git fetch origin main` し、remoteの `b3bd37c` とローカル `f60be3e`, `91229db` の重複/差分を確認してからrebaseまたはcherry-pickする。
2. P1: TypeScript検証が落ちている。
   - Evidence: `npx tsc -p tsconfig.json --noEmit` が `backend/src/__tests__/tokenRepository.test.ts` の `fetchImpl` 型不一致で失敗。
   - 修正案: mock fetchを `(input: string | URL | Request, init?: RequestInit) => Promise<Response>` に合わせ、`requests.push({ url: String(input), init: init ?? {} })` に直す。
3. P1: `SupabaseTokenRepository.findXToken()` はrevoked rowを除外するようになったが、read pathでscope再検査していない。
   - Evidence: `saveXToken()` は `assertReadOnlyXScopes()` を呼ぶが、DBから読んだrowのscopeはそのまま返す。
   - 修正案: `row` 取得後に `assertReadOnlyXScopes(row.scope)` を呼び、legacy/手動混入した `follows.read` 等をバックアップ処理へ渡さない。
4. P1: 原価モデルはdocs化されたが、Developer Console実値が未入力のため価格・上限設計はまだ仮置き。
   - 修正案: `GET /2/users/me`, `GET /2/users/:id`, `GET /2/users/:id/tweets`, media expansions, spending limit, usage endpointの値を確認し、`docs/API_COST_MODEL.md` とcompany側gateへ転記する。
5. P2: Stripe webhook冪等処理はDB設計止まり。
   - 修正案: `stripe_events.event_id` uniqueを先にinsertし、既存eventは処理済みとして返すhandler testから実装する。

## fixes applied

- この夜runでは、XGuard指定パスへの `apply_patch` がサンドボックス権限で拒否されたため、新規のXGuardコード修正は完了できなかった。
- 既存ローカルcommit `91229db Exclude revoked token refs` は、`findXToken()` のqueryに `revoked_at=is.null` を追加し、非revoked token refsだけ読むテストを追加している。
- ただし `91229db` は未pushで、かつtest mockの型不一致により `tsc --noEmit` が失敗するため、明日は型修正とremote統合を先に行う。

## proposed fixes

1. 書き込み可能な環境でXGuard指定パスをremote `origin/main` と同期し、`b3bd37c` とローカル `f60be3e`/`91229db` を整理する。
2. `backend/src/__tests__/tokenRepository.test.ts` のmock fetch型を修正し、`npx tsc -p tsconfig.json --noEmit` と `npm run check` を通す。
3. `SupabaseTokenRepository.findXToken()` のread pathにも `assertReadOnlyXScopes(row.scope)` を追加する。
4. Developer Consoleの実値を `docs/API_COST_MODEL.md` へ反映して、ユーザー単位月次上限とapp spending stop ruleを確定する。
5. 次の実装は `backup_runs` + `api_usage_events` transaction service、またはStripe webhook冪等handlerのどちらか1本に絞る。

## verification

- `date '+%Y-%m-%d %H:%M:%S %Z'`: `2026-05-25 18:01:22 JST`
- MyLife `git diff --check`: pass
- XGuard `git diff --check`: pass
- XGuard `npm run check`: fail。`dist/` へのemitが `EPERM: operation not permitted`。
- XGuard `npx tsc -p tsconfig.json --noEmit`: fail。mock `fetchImpl` の引数型が `typeof fetch` と不一致。
- XGuard `npx vitest run --configLoader runner`: pass, 3 files / 7 tests
- XGuard `git fetch origin main`: fail。`.git/FETCH_HEAD` が `Operation not permitted`。
- XGuard `git push -v origin main`: fail。remoteに先行commitがあり `fetch first`。

## tomorrow handoff

1. XGuard指定パスでremote `origin/main` を取得できる書き込み環境を使い、`b3bd37c` とローカル `91229db` を統合してpushする。
2. `tokenRepository.test.ts` のmock fetch型と `findXToken()` read path scope検査を修正し、`npm run check` をpassに戻す。
3. Developer Consoleのendpoint別単価/spending limit確認後、`backup_runs` + `api_usage_events` transaction serviceまたはStripe webhook冪等handlerを1本だけ実装する。
