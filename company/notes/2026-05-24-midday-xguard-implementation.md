---
created: "2026-05-24"
type: midday-xguard-implementation
project: "xguard"
status: implemented-after-write-access-restored
---

# 2026-05-24 XGuard 昼実装メモ

## 実行時刻

- System date: `2026-05-24 13:33:54 JST`

## 今日のゴール

朝会のスコープに沿って、`/Users/uryuatsuya/XGuard/xguard` に `supabase/schema.sql`、`shared/types.ts`、read-only構成docsを作る。

## 確認した前提

- XGuard v0は「BAN復活」ではなく、「本人が事前に許可したXデータのread-onlyバックアップ」と「BAN後の再起動支援用の証明ページ生成」に限定する。
- v0のwrite scope、自動DM、自動follow/unfollow、自動投稿、bulk outreachは対象外。
- 証明ページはraw X API payloadを公開せず、公開用DTOを分離する。
- X APIはPay-per-use / Owned Reads前提で、API使用量とbackup run単位の原価記録が必要。

## 実装ディレクトリ確認

- Target: `/Users/uryuatsuya/XGuard/xguard`
- Repo status: 既存Git repoあり。最新ローカルcommitは `606eb77 Initialize XGuard docs`。
- Existing files:
  - `/Users/uryuatsuya/XGuard/xguard/README.md`
  - `/Users/uryuatsuya/XGuard/xguard/docs/X_API_SCOPE.md`
  - `/Users/uryuatsuya/XGuard/xguard/docs/IMPLEMENTATION_GATE.md`
- Write check:
  - `test -w /Users/uryuatsuya/XGuard/xguard` => `not_writable`
  - `mkdir -p /Users/uryuatsuya/XGuard/xguard/supabase` => `Operation not permitted`
  - `mkdir -p /Users/uryuatsuya/XGuard/xguard/shared` => `Operation not permitted`

## 今日作成した代替成果

指定実装repoへ直接書けないため、実装コードをMyLife Vault内へ迂回配置せず、計画正本として以下を作成した。

- `company/projects/x-ban-recovery-storage/technical/supabase-v1-schema-draft.sql`
  - OAuth token暗号化保管前提の `x_oauth_connections`
  - API使用量記録の `api_usage_events`
  - backup run記録の `backup_runs`
  - proof page公開制御の `proof_pages`
  - X Content削除/変更追従の `content_compliance_events`
  - Stripe webhook冪等性の `stripe_events`
- `company/projects/x-ban-recovery-storage/technical/shared-types-v1-draft.md`
  - `shared/types.ts` へ移すための型ドラフト
  - `ProofPublicPayload` とraw X API payloadの分離
  - `BackupRunStatus`、`ProofPageVisibility`、`ContentComplianceEventType`、`ApiUsageEvent` を追加

## 検証

- 実施:
  - `date '+%Y-%m-%d %H:%M:%S %Z'`
  - `git -C /Users/uryuatsuya/XGuard/xguard status --short`
  - `git -C /Users/uryuatsuya/XGuard/xguard log --oneline -5`
  - `test -w /Users/uryuatsuya/XGuard/xguard`
  - `mkdir -p /Users/uryuatsuya/XGuard/xguard/supabase`
  - `mkdir -p /Users/uryuatsuya/XGuard/xguard/shared`
- 未実施:
  - XGuard repoへの `supabase/schema.sql` / `shared/types.ts` 作成
  - Next.js / Express scaffold
  - `npm install`
  - `npm run build`
  - `tsc --noEmit`
  - XGuard repo commit

## ブロッカー

Codexの現在の実行環境から `/Users/uryuatsuya/XGuard/xguard` は読み取り可能だが書き込み不可。実装repo自体は存在するため、次はこのパスをCodexのwritable rootに入れるか、ユーザー側で同内容を適用する。

## 夜レビューへの引き継ぎ

1. `/Users/uryuatsuya/XGuard/xguard` への書き込み権限をCodex実行環境に付与し、`supabase/schema.sql` と `shared/types.ts` を作成する。
2. `supabase-v1-schema-draft.sql` をレビューし、OAuth token暗号化、proof page公開制御、compliance queue、Stripe webhook冪等性の漏れを確認する。
3. Developer Consoleでendpoint別単価とspending limitを確認し、`API_COST_MODEL.md` の前提へ反映する。

## 追記: 2026-05-24 14:12 JST 実装再開

`/Users/uryuatsuya/XGuard/xguard` が書き込み可能になっていたため、昼会ドラフトを実装repoへ反映し、backend-firstの初回プロトタイプを作成した。

### 作成・更新した実装repo成果物

- `package.json`, `package-lock.json`, `tsconfig.json`, `vitest.config.ts`
- `shared/types.ts`
- `supabase/schema.sql`
- `backend/src/app.ts`
- `backend/src/server.ts`
- `backend/src/repositories/tokenRepository.ts`
- `backend/src/clients/xApiClient.ts`
- `backend/src/services/mockBackupService.ts`
- `backend/src/services/proofDtoBuilder.ts`
- `backend/src/fixtures/mockXData.ts`
- `backend/src/__tests__/api.test.ts`
- `backend/src/__tests__/proofDtoBuilder.test.ts`
- `docs/API_SPEC.md`
- `README.md`

### API / backend洗い出し

- v0で必要なAPI境界:
  - `GET /health`
  - `GET /api/x/oauth/start`
  - `GET /api/x/oauth/callback`
  - `POST /api/backup/run`
  - `GET /api/backup/status/:runId`
  - `GET /api/recovery/:runId/proof`
- 置き換え前提のbackend interface:
  - `TokenRepository`: in-memoryからSupabase service role + Vault/encryptionへ移行
  - `XApiClient`: fixtureからX API read-only endpointsへ移行
  - `MockBackupService`: backup transaction、snapshot保存、API usage/rate limit記録へ移行
- v0対象外として維持:
  - 自動DM
  - 自動follow/unfollow
  - 自動投稿
  - BAN回避
  - raw X API payload公開

### 検証

- `npm install`: pass
- `npm run check`: pass
  - `tsc -p tsconfig.json`: pass
  - `vitest run`: 2 files / 2 tests pass
- `npm run dev:api`: 起動確認済み
- `curl http://localhost:4000/health`: `ok: true`
- `curl -X POST http://localhost:4000/api/backup/run -d '{"tweetLimit":2}'`: mock backup `completed` と proof DTO 生成を確認

### 夜レビューへの更新引き継ぎ

1. `supabase/schema.sql` のOAuth token暗号化方針をSupabase Vault前提でレビューする。
2. X Developer Consoleでendpoint別単価とspending limitを確認し、API原価モデルを `docs/API_COST_MODEL.md` として追加する。
3. 次の実装はSupabase repository層とStripe webhook idempotencyのどちらを先に進めるか決める。
