---
date: "2026-06-05"
project: "xguard"
type: codex-handoff
status: ready
---

# 2026-06-05 Codex 昼実装 ハンドオフ

## 判断根拠

今日の朝会で確認した Top 3 は次のとおり。

1. OAuth configured mode に一回限り `state`、S256 PKCE、callback validation、TTL、replay 防止を実装しテストを追加する。
2. backup / proof API へ認証・user ownership・proof visibility/revocation 境界を追加しテストを入れる。
3. 実 Supabase/Postgres 検証と `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` の反映。

**昼実装の対象は Top 1 に絞る。** 理由は次のとおり。

- OAuth CSRF/replay 防止は P1 セキュリティ要件であり、Top 2 の backup/proof 認証より前に閉じるべきである。
- スコープが明確（start エンドポイントで state/PKCE 発行、callback で照合、TTL/replay 拒否）で、HTTP 境界テストにより pass/fail を確認しやすい。
- Top 2 以降は Top 1 完了後に並行可能であるが、OAuth state 管理が未実装のまま backup/proof API に認証を追加しても整合しない。

---

## Codex への実装指示

### 対象リポジトリ

- **実装コード**: `/Users/uryuatsuya/XGuard/xguard`
  - 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-05`（朝会で確認済み）
- **MyLife 記録先**: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`（コードは置かない）

### 起点コミット

`394a3c3 Add OAuth diagnostic HTTP boundary tests` (HEAD = origin/main = local main)

### 触ってよいディレクトリ・ファイル

| パス | 変更内容 |
|---|---|
| `backend/src/config/runtimeConfig.ts` | OAuth state TTL（例: 300秒）と PKCE verifier 長（例: 64 bytes）をランタイム設定として追加 |
| `backend/src/app.ts` | `/api/x/oauth/start` で one-time `state` と S256 PKCE `code_challenge` を発行・保存、`/api/x/oauth/callback` で state 照合・有効期限確認・replay 拒否を実施 |
| `backend/src/repositories/oauthStateRepository.ts`（新規） | `state` の保存・照合・失効・再利用拒否インターフェースと in-memory 実装。本番用 Supabase 実装は任意 |
| `backend/src/__tests__/api.test.ts` | S256 PKCE 正常フロー、state mismatch 拒否（403）、expired state 拒否（403）、replay 拒否（403）、OAuth scope 維持（`tweet.read users.read offline.access`）のテストを追加 |
| `docs/API_SPEC.md` | OAuth start / callback の state・PKCE・TTL・replay 防止の挙動を反映 |

### 触らないもの

- `backend/src/services/` の backup / proof 実装（Top 2 は昼実装スコープ外）
- `backend/src/repositories/supabaseTokenRepository.ts` および `tokenRepository.ts`
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`（Top 3）
- `docs/API_COST_MODEL.md`、`docs/COMPLIANCE.md`（Top 3）
- `frontend/`（今日は backend のみ）
- `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/`（production code を置かない）
- `output/playwright/`（未追跡、触らない）

### 期待する変更

1. **OAuth start** (`/api/x/oauth/start`):
   - `crypto.randomBytes(32)` 等で one-time `state` を生成し OAuthStateRepository へ TTL 付きで保存する。
   - S256 PKCE: `code_verifier = base64url(randomBytes(64))`、`code_challenge = base64url(sha256(verifier))`。
   - `code_verifier` は repository に一時保存するかセッションに紐付け、frontend へは返さない。
   - レスポンスに `state` と `code_challenge` を含め、認可 URL 構築に使用できるようにする。

2. **OAuth callback** (`/api/x/oauth/callback` or `/api/x/oauth/token`):
   - request の `state` と repository の `state` を比較し不一致なら 403。
   - TTL 超過なら 403（`state expired`）。
   - 使用済み `state` を削除し、2 回目の同一 `state` には 403（replay）。
   - 正常時のみ token 交換へ進む。

3. **テスト追加** (`api.test.ts`):
   - Happy path: start → state/PKCE 受け取り → callback 成功。
   - state mismatch: callback に異なる state → 403。
   - expired: TTL を短くして時間経過後に callback → 403。（`vi.useFakeTimers` 利用可）
   - replay: 同じ state で 2 回 callback → 2 回目 403。
   - scope: start レスポンスに `tweet.read users.read offline.access` が含まれるか確認。

### 完了条件

- [ ] `git diff --check` が pass する。
- [ ] `npx tsc -p tsconfig.json --noEmit` が pass する。
- [ ] `npx vitest run --configLoader runner backend/src/__tests__/api.test.ts` で OAuth 新テスト含め pass する。
- [ ] `npm run test` が pass する（既存テスト全 pass を維持）。
- [ ] `npm run build` が pass する。
- [ ] `npm run check` が pass する。
- [ ] state mismatch / expired / replay の各ケースが 403 を返すことをテストで確認する。
- [ ] `code_verifier` が frontend へ返らないことを実装またはテストで確認する。

### 検証コマンド（順番に実行）

```bash
# 1. 型チェック
npx tsc -p tsconfig.json --noEmit

# 2. OAuth 新テスト単体
npx vitest run --configLoader runner backend/src/__tests__/api.test.ts

# 3. 全テスト
npm run test

# 4. ビルド
npm run build

# 5. リント・型チェック統合
npm run check

# 6. diff 確認
git diff --check
git diff --cached --check
```

### push 手順

```bash
# XGuard 実装 repo
git -C /Users/uryuatsuya/XGuard/xguard add backend/src/config/runtimeConfig.ts \
  backend/src/app.ts \
  backend/src/repositories/oauthStateRepository.ts \
  backend/src/__tests__/api.test.ts \
  docs/API_SPEC.md
git -C /Users/uryuatsuya/XGuard/xguard commit -m "feat: add one-time state, S256 PKCE, TTL, and replay prevention to OAuth configured mode"
git -C /Users/uryuatsuya/XGuard/xguard push origin main
```

push 失敗（`could not resolve host` 等）の場合は、未 push の commit hash と理由を夜レビューメモへ記録する。force push は行わない。

### MyLife 側へ戻す記録先

| 記録先 | 内容 |
|---|---|
| `company/notes/2026-06-05-midday-xguard-implementation.md` | 実装スライス、変更内容、verification 結果、push 状態 |
| `company/projects/x-ban-recovery-storage/notes/2026-06-05-xguard-oauth-proof-supabase-compliance.md` | OAuth one-time state/PKCE 完了可否、次の Top 2/3 への引き継ぎ |
| `company/todos/2026-06-05.md` | Top 1 完了チェック |

---

## 実行時の注意点

- `/Users/uryuatsuya/XGuard/xguard` は朝の確認で `writable=no` だった。実行前に `touch /Users/uryuatsuya/XGuard/xguard/.write_test && rm /Users/uryuatsuya/XGuard/xguard/.write_test` で書き込み可否を再確認する。書き込み不可の場合は `cp -r /Users/uryuatsuya/XGuard/xguard /private/tmp/xguard-midday-2026-06-05` して作業し、push は正本パスの git remote を使う。
- `state` の保存は in-memory Map で十分（Supabase 連携は Top 2 以降）。TTL は環境変数 `OAUTH_STATE_TTL_SECONDS`（default 300）で変更できるようにする。
- `code_verifier` は response body に含めない。必要なら HttpOnly Cookie か backend session に保存する。
- v0 scope は `tweet.read users.read offline.access` に固定。`follows.read`、DM/write 系は追加しない。
- 実 Supabase 接続（`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`）は Top 3 なので今回は不要。
- MyLife の `Projects/`, `Ideas/`, `memo/` は未追跡のまま触らない。
