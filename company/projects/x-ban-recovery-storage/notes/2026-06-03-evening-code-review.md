---
date: "2026-06-03"
project: "xguard"
type: project-evening-code-review
status: reviewed
---

# 2026-06-03 夜レビュー

## 結論

指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled`、working tree clean。`03ecd2f` は `/api/x/oauth/status` を未設定時に404へ倒し、既定公開の事故を防ぐため、昼の一時commit `9e8b7c5` は丸ごとpushしない。

release gateはまだ閉じない。診断endpointを明示有効化した場合の無認証公開、OAuth `state` / S256 PKCE / callback validation、実Supabase/Postgres integration test、Developer Console原価確認が残っている。

## レビュー結果

- P0: なし。
- P1: `X_OAUTH_STATUS_EXPOSURE=deployment_diagnostic` 有効時の `/api/x/oauth/status` が無認証。header secret、admin auth、private health checkのいずれかが必要。
- P1: OAuth configured modeは固定 `state`、`plain` PKCE、callback未照合。
- P2: `npm run check` は `dist/` write `EPERM` で未完走。
- P2: status route testはExpress内部route stack直呼びで、HTTP境界テストが不足。

## 検証

- `git diff --check`: pass
- `git diff --cached --check`: pass
- targeted Vitest `backend/src/__tests__/api.test.ts`: pass、10 tests
- `tsc --noEmit`: pass
- `npm run test`: pass、45 passed / 2 skipped
- `build:api`: `dist/backend/...` write `EPERM`
- `build:web`: `dist/frontend/assets` rm `EPERM`
- `git fetch origin main`: `.git/FETCH_HEAD: Operation not permitted`

## 次

1. `deployment_diagnostic` 有効時の診断endpoint制限を入れる。
2. 実Supabase/Postgres SQL integration testを実行する。
3. OAuth `state` / S256 PKCE / callback validation / token schema契約とDeveloper Console原価確認を閉じる。

## 最終追記

- 最終確認で `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=6024667 Restrict production CORS origins` へ進んでいた。
- `6024667` はproduction CORSを `APP_BASE_URL` / `CORS_ORIGINS` ベースへ寄せるcommitで、CORSのP2は進展。
- 追加検証: `git diff --check`、`tsc --noEmit`、targeted Vitest（12 tests）、`npm run test`（47 passed / 2 skipped）pass。
