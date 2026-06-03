---
date: "2026-06-03"
project: "xguard"
type: evening-code-review
status: reviewed
---

# 2026-06-03 XGuard 夜コードレビュー

## completed

- 日付確認: `2026-06-03 18:00:58 JST`
- 正本確認: 実装は `/Users/uryuatsuya/XGuard/xguard`、会社記録は `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/company/`。
- XGuard実装repoは `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled`、working tree clean。
- `03ecd2f` は `/api/x/oauth/status` を `X_OAUTH_STATUS_EXPOSURE` 未設定時に環境名に関係なく404へ倒し、昼のP1 blockerだった既定公開リスクを塞いでいる。
- 昼の一時commit `9e8b7c5 Guard OAuth status diagnostic in production` は丸ごとpushしない判断にした。`03ecd2f` を正として扱う。

## unfinished

- live GitHub remoteの独立確認。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`、MyLife側fetchは `Could not resolve host: github.com`。
- 実Supabase/Postgres integration test。
- OAuth `state` / S256 PKCE / callback validation。
- token repositoryとSupabase schema保存契約の一本化。
- Developer ConsoleでのX API原価、Usage、Owned Reads条件確認。
- `npm run check` の完走。build段階で `dist/` write `EPERM`。

## findings

- P0: なし。
- P1: `X_OAUTH_STATUS_EXPOSURE=deployment_diagnostic` を明示した瞬間、`/api/x/oauth/status` が無認証診断endpointとして公開される。既定無効化は良いが、診断有効時は `x-xguard-diagnostic-token`、admin auth、private health checkのいずれかで制限する。
- P1: OAuth configured modeはまだ固定 `state`、`plain` PKCE、callback未照合。one-time `state` と S256 `code_verifier` 保存、callback照合が必要。
- P2: status route testはExpress内部route stack直呼びで、実HTTP/middleware/header境界を見ていない。
- P2: `npm run check` は権限blockerで未完走。writable checkoutまたはCIで再実行する。

## fixes applied

- 夜runではXGuard実装コードの変更なし。
- 理由: working treeはcleanで、`03ecd2f` が昼のproduction既定公開blockerをすでにより強く閉じていたため。

## proposed fixes

1. `/api/x/oauth/status` の `deployment_diagnostic` 有効時にheader secretまたはadmin/private health check制限を追加する。
2. OAuth start/callbackを、one-time `state`、S256 PKCE、callback照合、token exchange準備の順で閉じる。
3. `supertest` などで `/api/x/oauth/status` の404/200/diagnostic制限をHTTP境界から検証する。
4. 実Supabase/Postgresで `record_api_usage_event_with_monthly_limit` のrole/grant/ownership/monthly limit/negative value拒否を実証する。

## verification

- `git status --short --branch`: `## main...origin/main`
- `git rev-parse --short HEAD`: `03ecd2f`
- `git rev-parse --short origin/main`: `03ecd2f`
- `git diff --check`: pass
- `git diff --cached --check`: pass
- `./node_modules/.bin/vitest run --configLoader runner backend/src/__tests__/api.test.ts`: pass、1 file / 10 tests
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `npm run test`: pass、7 files passed / 1 skipped、45 tests passed / 2 skipped
- `npm run build:api`: fail、`dist/backend/...` write `EPERM`
- `npm run build:web -- --configLoader runner`: fail、`dist/frontend/assets` rm `EPERM`
- `git fetch origin main`: fail、`.git/FETCH_HEAD: Operation not permitted`
- MyLife `git fetch origin main`: fail、`Could not resolve host: github.com`

## tomorrow handoff

1. `03ecd2f` を正として、`deployment_diagnostic` 有効時の無認証公開をheader secret/admin/private health checkで閉じる。
2. 実Supabase/PostgresでSQL integration testを実行する。
3. OAuth `state` / S256 PKCE / callback validation / token schema契約とDeveloper Console原価確認を進める。

## subagent findings

- Review agent: 実サブエージェント使用。P0なし。P1は診断endpoint明示有効時の無認証公開とOAuth `state`/PKCE/callback未照合。P2は`npm run check`権限blockerとroute stack直呼びテスト。
- Verification agent: 実サブエージェント使用。local clean、`HEAD=origin/main=03ecd2f`。targeted/typecheck/testは通過。fetch/ls-remote/buildは環境・権限blocker。
- Documentation/Sync agent: 実サブエージェント使用。MyLife更新対象、明日Top 3、未解決事項を整理。
- Implementation agent: 夜runでは使用しない判断。小修正候補はあるが、実装repoがcleanかつbuild/push権限blockerがあるため明日タスク化した。
