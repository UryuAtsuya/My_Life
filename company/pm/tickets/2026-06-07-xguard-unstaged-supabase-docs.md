---
created: "2026-06-07"
project: "xguard"
assignee: "codex"
priority: high
status: in-progress-remote-reconcile
handoff: "company/notes/2026-06-07-morning-planning.md"
handoff_at: "2026-06-07T07:30:00"
---

# XGuard unstaged commit / Supabase test / docs release gate

## 内容

XGuard 正本 `/Users/uryuatsuya/XGuard/xguard` の `HEAD = origin/main = b03d9c8 Protect backup and proof APIs`。push 済みだが、その後の 3 ファイルが unstaged のまま残っている。今日のタスクはこれを commit/push し、実 Supabase/Postgres integration test と docs release gate（`API_COST_MODEL.md` / `COMPLIANCE.md`）を閉じること。

## 前提

- 起点: `b03d9c8 Protect backup and proof APIs`（`HEAD = origin/main`、push 済み）
- unstaged:
  - `backend/src/__tests__/backupProofAuth.test.ts`（テスト拡充）
  - `backend/src/app.ts`（visibility private default 修正）
  - `docs/API_SPEC.md`（auth 境界ドキュメント化）
- `output/playwright/` 未追跡は今日触らない

## 完了条件

- [x] `tsc --noEmit` pass. Evidence: 2026-06-07夜run `npx tsc -p tsconfig.json --noEmit` pass。
- [x] `git diff --check` pass. Evidence: 2026-06-07夜run `git diff --check && git diff --cached --check` pass。
- [x] targeted Vitest（`backupProofAuth.test.ts`）pass. Evidence: 1 file / 8 tests passed。
- [x] `git add backend/src/__tests__/backupProofAuth.test.ts backend/src/app.ts docs/API_SPEC.md` → commit → push. Evidence: XGuard `9ac4f2f Add proof visibility management route` pushed to `UryuAtsuya/Xguard` `main`。
- [x] push 結果（commit hash と状態）を記録する。Correction: 昼noteは未作成のため、夜レビュー `company/notes/2026-06-07-evening-xguard-code-review.md` に記録。
- [ ] `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts` を実行し、結果を記録する
  - 確認項目: `service_role` 専用、`authenticated` 拒否、ownership、同一 X アカウント、存在しない `backup_run`、`x_account_id` 必須、負値拒否、月次上限超過
  - blocker 時は条件（DB URL / `psql`）と skip 理由を記録する
- [x] `docs/API_COST_MODEL.md` 更新: 通常 read 単価、`Owned Reads` 非適用根拠、Usage endpoint、spending limit、月次上限前停止。Evidence: XGuard `c4403d8 Document XGuard release gates`。
- [x] `docs/COMPLIANCE.md` 更新: Enterprise 適用要否チェックリスト、24 時間削除 SLA、API access 終了時全削除 runbook。Evidence: XGuard `c4403d8 Document XGuard release gates`。
- [x] 上記 docs 変更を commit/push する。Evidence: `git push origin main` -> `9ac4f2f..c4403d8 main -> main`。
- [x] `company/notes/2026-06-07-midday-xguard-implementation.md` を作成して全実装ログを残す。

## 2026-06-07 昼run結果

- 実装スライス: docs release gate 更新のみ。
- 作業コピー: `/private/tmp/xguard-midday-2026-06-07-1331`
- XGuard commit: `c4403d8 Document XGuard release gates`
- push: 成功。`UryuAtsuya/Xguard` `main` へ `9ac4f2f..c4403d8`。
- 検証pass: `git diff --check`, `git diff --cached --check`, `tsc --noEmit`。
- blocker: `npx tsc` は temp clone に `node_modules` がなく、registry DNS `ENOTFOUND registry.npmjs.org`。正本 `node_modules` symlinkを一時利用して `tsc` pass。
- Review対応: 削除/退会とproof revokeのSLA分離、user read / total spend / credit balance evidence追加、100万tweet readの内部threshold明記、Usage endpointを `api.x.com` に修正。
- 未完: 実Supabase/Postgres integration test、OAuth configured mode 実token exchange。

## 2026-06-07 12:45 PM handoff メモ

- Top 1（unstaged commit）は `9ac4f2f Add proof visibility management route` として完了済み。
- Top 2（Supabase integration test）は DB URL / `psql` blocker のため昼 run でもスキップ見込み。次サイクルへ送る。
- 昼 Codex の実装対象を **Top 3（docs gate）** に絞り、`company/notes/2026-06-07-claude-code-codex-handoff.md` を作成した。
- `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` 更新 → commit / push は Codex 昼 run へ委譲。

## 2026-06-07 夜run結果

- XGuard commit: `9ac4f2f Add proof visibility management route`
- push: 成功。`git push origin main` -> `b03d9c8..9ac4f2f main -> main`
- 検証pass: `git diff --check`, `git diff --cached --check`, `npx tsc -p tsconfig.json --noEmit`, targeted `backupProofAuth.test.ts`, Verification agentの `npm run test`
- blocker: `npm run check` は `dist/backend/...` 書き込み `EPERM`
- blocker: push後の `git ls-remote` はDNS失敗
- 未完: 実Supabase/Postgres integration test、`docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md`
- 追加P0: configured OAuth callbackが実X token exchangeなしでsession発行するため、明日の上位タスクへ繰り上げる。
- 追加完了: owner-only `PATCH /api/recovery/:runId/proof/visibility` は `9ac4f2f` に含まれる。`diff check`、`tsc --noEmit`、targeted Vitest 11件はpass。

## 2026-06-07 朝会再整理

- システム日付: `2026-06-07 17:02:19 JST`。
- XGuard 正本: `/Users/uryuatsuya/XGuard/xguard`。
- current local `HEAD`: `7e33e9f Guard production OAuth callback boundary`。
- local git status: `main...origin/main [ahead 1]`、未追跡は `output/playwright/` のみ。
- 注意: 昼run記録上は `c4403d8 Document XGuard release gates` が `UryuAtsuya/Xguard` `main` へpush済みだが、現canonical checkoutのlocal trackingは `9ac4f2f`。次のCodex実装は `git ls-remote` / `git fetch` / ahead-behind比較を最初に行い、remote側の `c4403d8` を上書きしない。
- 次の実装Top 1: `7e33e9f` の remote 反映可否確認と、OAuth production boundaryの不足レビュー。
- 次の実装Top 2: 実 X token exchangeのlive疎通証跡、または live credentials 不足時のproduction mock callback禁止 gate確認。
- 次の実装Top 3: 実Supabase/Postgres integration test。

## 判断ルール

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。自動 DM、自動 follow/unfollow、自動投稿、bulk outreach、BAN 回避導線は追加しない。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない（Post read `$0.005/resource`、User read `$0.010/resource` を使う）。
- prototype user header（`x-xguard-user-id`）は production 認証として扱わない。
- production code を MyLife Vault 内へ置かない。
- 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-07` を remote 最新から clone して使う。
- force push しない。remote 先行確認後に push する。

## 戻し先

- 本チケット（`company/pm/tickets/2026-06-07-xguard-unstaged-supabase-docs.md`）に実装結果を追記する。
- 実装ログ: `company/notes/2026-06-07-midday-xguard-implementation.md` を新規作成する。
- MyLife repo 側のコミット: `company/todos/2026-06-07.md` の Top 3 チェックを更新する。
