---
date: "2026-06-07"
project: "xguard"
type: morning-planning
---

# 2026-06-07 朝会 — XGuard 朝会引き継ぎ

## 昨日の終了状態（2026-06-06 夜会から）

- XGuard 正本 `/Users/uryuatsuya/XGuard/xguard`
- local `HEAD` = local `origin/main` = `2b96993 Add OAuth state and PKCE guard`
- tracked 差分なし、`output/playwright/` 未追跡あり
- `npm run build:api` / `npm run build:web` は `EPERM`
- `git ls-remote` DNS 失敗、`git fetch` `.git/FETCH_HEAD` 書き込み不可
- 全 Vitest は frontend 5 秒 timeout 1 件で失敗（targeted では pass）
- 夜会レビュー: `company/notes/2026-06-06-evening-xguard-code-review.md`

## 今日の優先順位

### Top 1 — backup / proof API 認証・所有権・proof boundary（Codex 委譲）

**問題**: `POST /api/backup/run`、`GET /api/backup/status/:runId`、`GET /api/recovery/:runId/proof` が無認証。user ownership / proof visibility / revocation の拒否ロジックなし。

**実装対象**:
- auth middleware を backup / proof route へ適用し、`req.userId` を確立する。
- `backupRun.userId !== req.userId` の場合は 403 を返す。
- proof の `visibility === "private"` または `revokedAt != null` の場合は 404 を返す。
- 他 user アクセス、private proof、revoked proof、存在しない run id の HTTP 境界テストを追加する。

**検証条件**:
- `tsc --noEmit` pass
- `git diff --check` pass
- targeted Vitest（新規テストすべて pass）
- `npm run check`（writable 環境なら full pass）

**完了条件**: auth boundary と拒否テストが pass し、P1 "無認証 backup/proof" が解消されること。

### Top 2 — 実 Supabase/Postgres integration test（Codex 委譲）

```bash
RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner \
  backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts
```

**確認項目**: service_role、ownership、同一 X アカウント整合性、存在しない `backup_run`、`x_account_id` 必須、負値拒否、月次上限超過。

**blocker**: Supabase DB URL と `psql` が接続可能な環境が必要。sandbox 環境では skip される可能性あり。ログを `company/notes/2026-06-07-midday-xguard-implementation.md` へ記録する。

### Top 3 — docs gate 更新（Codex 委譲）

- `docs/API_COST_MODEL.md` へ追記: 通常 read 単価（`$0.00003` / 1,000 tweets 程度）、`Owned Reads` は SaaS 向け複数ユーザーに非適用、Usage API endpoint の存在、spending limit、月次上限前停止ロジック。
- `docs/COMPLIANCE.md` へ追記: Enterprise プラン適用要否確認チェックリスト、24 時間削除 SLA、API access 終了時の全データ削除 runbook。

## Codex 昼実装 handoff スコープ

| 項目 | 内容 |
|------|------|
| 対象リポジトリ | `UryuAtsuya/Xguard`（local: `/Users/uryuatsuya/XGuard/xguard`） |
| 起点 commit | `2b96993 Add OAuth state and PKCE guard` |
| 書き込み不可の場合 | `/private/tmp/xguard-midday-2026-06-07` を remote 最新から clone して使う |
| 変更候補 | `backend/src/routes/backup.ts`（または相当）、`backend/src/routes/recovery.ts`（または相当）、auth middleware、新規テストファイル |
| 完了条件 | auth boundary + 拒否テスト pass、tsc pass、targeted Vitest pass |
| 検証条件 | `git diff --check`、`tsc --noEmit`、targeted Vitest、可能なら `npm run check` |
| 戻し先 | `company/pm/tickets/2026-06-05-xguard-oauth-proof-supabase-compliance.md` に実装結果を追記 |
| 新規ノート | `company/notes/2026-06-07-midday-xguard-implementation.md` を作成して実装ログを残す |
| push 先 | `UryuAtsuya/Xguard` `origin/main`（DNS / 権限 blocker の場合は理由・commit hash・次の操作を記録） |

## 判断ルール（引き継ぎ）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。自動 DM、自動 follow/unfollow、自動投稿、bulk outreach、BAN 回避導線は追加しない。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない。
- 実装コードを MyLife Vault 内へ置かない。
- `output/playwright/` 未追跡は今日触らない。

## 未解決事項

- GitHub DNS 解決失敗による live remote 確認未完。CI 環境または GitHub Actions で `git ls-remote origin refs/heads/main` を試す。
- `npm run build:api` / `npm run build:web` の `EPERM` は指定パス権限の問題。writable clone での build 確認を推奨。
- frontend `App.test.tsx` 5 秒 timeout 失敗は環境遅延と判断済み。next run で `--testTimeout=20000` を加えた targeted で再確認する。
- 実 Supabase integration test は DB URL / psql なしでは skip。本番環境または Supabase CLI でのローカル起動を要する。
