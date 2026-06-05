---
date: "2026-06-06"
project: "xguard"
type: evening-code-review
status: completed-with-blockers
---

# 2026-06-06 XGuard 夜コードレビュー

## completed

- 今日の正本を `/Users/uryuatsuya/XGuard/xguard`、GitHub反映先を `UryuAtsuya/Xguard` `origin/main` として確認した。
- XGuard local `HEAD` と local tracking `origin/main` は `2b96993 Add OAuth state and PKCE guard` で一致していた。
- 6/5昼の未push扱いだったOAuth state / S256 PKCE差分は、今日の正本では `2b96993` として反映済みだった。
- OAuth configured modeは、一回限り `state`、S256 `code_challenge`、callback state検証、TTL、replay拒否、`code_verifier` 非返却へ進んでいることを確認した。
- Review agent、Verification agent、Documentation/Sync agent、Implementation agent相当の順次ロール分担で夜レビューを完了した。

## unfinished

- `POST /api/backup/run`、`GET /api/backup/status/:runId`、`GET /api/recovery/:runId/proof` はまだ認証なし。user ownership、proof visibility、revocation境界も未実装。
- 実Supabase/Postgres integration testは未完。`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` 実行では対象テストが環境変数不足によりskipされた。
- `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` の商用release gate更新は未完。
- `/Users/uryuatsuya/XGuard/xguard` はこの実行環境から `writable=no`。build成果物、`node_modules/.vite-temp`、`.git/FETCH_HEAD` への書き込みができない。
- `output/playwright/` 配下の未追跡ファイルは残存。今回のレビューでは触っていない。

## findings

- P0: なし。
- P1: backup / proof APIが無認証のまま公開routeになっている。現状では任意の利用者がmock backupを作成し、run idを知っていればstatus/proof DTOを読める。prototype範囲ではあるが、release gateとしてはNo-Go。
- P1: proof visibility / revocation / owner境界がAPI層にない。`shared/types.ts` とschema設計には `private` / `revoked` があるが、現行routeは `backupRuns` mapから直接返すだけで拒否条件を検証しない。
- P1: 実Supabase/Postgresで `service_role`、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を実証できていない。
- P1: `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` に、通常read単価、`Owned Reads` 非適用、spending limit、24時間削除SLA、API access終了時全削除runbookがrelease gateとしてまだ閉じていない。
- P2: frontendは `authorizationUrl` を取得してもX認可画面へ遷移しない。configured OAuthの実ユーザー導線は未完。
- P2: `InMemoryOAuthStateRepository` はprototypeとして妥当だが、複数process / 複数instanceではcallbackが別instanceへ届く可能性があるため、本番は共有永続storeへ置き換える必要がある。
- P2: 全Vitestはこの環境で `frontend/src/App.test.tsx` の既定5秒timeoutに当たり1件失敗した。targeted frontend testはtimeout延長でpassしたため、コード不具合ではなく環境遅延として扱う。

## fixes applied

- XGuard実装コードへの追加修正はなし。正本が `writable=no` で、夜間に入れるべき小さな安全修正も今回のP1範囲ではAPI認証設計が必要なため、明日タスク化した。
- MyLife側に夜レビュー、明日TODO、PM ticket追記、project note、decision、automation memoryを同期する。

## proposed fixes

1. backup / proof APIへauth boundaryを追加し、request userと `backupRun.userId` / `proof.userId` の一致を必須にする。
2. proof APIで `visibility === "public" || visibility === "unlisted"` かつ `revokedAt` なしだけを返し、private / revoked / 他userを404または403で拒否する。
3. 他user backup/status/proof、private proof、revoked proof、存在しないrun idのHTTP境界テストを追加する。
4. `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実DB接続ありで実行し、role・ownership・月次上限・負値拒否を証跡化する。
5. `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` にcommercial release No-Go条件を明文化する。

## verification

- `date '+%Y-%m-%d %H:%M:%S %Z (%z)'` -> `2026-06-06 03:01:31 JST (+0900)`。
- `git status --short --branch` in XGuard -> `main...origin/main`、tracked差分なし、`output/playwright/` 未追跡あり。
- `git rev-parse --short HEAD` / `git rev-parse --short origin/main` -> `2b96993` / `2b96993`。
- `git diff --check HEAD^ HEAD && git diff --check && git diff --cached --check` -> pass。
- `npx tsc -p tsconfig.json --noEmit` -> pass。
- `CODEX_SANDBOX=1 npm test -- backend/src/__tests__/api.test.ts` -> 1 file passed、19 passed、2 skipped。
- `CODEX_SANDBOX=1 npx vitest run --configLoader runner frontend/src/App.test.tsx --testTimeout=20000` -> 1 file passed、2 passed。
- `CODEX_SANDBOX=1 npm run test` -> 6 files passed、1 skipped、1 failed。失敗は `frontend/src/App.test.tsx` の5秒timeout 1件で、timeout延長targetedではpass。
- `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts` -> 1 file skipped、2 skipped。実DB URL / `psql` なし。
- `npm run build:api` -> `dist/backend/...` 書き込み `EPERM` で失敗。
- `npm run build:web` -> `node_modules/.vite-temp/...` 書き込み `EPERM` で失敗。
- `git ls-remote origin refs/heads/main` -> `Could not resolve host: github.com`。
- `git fetch origin main` -> `.git/FETCH_HEAD: Operation not permitted`。

## tomorrow handoff

1. backup / proof APIの認証、user ownership、proof visibility/revocation境界を実装し、他user・private・revoked拒否テストを追加する。
2. 実Supabase/Postgresでusage ledger integration testを走らせ、role・ownership・同一Xアカウント・負値・月次上限の証跡を残す。
3. `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` に通常read単価、`Owned Reads` 非適用、spending limit、24時間削除SLA、API access終了時全削除runbookを反映する。

## subagent findings

- Review agent: 実サブエージェントは利用不可。順次ロールで代替。P0なし、P1はbackup/proof無認証、proof visibility/revocation未実装、実DB/compliance release gate未完。
- Verification agent: 実サブエージェントは利用不可。順次ロールで代替。diff check、typecheck、backend targeted、frontend targetedはpass。full testは環境timeout、build/fetchは権限/DNSblocker。
- Documentation/Sync agent: 実サブエージェントは利用不可。順次ロールで代替。MyLife側の夜レビュー、TODO、PM ticket、project note、decision、automation memoryを同期対象にした。
- Implementation agent: 実サブエージェントは利用不可。順次ロールで代替。夜間の小修正は適用せず、P1は明日の実装タスクへ送った。
