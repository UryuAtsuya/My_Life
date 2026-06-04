---
date: "2026-06-04"
project: "xguard"
type: evening-code-review
status: reviewed
---

# 2026-06-04 XGuard 夜コードレビュー

## completed

- 日付確認: `2026-06-04 18:02:04 JST`
- 正本確認: 実装は `/Users/uryuatsuya/XGuard/xguard`、会社記録は `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/company/`。
- XGuard実装repoは `HEAD=origin/main=394a3c3 Add OAuth diagnostic HTTP boundary tests`、working tree clean。
- `fe4b13f` は `deployment_diagnostic` 有効時の `/api/x/oauth/status` を32文字以上のheader token一致時だけ返し、拒否時404統一、`Cache-Control: no-store`、listener不要fallbackテストを追加した。
- `394a3c3` は診断endpointの `supertest` HTTP境界2件と、`docs/API_SPEC.md` の認証列を追加した。
- 前回P1だった診断endpointの無認証公開は解消した。v0 scopeは `tweet.read`, `users.read`, `offline.access` のまま。

## unfinished

- OAuth configured modeの一回限り `state`、S256 PKCE、callback照合、replay防止。
- backup / proof APIの認証・所有権境界。
- 実Supabase/Postgres integration test。
- token repositoryとSupabase schema保存契約の一本化。
- configured OAuthのfrontend認可画面遷移。
- `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` の商用release gate反映。

## findings

- P0: なし。
- P1: OAuth startは固定 `state` と固定 `plain` PKCEを返し、callbackは `code` と `state` が空でないことしか確認しない。CSRF、callback injection、replayを防げないため、configured modeはproduction No-Go。
- P1: `/api/backup/run`、`/api/backup/status/:runId`、`/api/recovery/:runId/proof` に認証・所有権確認がない。fixtureを実データへ置き換える前に、user ownershipとproof visibility/revocation境界が必要。
- P1 release gate: 実Supabase/Postgresでrole、ownership、Xアカウント整合性、月次上限、負値拒否を実証できていない。
- P1 compliance gate: 24時間削除・変更追従、API access終了時の全削除runbook、Enterprise適用要否がXGuard docsで閉じていない。
- P2: configured OAuthのfrontendは `authorizationUrl` を取得してもX認可画面へ遷移しない。
- P2: 診断endpointの `supertest` HTTP境界テストは `394a3c3` で実装済みだが、`CODEX_SANDBOX` ではlisten制限により2件skipされる。通常CIでの実行確認が必要。

## fixes applied

- `backend/src/__tests__/api.test.ts`: 診断endpointのheader欠落・不一致・一致・`Cache-Control: no-store` を `supertest` HTTP境界で確認する2件を追加。
- `docs/API_SPEC.md`: route一覧に認証列を追加し、診断endpointのheader tokenとbackup/proof APIの認証なし状態を明示。
- 残るP1はOAuth状態管理、認証・所有権、実DB検証など夜間の小修正範囲を超えるため、追加実装せず明日へ送った。

## proposed fixes

1. OAuth startで暗号学的乱数の `state` と `code_verifier` を発行し、S256 challenge、user/session、TTLをbackend storeへ保存する。callbackで一致・期限・未使用を検証し、一回限りで消費する。
2. backup / proof routeへauth middlewareを追加し、backup runのuser ownershipとproof visibility/revocationを確認する。
3. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、SQL境界を実証する。
4. configured modeでfrontendを `authorizationUrl` へ遷移させ、通常CIでHTTP境界テストを実行する。
5. `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` に通常read単価、`Owned Reads` 非適用、Enterprise確認、24時間SLA、全削除runbookを反映する。

## verification

- `git status --short --branch`: `## main...origin/main`
- `git rev-parse HEAD` / `git rev-parse origin/main`: `394a3c3b2a5a84c345c7211b41b994c06212e8bb`
- `git diff --check`: pass
- `git diff --cached --check`: pass
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npm run test`: pass、7 files passed / 1 skipped、50 tests passed / 4 skipped
- `npm run build`: fail、`build:api` の `dist/backend/...` write `TS5033 / EPERM`。コード失敗ではなくsandbox権限blocker。
- `npm run check`: fail、`build:api` の `dist/backend/...` write `TS5033 / EPERM`。コード失敗ではなくsandbox権限blocker。
- 実Supabase/Postgres integration test: 未実施。`SUPABASE_DB_URL` / `POSTGRES_URL` と `psql` がない。
- `git push origin main`: pass、`fe4b13f..394a3c3 main -> main`

## tomorrow handoff

1. OAuth一回限り `state`、S256 PKCE、callback validation、replay防止を実装する。
2. backup / proof APIの認証・所有権境界を設計・実装する。
3. 実Supabase/Postgres integration testと商用cost/compliance docsを閉じる。

## subagent findings

- Review agent: 実サブエージェント使用。P0なし。P1はOAuth CSRF/replay、backup/proof認証・所有権、実DB/compliance release gate。P2はconfigured OAuth UI遷移と通常CIでのHTTP境界確認。
- Verification agent: 実サブエージェント使用。typecheckと全testはpass。coordinator最終再検証では全test `50 passed / 4 skipped`、build/checkはsandbox権限blocker。
- Documentation/Sync agent: 実サブエージェント使用。closeout更新先、未完、明日Top 3を整理。昼記録の未push状態は夜の確定状態で訂正する。
- Implementation agent: 実サブエージェント使用。`394a3c3` の対象2ファイルだけを最終確認し、残るP1は明日タスク化する。

## commit / push

- XGuard: `394a3c3 Add OAuth diagnostic HTTP boundary tests` を `UryuAtsuya/Xguard` `origin/main` へpush済み。
- MyLife: 夜レビュー資料を別commitで `UryuAtsuya/My_Life` `origin/main` へ反映する。
