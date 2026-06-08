---
date: "2026-06-08"
project: "xguard"
type: codex-handoff
status: ready
scheduled: "12:45"
---

# 2026-06-08 Codex 昼実装 ハンドオフ

## 現状サマリ（12:45 時点）

| 項目 | 状態 |
|------|------|
| XGuard local HEAD | `7e33e9f Guard production OAuth callback boundary`（未 push、origin/main [ahead 1] per local tracking） |
| XGuard remote origin/main | `c4403d8 Document XGuard release gates`（昨日昼 temp clone から push 済み） |
| git 状態 | local と remote が `9ac4f2f` から分岐。fetch → rebase が必要 |
| MyLife repo | `a6a9710 Refresh June 7 XGuard morning research`（remote と同期済み） |
| 未追跡 | `output/playwright/`（今日も触らない） |

### 本日 Top 3 進捗

| # | 内容 | 状態 |
|---|------|------|
| Top 1 | OAuth configured mode で実 X token exchange 実装 | ❌ 未着手（live credentials 要） |
| Top 2 | 実 Supabase/Postgres integration test | ❌ blocker（DB URL / `psql` 不足） |
| Top 3 | docs CI/runtime release gate 化 | ❌ 未着手（docs 更新は完了、gate 実装が残る） |

---

## 昼 Codex 実装対象

**Top 3 — runtime release gate 実装** に絞る。

**理由:**
- Top 1 は live X API credentials（`X_CLIENT_ID` / `X_CLIENT_SECRET` / 実 callback URL）が必要。sandbox では verified できない。
- Top 2 は Supabase DB URL と `psql` が依然 blocker。
- Top 3 は外部依存なし。`docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` は `c4403d8` で既に更新済み。残りは「文書上の No-Go を runtime config で機械的に止める仕組み」の実装のみ。tsc + vitest で完全検証可能。

---

## Codex への実装指示

### 対象リポジトリ

- **実装コード**: `/Users/uryuatsuya/XGuard/xguard`
  - 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-08` へ `git clone git@github.com:UryuAtsuya/Xguard.git` して使う
- **MyLife 記録先**: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`（実装コードは置かない）

### git 状態の整合作業（最初に実施）

```bash
cd /Users/uryuatsuya/XGuard/xguard
git fetch origin
git log --oneline origin/main..HEAD  # local-only commits を確認
git log --oneline HEAD..origin/main  # remote-only commits を確認
```

期待結果:
- local-only: `7e33e9f Guard production OAuth callback boundary`
- remote-only: `c4403d8 Document XGuard release gates`

統合方法（衝突がない場合）:

```bash
git rebase origin/main
# または
git merge origin/main --no-ff
```

force push しない。rebase / merge 後、`git push origin main` で push する。

### 起点コミット（整合後）

`c4403d8 Document XGuard release gates` の上に `7e33e9f` が乗った状態（rebase 成功時）

### 触ってよいファイル

| パス | 変更内容 |
|------|----------|
| `backend/src/config/runtimeConfig.ts` | `PRICING_CONFIRMED` / `COMPLIANCE_CONFIRMED` gate を production 起動時チェックに追加 |
| `backend/src/__tests__/runtimeConfig.test.ts` | 新規 gate のテストを追加 |
| `docs/IMPLEMENTATION_GATE.md` | cost/compliance gate を Go 条件として追加・反映 |

### 触らないもの

- `output/playwright/`（未追跡。今回も触らない）
- `docs/API_COST_MODEL.md`（更新済み。今回は編集不要）
- `docs/COMPLIANCE.md`（更新済み。今回は編集不要）
- `frontend/`（今回は backend config のみ）
- `shared/`（今回は backend config のみ）
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`（Top 2 スコープ外）
- `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/`（実装コードを置かない）

### `runtimeConfig.ts` への変更内容

`createRuntimeConfig` の production チェック群に以下を追加する。

```typescript
// production 起動時: PRICING_CONFIRMED=true が必要
if (nodeEnv === "production" && env.PRICING_CONFIRMED?.trim() !== "true") {
  throw new Error("invalid_runtime_env:PRICING_CONFIRMED");
}

