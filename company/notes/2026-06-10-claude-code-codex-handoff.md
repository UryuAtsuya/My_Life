---
date: "2026-06-10"
project: "xguard"
type: codex-handoff
scheduled: "12:45"
---

# 2026-06-10 12:45 Codex 昼ハンドオフ

## 今日の優先順位と背景

`7e33e9f Guard production OAuth callback boundary` が **4 日目未 push**。Codex 昼 run が 3 日連続未実施。今日は Top 1 → Top 2 の順に必ず完了させる。

---

## 実装対象（優先順）

### 【Top 1】`7e33e9f` rebase + verify + push（最優先・本日必須）

**対象リポジトリ:** `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-10` へ `git clone git@github.com:UryuAtsuya/Xguard.git` して作業する

**現在の git 状態（12:45 時点確認済み）:**

| 項目 | 内容 |
|------|------|
| local HEAD | `7e33e9f Guard production OAuth callback boundary` |
| remote origin/main | `c4403d8 Document XGuard release gates` |
| diverge | `9ac4f2f` から分岐。local ahead 1 / remote ahead 1 |

**実行手順（この順番で実行する）:**

```bash
cd /Users/uryuatsuya/XGuard/xguard
git fetch origin
git log --oneline origin/main..HEAD   # 期待: 7e33e9f のみ
git log --oneline HEAD..origin/main   # 期待: c4403d8 のみ
git rebase origin/main
git diff --check
npx tsc -p tsconfig.json --noEmit
npx vitest run --configLoader runner
git push origin main
```

**完了条件:**
- `git rebase origin/main` が conflict なしで完了する
- `git diff --check` が clean
- `npx tsc -p tsconfig.json --noEmit` が 0 errors
- `npx vitest run --configLoader runner` が全テスト pass
- `git push origin main` が成功する（force push 禁止）
- push 後の commit hash を記録する

**conflict 発生時:** 中断し、状態を `company/notes/2026-06-10-midday-xguard-implementation.md` に記録して Claude Code へ戻す。

---

### 【Top 2】`runtimeConfig.ts` runtime gate 実装（本日必須）

Top 1 が完了してから着手する。

**対象リポジトリ:** 同上 `/Users/uryuatsuya/XGuard/xguard`

**触ってよいファイル:**

| パス | 変更内容 |
|------|----------|
| `backend/src/config/runtimeConfig.ts` | production 起動チェックに gate 追加 |
| `backend/src/__tests__/runtimeConfig.test.ts` | 5 ケースのテスト追加（ファイルが存在しない場合は新規作成） |
| `docs/IMPLEMENTATION_GATE.md` | Go 条件に 2 行追加（該当セクションが存在する場合のみ） |

**`runtimeConfig.ts` に追加する実装:**

```typescript
if (nodeEnv === "production" && env.PRICING_CONFIRMED?.trim() !== "true") {
  throw new Error("invalid_runtime_env:PRICING_CONFIRMED");
}
if (nodeEnv === "production" && env.COMPLIANCE_CONFIRMED?.trim() !== "true") {
  throw new Error("invalid_runtime_env:COMPLIANCE_CONFIRMED");
}
```

既存の production gate チェックブロックに続けて追加する。配置位置は既存の `NODE_ENV=production` 条件チェックの近く。

**テストケース（5 件・全て必須）:**

1. `NODE_ENV=production` かつ `PRICING_CONFIRMED` 未設定 → `Error("invalid_runtime_env:PRICING_CONFIRMED")` を throw する
2. `NODE_ENV=production` かつ `PRICING_CONFIRMED=false` → `Error("invalid_runtime_env:PRICING_CONFIRMED")` を throw する
3. `NODE_ENV=production` かつ `PRICING_CONFIRMED=true` かつ `COMPLIANCE_CONFIRMED` 未設定 → `Error("invalid_runtime_env:COMPLIANCE_CONFIRMED")` を throw する
4. `NODE_ENV=production` かつ `PRICING_CONFIRMED=true` かつ `COMPLIANCE_CONFIRMED=true`（他の必須 env 揃い） → エラーなし
5. `NODE_ENV=development` かつ `PRICING_CONFIRMED` / `COMPLIANCE_CONFIRMED` 両方未設定 → エラーなし

**完了条件:**

```bash
git diff --check
npx tsc -p tsconfig.json --noEmit
npx vitest run --configLoader runner backend/src/__tests__/runtimeConfig.test.ts
```

全 pass 後に commit → push する。

---

## 触らないもの（絶対禁止）

- `output/playwright/`（未追跡ファイル。今回も触らない）
- `docs/API_COST_MODEL.md`（更新済み・変更不要）
- `docs/COMPLIANCE.md`（更新済み・変更不要）
- `frontend/`（今回は backend config のみ）
- **MyLife Vault への production code 配置は禁止**（`/Users/uryuatsuya/Documents/ObsidianVault/MyLife` に実装コードを置かない）
- force push 禁止（`git push --force` / `git push -f` は使わない）

---

## 実行してほしい検証（変更前後で必ず実行）

```bash
git diff --check
npx tsc -p tsconfig.json --noEmit
npx vitest run --configLoader runner
```

Top 2 完了後は targeted test も追加:

```bash
npx vitest run --configLoader runner backend/src/__tests__/runtimeConfig.test.ts
```

`npm run check` は `dist/` 書き込み EPERM が発生する環境では skip してよい。`tsc --noEmit` と targeted Vitest で代替する。

---

## MyLife 側への記録先

完了後または中断時に `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/company/notes/2026-06-10-midday-xguard-implementation.md` を新規作成し、以下を記録する:

- Top 1: rebase 後の commit hash と push 結果（成功/失敗）
- Top 2: targeted Vitest pass ログと push 完了確認
- 未解決事項・conflict・エラーがあれば詳細と次のアクション

記録後に MyLife repo を `git commit` / `git push` する。

---

## 今日 Codex がやらなくてよいこと

- **Top 3（Supabase CLI 環境確保）**: CEO 手動タスク。Codex は触らない。
- `output/playwright/` 未追跡ファイルの commit 判断
- OAuth live credentials 検証（runtime gate 完了後フェーズ）
- `InMemoryOAuthStateRepository` multi-instance 対応（P1 継続・今回スコープ外）

---

## 判断ルール（継続）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない
- `prototype user header`（`x-xguard-user-id`）は production 認証として扱わない
- production code を MyLife Vault に置かない

---

## 参照ドキュメント

- `company/notes/2026-06-10-morning-planning.md` — Top 2 手順の全文
- `company/decisions/2026-06-10.md` — CEO 判断一覧
- `company/todos/2026-06-10.md` — 今日の TODO
