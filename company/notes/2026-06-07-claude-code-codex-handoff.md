---
date: "2026-06-07"
project: "xguard"
type: codex-handoff
status: ready
scheduled: "12:45"
---

# 2026-06-07 Codex 昼実装 ハンドオフ

## 現状サマリ（12:45 時点）

| 項目 | 状態 |
|------|------|
| XGuard HEAD | `9ac4f2f Add proof visibility management route`（push 済み） |
| MyLife repo | `c287bb7 Record June 7 XGuard evening review`（push 済み） |
| XGuard tracked 差分 | なし（未追跡 `output/playwright/` のみ） |

### 本日 Top 3 進捗

| # | 内容 | 状態 |
|---|------|------|
| Top 1 | unstaged 3 ファイルの commit / push | ✅ 完了（`9ac4f2f`） |
| Top 2 | 実 Supabase/Postgres integration test | ❌ blocker（DB URL / `psql` 不足） |
| Top 3 | docs release gate（API_COST_MODEL / COMPLIANCE） | ❌ 未着手 |

---

## 昼 Codex 実装対象

**Top 3 — docs release gate 更新** に絞る。

**理由:**
- Top 1 は完了済み。
- Top 2 は実 Supabase DB URL と `psql` が必要であり、sandbox 環境ではスキップされる可能性が高い。今日の Codex run でも同様の制約が予想される。
- Top 3 は外部依存なし、diff が文書のみのため完了・検証が容易であり、production release の docs No-Go を解消できる。

---

## Codex への実装指示

### 対象リポジトリ

- **実装コード**: `/Users/uryuatsuya/XGuard/xguard`
  - 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-07` へ `git clone git@github.com:UryuAtsuya/Xguard.git` して使う
- **MyLife 記録先**: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`（実装コードは置かない）

### 起点コミット

`9ac4f2f Add proof visibility management route`（HEAD = origin/main = local main）

### 触ってよいファイル

| パス | 変更内容 |
|------|----------|
| `docs/API_COST_MODEL.md` | 通常 read 単価・Owned Reads 非適用根拠・Usage endpoint・spending limit・月次上限前停止を追記 |
| `docs/COMPLIANCE.md` | Enterprise 適用要否チェックリスト・24 時間削除 SLA・API access 終了時全削除 runbook を追記 |

### 触らないもの

- `output/playwright/`（未追跡ファイル。今回も触らない）
- `backend/`（今回は docs のみ）
- `frontend/`（今回は docs のみ）
- `shared/`（今回は docs のみ）
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`（Top 2 スコープ外）
- `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/`（実装コードを置かない）

### `docs/API_COST_MODEL.md` への追記内容

以下の項目を確認・追記する（既存記述と重複しない範囲で）:

1. **通常 read 単価**: Post read `$0.005/resource`、User read `$0.010/resource`（2025-05 時点 X API Basic/Pro tier 参照）
2. **`Owned Reads` 非適用根拠**: `Owned Reads` は X 公式の個人アカウント向け読み込み枠であり、複数顧客向け SaaS のコスト計算には適用しない。本サービスは各ユーザーの tweet read を原価として計算する。
3. **Usage API endpoint**: `GET https://api.twitter.com/2/usage/tweets` でリアルタイム使用量を確認できる。
4. **spending limit**: X Developer Portal の `Spending limit` 設定で月次上限を設定する。
5. **月次上限前停止ロジック**: 上限の 80% に達した時点でバックアップ実行を停止し、ユーザーへ通知する設計とする。

### `docs/COMPLIANCE.md` への追記内容

以下の項目を確認・追記する:

1. **Enterprise プラン適用要否チェックリスト**:
   - 月次 tweet read が 100 万件を超える場合 → Enterprise プラン確認必須
   - 複数顧客向けに同一 token でアクセスする場合 → Enterprise 要件確認
   - v0 スコープ（`tweet.read`, `users.read`, `offline.access`）ではまず Pro 以下で充足するか確認する
2. **24 時間削除 SLA**:
   - ユーザーが削除リクエストを発行した場合、24 時間以内に backup data・proof data・session token を削除する。
   - 削除完了を audit log に記録する。
3. **API access 終了時全削除 runbook**:
   - Step 1: X API token を revoke する。
   - Step 2: `backup_runs` テーブルの当該 `x_account_id` レコードを削除する。
   - Step 3: `proof_pages` テーブルの当該 `x_account_id` レコードを削除する。
   - Step 4: session token を削除する。
   - Step 5: audit log に削除完了・タイムスタンプ・担当者を記録する。

### 完了条件

- [ ] `git status --short --branch` で tracked 差分（docs のみ）を確認する。
- [ ] `git diff --check` pass
- [ ] `npx tsc -p tsconfig.json --noEmit` pass（docs 変更のみなので pass するはず）
- [ ] docs 変更を `git add docs/API_COST_MODEL.md docs/COMPLIANCE.md` → commit → push する。
- [ ] push 結果（commit hash）を `company/notes/2026-06-07-midday-xguard-implementation.md` に記録する。

### 検証条件

- `git diff --check` pass
- `tsc --noEmit` pass
- push 完了を commit hash で確認する

### MyLife への記録

- 実装結果と検証ログを `company/notes/2026-06-07-midday-xguard-implementation.md` に残す（本ファイルと分けて新規作成）。
- PM ticket `company/pm/tickets/2026-06-07-xguard-unstaged-supabase-docs.md` の `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` 行を完了に更新する。

### push 先

- `UryuAtsuya/Xguard` `origin/main`
- DNS / 権限 blocker の場合は理由・commit hash・次の操作を `company/notes/2026-06-07-midday-xguard-implementation.md` に記録する。

---

## 判断ルール（引き継ぎ）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。自動 DM・自動 follow/unfollow・自動投稿・bulk outreach・BAN 回避導線は追加しない。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない。
- production code を MyLife Vault 内へ置かない。
- `output/playwright/` 未追跡は今回触らない。
- force push しない。remote 先行確認後に push する。

---

## 未解決事項（引き継ぎ）

- **Top 2 (Supabase integration test)**: DB URL / psql なし環境ではスキップ継続。本番環境または Supabase CLI でのローカル起動を要する。Top 3 完了後、次サイクルで再挑戦する。
- **OAuth configured mode**: 実 X token exchange 未実装は P0 継続。明日の Top 1 として確定（CEO 判断済み: `company/decisions/2026-06-07.md` 参照）。
- **GitHub DNS 解決失敗**: live remote 確認は CI 環境推奨。push 自体は成功しているため実害なし。
- `npm run build:api` / `npm run build:web` の `EPERM`: writable clone での build 確認を推奨。今回は docs のみなので影響なし。
