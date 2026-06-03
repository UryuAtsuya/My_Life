---
date: "2026-06-03"
project: "xguard"
type: project-midday-implementation
status: completed_local_unpushed
---

# 2026-06-03 昼実装メモ

## 結論

今日の昼は、朝会でP1 blockerになっていた `/api/x/oauth/status` のproduction公開制御を小さく閉じた。productionでは `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` と `x-xguard-diagnostic-token` headerが一致した場合のみstatus responseを返す。

XGuard local commitは `/private/tmp/xguard-midday-2026-06-03-1339` の `9e8b7c5 Guard OAuth status diagnostic in production`。pushはremote先行のため拒否され、fetch/ls-remoteはDNS失敗で未完了。

最終確認で、指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled` へ進んでいた。`03ecd2f` は `X_OAUTH_STATUS_EXPOSURE` 未設定時にstatus endpointを404へ倒し、`deployment_diagnostic` 明示時だけ有効化する方式。次回は `03ecd2f` を正として `9e8b7c5` の必要差分だけ確認する。

## 実装差分

- Runtime configに `NODE_ENV` と `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` を追加。
- `/api/x/oauth/status` にproduction diagnostic token gateを追加。
- status responseは `X_CLIENT_ID` 値、`X_CLIENT_SECRET` 値、diagnostic token値、token materialを返さない。
- `docs/API_SPEC.md` と `docs/DEPLOY.md` にproduction access条件とenvを反映。

## 検証

- `git diff --check`: pass
- `git diff --cached --check`: pass
- targeted Vitest `backend/src/__tests__/api.test.ts`: pass（7 tests）
- `tsc --noEmit`: pass
- `npm run build:api`: pass
- `npm run build:web -- --configLoader runner`: pass
- `npm run test`: pass（42 passed / 2 skipped）
- `npm run check`: `node_modules/.vite-temp` write `EPERM` で環境blocker

## 未完了

- `03ecd2f` と `9e8b7c5` の差分確認。`9e8b7c5` を丸ごとpushしない。
- 実Supabase/Postgres integration test。
- OAuth `state` / S256 PKCE / callback validation。
- token repositoryとSupabase schema保存契約の一本化。
- Developer Console原価実値確認。