// production 起動時: COMPLIANCE_CONFIRMED=true が必要
if (nodeEnv === "production" && env.COMPLIANCE_CONFIRMED?.trim() !== "true") {
  throw new Error("invalid_runtime_env:COMPLIANCE_CONFIRMED");
}
```

`RuntimeConfig` interface に追加する項目はない（env var の存在チェックのみ）。

### `runtimeConfig.test.ts` への追加テスト

以下のケースを追加する。既存テストファイルがある場合はそちらへ追記する。

1. `NODE_ENV=production` かつ `PRICING_CONFIRMED` 未設定 → `invalid_runtime_env:PRICING_CONFIRMED` で throw
2. `NODE_ENV=production` かつ `PRICING_CONFIRMED=false` → `invalid_runtime_env:PRICING_CONFIRMED` で throw
3. `NODE_ENV=production` かつ `PRICING_CONFIRMED=true` かつ `COMPLIANCE_CONFIRMED` 未設定 → `invalid_runtime_env:COMPLIANCE_CONFIRMED` で throw
4. `NODE_ENV=production` かつ `PRICING_CONFIRMED=true` かつ `COMPLIANCE_CONFIRMED=true`（他必須 env 揃い） → エラーなし
5. `NODE_ENV=development` かつ `PRICING_CONFIRMED` / `COMPLIANCE_CONFIRMED` 未設定 → エラーなし

### `docs/IMPLEMENTATION_GATE.md` への追記

「Go 条件」セクションに追加する:

```markdown
- production 起動に `PRICING_CONFIRMED=true` が必要（`runtimeConfig.ts` で強制）。
- production 起動に `COMPLIANCE_CONFIRMED=true` が必要（`runtimeConfig.ts` で強制）。
```

### 完了条件

- [ ] `git fetch origin` 後、local と remote の commit divergence を確認する
- [ ] `git rebase origin/main` または `git merge origin/main` で統合する
- [ ] `runtimeConfig.ts` に `PRICING_CONFIRMED` / `COMPLIANCE_CONFIRMED` gate を追加する
- [ ] `runtimeConfig.test.ts` に上記 5 ケースのテストを追加する
- [ ] `docs/IMPLEMENTATION_GATE.md` を更新する
- [ ] `git diff --check` pass
- [ ] `npx tsc -p tsconfig.json --noEmit` pass
- [ ] targeted Vitest `backend/src/__tests__/runtimeConfig.test.ts` pass（新規ケース含む）
- [ ] commit → push する（push 先: `UryuAtsuya/Xguard` `origin/main`）
- [ ] commit hash と push 結果を `company/notes/2026-06-08-midday-xguard-implementation.md` に記録する

### 検証条件

```bash
git diff --check
npx tsc -p tsconfig.json --noEmit
npx vitest run --configLoader runner backend/src/__tests__/runtimeConfig.test.ts
```

全 pass を確認してから push する。

### MyLife への記録

- 実装結果と検証ログを `company/notes/2026-06-08-midday-xguard-implementation.md` に新規作成する（本ファイルと分けて作成）。
- PM ticket `company/pm/tickets/2026-06-07-xguard-unstaged-supabase-docs.md` の記録を更新する。

### push 先

- `UryuAtsuya/Xguard` `origin/main`
- DNS / 権限 blocker の場合は理由・commit hash・次の操作を `company/notes/2026-06-08-midday-xguard-implementation.md` に記録する。

---

## 判断ルール（引き継ぎ）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。自動 DM・自動 follow/unfollow・自動投稿・bulk outreach・BAN 回避導線は追加しない。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない。
- production code を MyLife Vault 内へ置かない。
- `output/playwright/` 未追跡は今回触らない。
- force push しない。remote 先行確認後に push する。
- `prototype user header`（`x-xguard-user-id`）は production 認証として扱わない。

---

## 未解決事項（引き継ぎ）

- **Top 1 (OAuth token exchange)**: live X credentials 要。sandbox では未検証継続。次サイクルで再挑戦。
- **Top 2 (Supabase integration test)**: DB URL / psql なし環境ではスキップ継続。
- **`InMemoryOAuthStateRepository`**: multi-instance / restart 対応は P1 継続。今回スコープ外。
- **`npm run check` EPERM**: `dist/backend/...` 書き込み権限の問題。writable clone での確認を推奨。今回の変更では影響範囲外。
- **`git ls-remote` DNS 失敗**: push 成功を push 出力で確認する。DNS 解決失敗は実害なし。
