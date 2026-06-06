---
date: "2026-06-06"
project: "xguard"
type: codex-handoff
status: ready
---

# 2026-06-06 Codex 昼実装 ハンドオフ

## 判断根拠

今日の朝会 Top 3 は次のとおり。

1. backup / proof API へ認証、user ownership、proof visibility/revocation 境界を追加し、他 user・private・revoked proof 拒否テストを入れる。
2. 実 Supabase/Postgres で `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role・ownership・同一 X アカウント・存在しない `backup_run`・`x_account_id` 必須・負値・月次上限超過を確認する。
3. `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` に通常 read 単価・`Owned Reads` 非適用・Usage endpoint・spending limit・24 時間削除 SLA・全削除 runbook・Enterprise 確認を反映する。

**昼実装の対象は Top 1（backup / proof API 認証・所有権・proof boundary）に絞る。**

理由:
- P1 セキュリティ要件（IDOR、private/revoked proof の無認証公開）を最初に閉じることで production release の主要 No-Go を1件解消できる。
- 変更対象が `backend/src/app.ts` の3エンドポイントと新規テストファイルに限定され、HTTP 境界テストで pass/fail を確認しやすい。
- Top 2 は実 Supabase DB URL + psql が必要であり、sandbox 環境では skip される可能性が高い。Top 3 はドキュメント更新のみで合意済みのため昼実装の優先度が下がる。

---

## Codex への実装指示

### 対象リポジトリ

- **実装コード**: `/Users/uryuatsuya/XGuard/xguard`（書き込み可であることを確認済み）
  - 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-06` へ `git clone git@github.com:UryuAtsuya/Xguard.git` して使う
- **MyLife 記録先**: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`（production code を置かない）

### 起点コミット

`2b96993 Add OAuth state and PKCE guard` （HEAD = origin/main = local main）

### git 状態確認

```bash
git -C /Users/uryuatsuya/XGuard/xguard status --short --branch
git -C /Users/uryuatsuya/XGuard/xguard rev-parse --short HEAD
git -C /Users/uryuatsuya/XGuard/xguard rev-parse --short origin/main
git ls-remote origin refs/heads/main   # DNS 失敗なら理由と next action を記録する
```

### 触ってよいファイル

| パス | 変更内容 |
|------|----------|
| `backend/src/app.ts` | セッション管理の追加、auth middleware の適用、backup/proof エンドポイントへの ownership・visibility・revocation チェック追加 |
| `backend/src/repositories/sessionRepository.ts`（新規） | sessionToken → userId/xAccountId のインメモリストア |
| `backend/src/__tests__/backupProofAuth.test.ts`（新規） | 認証・所有権・visibility/revocation 境界テスト |
| `backend/src/services/mockBackupService.ts` | 戻り値に `visibility` / `revokedAt` を追加する場合のみ変更可 |

### 触らないもの

- `output/playwright/`（未追跡ファイル。commit/delete 判断は今回行わない）
- `frontend/`（今回は backend のみ）
- `docs/API_COST_MODEL.md`、`docs/COMPLIANCE.md`（Top 3 スコープ外）
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`（Top 2 スコープ外）
- `shared/types.ts`（追加が必要な場合は最小限、削除・改名はしない）
- `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/`（実装コードを置かない）

### 既存コード把握

- `shared/types.ts` に `ProofPageVisibility = "private" | "unlisted" | "public" | "revoked"`、`ProofPage`（`userId`、`visibility`、`revokedAt` 付き）が定義済み。
- `BackupRun`（`shared/types.ts`）に `userId` フィールドはない。`xAccountId` のみ。
- `app.ts` の `backupRuns` は `Map<string, Awaited<ReturnType<MockBackupService["runBackup"]>>>` であり、ユーザー情報を持たない。
- `POST /api/backup/run`、`GET /api/backup/status/:runId`、`GET /api/recovery/:runId/proof` は現在無認証。
- OAuth callback は `fixtureAccount.id` を `xAccountId` として token を保存し、`connectedAccount` を返すが session token を返さない。

### 期待する変更

#### 1. セッション管理（`backend/src/repositories/sessionRepository.ts` 新規作成）

```typescript
// シンプルなインメモリストア: sessionToken → userId（xAccountId）
interface SessionRepository {
  save(sessionToken: string, userId: string): Promise<void>;
  lookup(sessionToken: string): Promise<string | undefined>;
}
```

#### 2. OAuth callback 変更（`backend/src/app.ts`）

`POST /api/x/oauth/callback` 成功時に:
- `crypto.randomBytes(32).toString("base64url")` でセッショントークンを生成する。
- `sessionRepository.save(sessionToken, xAccountId)` で保存する。
- レスポンスに `sessionToken` を追加して返す。

#### 3. バックアップ実行ストア変更（`backend/src/app.ts`）

```typescript
// backupRuns の値型を拡張する
type BackupRunEntry = {
  userId: string;
  visibility: "public" | "unlisted" | "private" | "revoked";
  revokedAt: string | null;
  backupRun: Awaited<ReturnType<MockBackupService["runBackup"]>>["backupRun"];
  proofPayload: Awaited<ReturnType<MockBackupService["runBackup"]>>["proofPayload"];
};
const backupRuns = new Map<string, BackupRunEntry>();
```

#### 4. Auth middleware（`backend/src/app.ts` 内、または別ファイル）

