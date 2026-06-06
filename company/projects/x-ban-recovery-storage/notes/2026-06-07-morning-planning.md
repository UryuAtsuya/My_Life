---
date: "2026-06-07"
project: "xguard"
type: "morning-planning"
status: "ready-for-midday"
---

# 2026-06-07 XGuard 朝会

## 今日の方針

XGuard を事業最優先にする。`b03d9c8 Protect backup and proof APIs` は `origin/main` への push 済み。今日の最初のタスクは正本パスの unstaged changes（3ファイル）を commit / push することで、その後 実 Supabase/Postgres integration test と docs release gate を閉じる。

## XGuard 正本の現在状態（朝確認）

- パス: `/Users/uryuatsuya/XGuard/xguard`
- `HEAD = origin/main = b03d9c8 Protect backup and proof APIs`（push 済み）
- **unstaged changes（要 commit/push）**:
  - `backend/src/__tests__/backupProofAuth.test.ts`: テスト拡充（private default、public proof token 非漏洩）
  - `backend/src/app.ts`: backup run visibility default `"public"` → `"private"` 修正
  - `docs/API_SPEC.md`: auth 境界と private/revoked 404 ルールのドキュメント化
- **untracked（今日は触らない）**:
  - `output/playwright/record-local-flow.mjs`
  - `output/playwright/videos/`
  - `output/playwright/xguard-local-flow-summary.json`
  - `output/playwright/xguard-local-initial.png` 他

## 今日の Top 3

### Top 1 — unstaged changes の commit / push（Codex 委譲）

- `tsc --noEmit` → pass 確認
- `git diff --check` → pass 確認
- targeted Vitest（`backupProofAuth.test.ts`）→ pass 確認
- `git add backend/src/__tests__/backupProofAuth.test.ts backend/src/app.ts docs/API_SPEC.md`
- commit → push `origin/main`
- blockerがある場合は commit hash と理由を記録して止める。

**完了定義**: commit hash と push 状態が `company/notes/2026-06-07-midday-xguard-implementation.md` に記録される。

### Top 2 — 実 Supabase/Postgres integration test（Codex 委譲）

```bash
RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner \
  backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts
```

**確認項目**: `service_role` 専用実行、`authenticated` 拒否、ownership、同一 X アカウント、存在しない `backup_run`、`x_account_id` 必須、負値拒否、月次上限超過。

**blocker 対応**: 実 Supabase DB URL / `psql` が必要。sandbox 環境では skip される場合はその旨とコマンドだけを記録する。

**完了定義**: テスト結果（pass / skip / fail 理由）が `company/notes/2026-06-07-midday-xguard-implementation.md` に記録される。

### Top 3 — docs release gate 更新（Codex 委譲）

- `docs/API_COST_MODEL.md`:
  - 通常 read 単価（Post: `$0.005/resource`、User: `$0.010/resource`）
  - `Owned Reads` は developer app owner 本人条件のため SaaS 複数ユーザーには非適用
  - Usage API endpoint の存在と確認手順
  - spending limit の設定方法
  - 月次上限前停止ロジック
- `docs/COMPLIANCE.md`:
  - Enterprise プラン適用要否確認チェックリスト
  - 24 時間削除・変更・非公開・停止 SLA
  - API access 終了時の全データ削除 runbook

**完了定義**: 両ドキュメントの更新と commit が `company/notes/2026-06-07-midday-xguard-implementation.md` に記録される。

## Codex 昼実装 handoff スコープ

| 項目 | 内容 |
|------|------|
| 対象リポジトリ | `UryuAtsuya/Xguard`（local: `/Users/uryuatsuya/XGuard/xguard`） |
| 起点 commit | `b03d9c8 Protect backup and proof APIs`（`HEAD = origin/main`） |
| 書き込み不可の場合 | `/private/tmp/xguard-midday-2026-06-07` を remote 最新から clone して使う |
| 変更候補 | `backend/src/__tests__/backupProofAuth.test.ts`、`backend/src/app.ts`、`docs/API_SPEC.md`、`docs/API_COST_MODEL.md`、`docs/COMPLIANCE.md` |
| 完了条件 | unstaged commit/push + tsc pass + targeted Vitest pass |
| 検証条件 | `git diff --check`、`tsc --noEmit`、targeted Vitest、可能なら `npm run check` |
| 戻し先 | `company/pm/tickets/2026-06-07-xguard-unstaged-supabase-docs.md` に実装結果を追記 |
| 新規ノート | `company/notes/2026-06-07-midday-xguard-implementation.md` を作成して実装ログを残す |
| push 先 | `UryuAtsuya/Xguard` `origin/main`（blocker の場合は commit hash・理由・次の操作を記録） |

## 判断ルール（引き継ぎ）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない。
- `follows.read`、DM/write/follow 系 scope、自動 DM、自動 follow/unfollow、自動投稿、bulk outreach、BAN 回避導線は追加しない。
- production code を MyLife Vault 内へ置かない。
- `output/playwright/` 未追跡は今日触らない（Top 3 完了後に commit 対象か削除対象かを判断する）。
- prototype user header は production 認証として扱わない。本番前に Supabase Auth/JWT + DB ownership へ置換する。

## 未解決事項

- GitHub DNS 解決失敗による live remote 確認は blockerとして継続。CI 環境での確認を推奨。
- `npm run build:api` / `npm run build:web` の `EPERM` は指定パス権限の問題。writable clone での build 確認を推奨。
- frontend `App.test.tsx` 5 秒 timeout 失敗は環境遅延と判断済み。targeted では `--testTimeout=20000` で pass 確認済み。
- 実 Supabase integration test は DB URL / `psql` なしでは skip。Supabase CLI ローカル起動または本番環境での実行が必要。
- Supabase Auth/JWT + DB ownership による prototype user header の置換は release gate として継続。production No-Go 継続。
