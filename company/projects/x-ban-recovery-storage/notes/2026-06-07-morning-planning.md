---
date: "2026-06-07"
project: "xguard"
type: "morning-planning"
status: "ready-for-midday-rerun"
---

# 2026-06-07 XGuard 朝会

## 今日の方針

XGuard を事業最優先にする。朝時点の `b03d9c8` / unstaged 3ファイル前提は、その後 `9ac4f2f Add proof visibility management route`、`c4403d8 Document XGuard release gates`、local `7e33e9f Guard production OAuth callback boundary` まで進展している。

この朝会再整理では production code は実装しない。昼runの最初の仕事は、canonical checkoutの `7e33e9f` と remote 側の `c4403d8` / `9ac4f2f` の関係を確認し、force pushなしで整合させることにする。

## XGuard 正本の現在状態（再確認）

- パス: `/Users/uryuatsuya/XGuard/xguard`
- `HEAD = 7e33e9f Guard production OAuth callback boundary`
- local status: `main...origin/main [ahead 1]`
- local tracking `origin/main`: `9ac4f2f Add proof visibility management route`
- 6/7昼run記録: `c4403d8 Document XGuard release gates` は `UryuAtsuya/Xguard` `main` へpush成功記録あり。ただし現canonical checkoutには未反映に見えるため、昼runでremoteを再確認する。
- **tracked changes**: なし
- **untracked（今日は触らない）**:
  - `output/playwright/record-local-flow.mjs`
  - `output/playwright/videos/`
  - `output/playwright/xguard-local-flow-summary.json`
  - `output/playwright/xguard-local-initial.png` 他

## 今日の Top 3

### Top 1 — `7e33e9f` / remote 整合確認とpush（Codex 委譲）

- `git ls-remote origin refs/heads/main` で live remote の hash を確認する。
- `git fetch origin main` が通る場合は fetch 後に `origin/main..HEAD` と `HEAD..origin/main` を比較する。
- remote に `c4403d8` が存在する場合、`7e33e9f` と docs gate commitを競合させず、merge / rebase / cherry-pickの最小手順を選ぶ。
- `git push origin main` は force しない。
- `output/playwright/` は今回の対象外。

**完了定義**: `7e33e9f` のpush可否、remote hash、`c4403d8` との関係が PM ticket と実装ログに記録される。

### Top 2 — OAuth configured mode 実token exchange境界（Codex 委譲）

- `7e33e9f` の内容をレビューし、productionで mock callback/session 発行が禁止されているか確認する。
- live X credentials がある場合は実 X token endpoint 交換、subject/account 検証、scope維持（`tweet.read`, `users.read`, `offline.access`）を確認する。
- credentials がない場合は、実交換なしでproduction sessionが発行されない runtime gate と targeted test を証跡化する。

**完了定義**: OAuth configured mode の production No-Go 条件がコード・テスト・docsで一致し、未確認事項が明記される。

### Top 3 — 実 Supabase/Postgres integration test（Codex 委譲）

```bash
RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner \
  backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts
```

**確認項目**: `service_role` 専用実行、`authenticated` 拒否、ownership、同一 X アカウント、存在しない `backup_run`、`x_account_id` 必須、負値拒否、月次上限超過。

**blocker 対応**: 実 Supabase DB URL / `psql` が必要。sandbox 環境では skip される場合はその旨とコマンドだけを記録する。

**完了定義**: テスト結果（pass / skip / fail 理由）が `company/notes/2026-06-07-midday-xguard-implementation.md` に記録される。

### 完了済み扱い — docs release gate 更新

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

**完了定義**: 6/7昼runで XGuard `c4403d8 Document XGuard release gates` としてpush済み記録あり。昼runでは remote 上の存在を再確認する。

## Codex 昼実装 handoff スコープ

| 項目 | 内容 |
|------|------|
| 対象リポジトリ | `UryuAtsuya/Xguard`（local: `/Users/uryuatsuya/XGuard/xguard`） |
| 起点 commit | local `7e33e9f Guard production OAuth callback boundary`。remote側に `c4403d8` がある可能性を先に確認する |
| 書き込み不可の場合 | `/private/tmp/xguard-midday-2026-06-07` を remote 最新から clone して使う |
| 変更候補 | `backend/src/app.ts`、`backend/src/config/runtimeConfig.ts`、`backend/src/__tests__/api.test.ts`、`docs/API_SPEC.md`、`docs/DEPLOY.md`、必要なら `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` |
| 完了条件 | remote整合確認 + `7e33e9f` push可否確定 + OAuth production boundary検証 + Supabase実DB検証またはblocker記録 |
| 検証条件 | `git diff --check`、`tsc --noEmit`、OAuth targeted Vitest、Supabase integration test、可能なら `npm run check` |
| 戻し先 | `company/pm/tickets/2026-06-07-xguard-unstaged-supabase-docs.md` に実装結果を追記 |
| 新規ノート | `company/notes/2026-06-07-midday-xguard-implementation.md` を作成して実装ログを残す |
| push 先 | `UryuAtsuya/Xguard` `origin/main`（force push禁止。blocker の場合は commit hash・理由・次の操作を記録） |

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