```typescript
function requireAuth(
  request: express.Request,
  response: express.Response,
  next: express.NextFunction,
): void {
  const auth = request.get("Authorization");
  const token = auth?.startsWith("Bearer ") ? auth.slice(7) : undefined;
  if (!token) {
    response.status(401).json({ error: "authentication_required" });
    return;
  }
  sessionRepository.lookup(token).then((userId) => {
    if (!userId) {
      response.status(401).json({ error: "invalid_session" });
      return;
    }
    (request as express.Request & { userId: string }).userId = userId;
    next();
  });
}
```

#### 5. `POST /api/backup/run` 変更

- `requireAuth` を適用し、`req.userId` を取得する。
- `backupRuns.set(result.backupRun.id, { userId: req.userId, visibility: "public", revokedAt: null, ...result })` で保存する。

#### 6. `GET /api/backup/status/:runId` 変更

- `requireAuth` を適用する。
- `entry.userId !== req.userId` なら `403 { error: "forbidden" }` を返す。

#### 7. `GET /api/recovery/:runId/proof` 変更

- `requireAuth` を適用する。
- `entry.userId !== req.userId` なら `403 { error: "forbidden" }` を返す。
- `entry.visibility === "private"` なら `404 { error: "proof_not_found" }` を返す。
- `entry.revokedAt != null` なら `404 { error: "proof_not_found" }` を返す。

### 追加するテスト（`backend/src/__tests__/backupProofAuth.test.ts` 新規）

supertest を使った HTTP 境界テスト。`createApp()` を使い in-memory で完結させる。

| テスト名 | 想定シナリオ | 期待する HTTP レスポンス |
|----------|-------------|--------------------------|
| 認証なしで backup/run が拒否される | Authorization ヘッダーなし | 401 |
| 認証なしで backup/status が拒否される | Authorization ヘッダーなし | 401 |
| 認証なしで proof が拒否される | Authorization ヘッダーなし | 401 |
| 他ユーザーの backup/status にアクセスできない | 別ユーザーの sessionToken を使用 | 403 |
| 他ユーザーの proof にアクセスできない | 別ユーザーの sessionToken を使用 | 403 |
| private proof にアクセスできない | 所有者本人でも visibility=private なら 404 | 404 |
| revoked proof にアクセスできない | 所有者本人でも revokedAt != null なら 404 | 404 |
| 所有者が自分の backup/status を取得できる | 正しい sessionToken で自分の runId | 200 |
| 所有者が自分の proof を取得できる | 正しい sessionToken で自分の runId、visibility=public | 200 |
| 存在しない runId へのアクセスは 404 のまま | 正しい認証で存在しない runId | 404 |

テストの setUp:
1. OAuth callback を経由して sessionToken を取得するか、テスト用に `sessionRepository.save("test-token-a", "user-a")` を直接呼ぶ。
2. `backupRuns.set(...)` をテスト用ヘルパーで直接セットアップする、または `POST /api/backup/run` を呼んで runId を取得する。

### 完了条件

- [ ] `git status --short --branch` で tracked 差分を確認する。
- [ ] `git ls-remote origin refs/heads/main` — 失敗時は理由と next action を記録する。
- [ ] `git diff --check` pass
- [ ] `npx tsc -p tsconfig.json --noEmit` pass（backend ディレクトリにある場合はそちらも）
- [ ] targeted Vitest:
  ```bash
  npx vitest run --configLoader runner \
    backend/src/__tests__/backupProofAuth.test.ts \
    backend/src/__tests__/api.test.ts
  ```
  全テスト pass
- [ ] `npm run check`（writable 環境なら full pass、EPERM の場合は理由を記録）
- [ ] `POST /api/backup/run`、`GET /api/backup/status/:runId`、`GET /api/recovery/:runId/proof` の無認証アクセスが 401 で拒否されること。
- [ ] 他ユーザー・private・revoked proof の拒否テストが pass すること。
- [ ] P1 "無認証 backup/proof" が解消されること。

### MyLife への記録

- 実装結果と検証ログを `company/notes/2026-06-06-midday-xguard-implementation.md` に残す。
- commit/push 状態（XGuard と MyLife を分けて）を記録する。

### push 先

- `UryuAtsuya/Xguard` `origin/main`
- DNS / 権限 blocker の場合は理由・commit hash・次の操作を記録する。

---

## 判断ルール（引き継ぎ）

- v0 scope は `tweet.read`, `users.read`, `offline.access` のみ。自動 DM、自動 follow/unfollow、自動投稿、bulk outreach、BAN 回避導線は追加しない。
- `Owned Reads` を複数顧客向け SaaS の原価前提にしない。
- production code を MyLife Vault 内へ置かない。
- `output/playwright/` 未追跡は今回触らない。

---

## 未解決事項（引き継ぎ）

- GitHub DNS 解決失敗による live remote 確認未完。writable clone 環境か CI で `git ls-remote origin refs/heads/main` を試す。
- `npm run build:api` / `npm run build:web` は `EPERM`。writable checkout での build 確認を推奨。
- frontend `App.test.tsx` 5 秒 timeout 失敗は環境遅延と判断済み。次 run で `--testTimeout=20000` を加えた targeted で再確認する。
- 実 Supabase integration test は DB URL / psql なしでは skip。本番環境または Supabase CLI でのローカル起動を要する（Top 2 の blocker）。
