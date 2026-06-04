---
date: "2026-06-04"
project: "xguard"
type: midday-implementation
status: completed_local_unpushed
---

# 2026-06-04 XGuard 昼実装

## 実装スライス

朝会Top 1の `/api/x/oauth/status` 無認証公開を閉じた。`X_OAUTH_STATUS_EXPOSURE=deployment_diagnostic` を有効にしても、32文字以上の `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` とrequest header `x-xguard-diagnostic-token` が一致した場合だけ診断情報を返す。

disabled、token未設定、header欠落、token不一致は同じ404へ寄せ、成功・拒否responseの両方に `Cache-Control: no-store` を付けた。v0 scopeは `tweet.read`, `users.read`, `offline.access` のまま維持した。

## 作業場所

- 正本: `/Users/uryuatsuya/XGuard/xguard`
- 正本状態: `HEAD=origin/main=6024667`, worktree / `.git` ともに `writable=no`
- 作業コピー: `/private/tmp/xguard-midday-2026-06-04-UdD2dZ`
- GitHub実装repo: `UryuAtsuya/Xguard`
- origin: `https://github.com/UryuAtsuya/Xguard.git`

## サブエージェント分担

- Implementation agent: runtime config、診断endpoint、HTTP/fallbackテスト、XGuard docsを実装。
- Review agent: 情報漏えい、token強度、cache、テスト境界をP0/P1/P2でレビュー。
- Verification agent: targeted test、typecheck、全test、build、実DB env有無を確認。
- Documentation/Sync agent: MyLife更新先と夜レビューTop 3を整理。
- Coordinator: 差分統合、Review P1修正、commit/push試行、MyLife同期を担当。

実サブエージェントを利用できた。Reviewで見つかった短token許容と共有cache漏えいリスクは、32文字未満拒否と `Cache-Control: no-store` で修正した。

## 変更内容

- `backend/src/config/runtimeConfig.ts`: `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` を読み込み、32文字未満をruntime config errorで拒否。
- `backend/src/app.ts`: SHA-256 digestと `timingSafeEqual` でheader tokenを比較し、拒否時は情報を出さず404。全responseへ `Cache-Control: no-store` を追加。
- `backend/src/__tests__/api.test.ts`: `supertest` HTTP境界テストと、listen不可sandbox用の常時fallbackテストを追加。
- `docs/API_SPEC.md`, `docs/DEPLOY.md`: 診断token、404統一、no-store、運用解除手順を日本語で反映。

## Review agent findings

- 初回 P1: 診断endpoint無認証公開、実HTTP境界テスト不足。
- 実装後 P1: 短token許容、共有cache漏えい、sandboxでのHTTP test failure。
- 対応: header secret gate、32文字未満拒否、`Cache-Control: no-store`、sandbox fallbackを追加。
- 最終Review: P0/P1/P2なし、merge可能。

## Verification

通過:

- `git diff --check`
- `git diff --cached --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx tsc -p frontend/tsconfig.json --noEmit`
- targeted Vitest: `10 passed / 4 skipped`
- `npm run build`
- `npm run check`: `7 passed / 1 skipped files`, `45 passed / 6 skipped tests`

未実施 / 環境blocker:

- `supertest` HTTP境界4件: sandboxの `listen EPERM` によりskip。通常CIで実行可能なテストは残し、同じ契約をlistener不要fallbackで確認済み。
- 実Supabase/Postgres integration test: `SUPABASE_DB_URL` / `POSTGRES_URL` 未設定、`psql` なし。

## Commit / push

- XGuard local commit: `e31510b89b41de30b6e8318450c2a8f05a2c1966 Guard OAuth deployment diagnostic`
- push先: `UryuAtsuya/Xguard` `origin/main`
- push結果: 未push。`git push origin main` は `Could not resolve host: github.com`。
- 作業コピー状態: `main...origin/main [ahead 1]`
- 判断: force pushしない。DNS復旧後にfetch/divergence確認してpushする。

## 夜レビューTODO

1. `e31510b` をlive `origin/main` と照合してpushし、通常CIで `supertest` HTTP境界4件を実行する。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、Xアカウント整合性、月次上限、負値拒否を確認する。
3. OAuth一回限り `state`、S256 PKCE、callback validation、token repositoryとSupabase schema契約を閉じる。
