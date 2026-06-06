---
created: "2026-06-07"
project: "xguard"
assignee: "codex"
priority: high
status: open
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

- [ ] `tsc --noEmit` pass
- [ ] `git diff --check` pass
- [ ] targeted Vitest（`backupProofAuth.test.ts`）pass
- [ ] `git add backend/src/__tests__/backupProofAuth.test.ts backend/src/app.ts docs/API_SPEC.md` → commit → push
- [ ] push 結果（commit hash と状態）を `company/notes/2026-06-07-midday-xguard-implementation.md` に記録する
- [ ] `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts` を実行し、結果を記録する
  - 確認項目: `service_role` 専用、`authenticated` 拒否、ownership、同一 X アカウント、存在しない `backup_run`、`x_account_id` 必須、負値拒否、月次上限超過
  - blocker 時は条件（DB URL / `psql`）と skip 理由を記録する
- [ ] `docs/API_COST_MODEL.md` 更新: 通常 read 単価、`Owned Reads` 非適用根拠、Usage endpoint、spending limit、月次上限前停止
- [ ] `docs/COMPLIANCE.md` 更新: Enterprise 適用要否チェックリスト、24 時間削除 SLA、API access 終了時全削除 runbook
- [ ] 上記 docs 変更を commit/push する
- [ ] `company/notes/2026-06-07-midday-xguard-implementation.md` を作成して全実装ログを残す

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
