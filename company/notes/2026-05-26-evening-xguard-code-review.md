---
created: "2026-05-26"
type: evening-xguard-code-review
project: "xguard"
status: reviewed-with-specified-path-sync-blocked
---

# 2026-05-26 XGuard 夜コードレビュー

## completed

- システム日付を `2026-05-26 18:01:47 JST` として確認した。
- `CLAUDE.md`, `company/sync-policy.md`, automation memory、今日のTODO、朝会メモ、昼実装メモ、今日のdecision、PM ticket、XGuard計画ファイル、MyLife/XGuard両方のgit statusを確認した。
- 昼実装のpush済み状態として `/private/tmp/xguard-midday-2026-05-26` を確認した。HEADは `c7a315c Add API usage ledger contract`、trackingは `origin/main` と一致。
- push済み側では `ApiUsageLedgerService`、`MockBackupService` のledger接続、token repository scope再検査、API cost docsをレビューした。
- XGuard検証は一時cloneで `npm run check` pass、`tsc --noEmit` pass、`vitest` pass、`git diff --check` pass。
- MyLife側の `git diff --check` もpass。

## unfinished

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は引き続き `XGUARD_NOT_WRITABLE` / `.git` も `XGUARD_GIT_NOT_WRITABLE`。
- 指定パスのlocal HEADは `0991eeb Add API usage ledger contract`、tracking `origin/main` は `ba98160 Document minimum OAuth scope` のまま見えており、push済み一時cloneの `c7a315c` と同期していない。
- `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com` で、夜run中のGitHub live確認はできなかった。
- Developer Console実画面のendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件は未確認。
- `ApiUsageLedgerService` のSupabase transaction repository、`monthly_api_cost_limit_usd` 超過前停止、Stripe webhook冪等handlerは未実装。

## findings

1. P0: 指定パスのXGuard checkoutが、push済み作業ツリーと同期できていない。
   - Evidence: `/Users/uryuatsuya/XGuard/xguard` は `main...origin/main [ahead 3]`、HEAD `0991eeb`、tracking `origin/main` `ba98160`。一方、一時cloneは `c7a315c` でclean。
   - リスク: 次回automationが指定パスだけを見ると、GitHub反映済みの正しい履歴と別hashのローカル履歴をレビューしてしまう。
   - 修正案: 書き込み可能な環境で指定パスを `git fetch origin main` し、`origin/main` が `c7a315c` 以降であることを確認してから `reset` ではなく安全なrebaseまたはfresh cloneで同期する。
2. P1: usage ledgerに負値・小数入力を拒否する境界テストがまだない。
   - Evidence: `estimateXApiReadCostUsd()`, `startBackupRun()`, `recordApiUsage()`, `completeBackupRun()` に `resourceCount`, `tweetLimit`, `tweetsCaptured`, `profilesCaptured` の非負整数検査がない。
   - リスク: 将来のadapter不具合で負のusage/costが入ると、月次上限や原価rollupが壊れる。
   - 修正案: `assertNonNegativeInteger()` をservice境界に追加し、負値・小数を拒否するvitestを追加する。
3. P1: Developer Console実値が未確認のため、月額3,000円の原価判断はまだ固定できない。
   - Evidence: `docs/API_COST_MODEL.md` は保守的単価と未確認項目を明記しているが、authenticated console値は未入力。
   - 修正案: `GET /2/users/me`, `GET /2/users/:id`, `GET /2/users/:id/tweets`, media expansions, spending limit, Usage endpoint, Owned Reads適用条件を実画面で確認してdocsへ転記する。
4. P1: `ApiUsageLedgerService` はin-memory contract段階で、実DBのtransaction境界とbudget stopが未実装。
   - 修正案: Supabase repositoryを追加し、`backup_runs` 作成、`api_usage_events` insert、summary update、`monthly_api_cost_limit_usd` stopを同一service境界で検証する。
5. P2: Stripe webhook冪等handlerはschema設計止まり。
   - 修正案: `stripe_events.event_id` uniqueを先にinsertし、既存eventは処理済みとして返すhandler testから実装する。

## fixes applied

- XGuardコード修正は未適用。`/private/tmp/xguard-midday-2026-05-26` への `apply_patch` は、現Codex workspace外として拒否された。
- そのため、夜runではコードを広げず、検証と会社側ドキュメント同期に限定した。

## proposed fixes

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` をGitHub `origin/main` の `c7a315c` 以降へ同期し、次回レビュー対象を一本化する。
2. `ApiUsageLedgerService` に非負整数validationを追加し、負値・小数のresource/tweet countを拒否するテストを入れる。
3. Developer Console実値を `docs/API_COST_MODEL.md` とcompany gateへ反映する。
4. `ApiUsageLedgerService` のSupabase transaction repositoryと `monthly_api_cost_limit_usd` stop ruleを実装する。
5. Stripe webhook冪等handlerは、ledger永続化が終わった後のP2として扱う。

## verification

- `date '+%Y-%m-%d %H:%M:%S %Z (%z)'`: `2026-05-26 18:01:47 JST (+0900)`
- MyLife `git diff --check`: pass
- XGuard一時clone `git diff --check && git diff --cached --check`: pass
- XGuard一時clone `npm run check`: pass, 4 files / 9 tests
- XGuard一時clone `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- XGuard一時clone `./node_modules/.bin/vitest run --configLoader runner`: pass, 4 files / 9 tests
- XGuard一時clone `git status --short --branch`: `## main...origin/main`
- XGuard live remote確認 `git ls-remote origin refs/heads/main`: fail, `Could not resolve host: github.com`
- 指定パス `/Users/uryuatsuya/XGuard/xguard` `git status --short --branch`: `## main...origin/main [ahead 3]`

## tomorrow handoff

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` の権限と履歴を直し、GitHub `origin/main` の `c7a315c` 以降と同期する。
2. `ApiUsageLedgerService` に非負整数validationと失敗テストを追加し、`npm run check` を通す。
3. Developer Console実値確認後、Supabase transaction repositoryと `monthly_api_cost_limit_usd` stop ruleを実装する。
