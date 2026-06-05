---
date: "2026-06-05"
project: "xguard"
type: midday-implementation
status: push-blocked
---

# 2026-06-05 XGuard OAuth state / PKCE 実装メモ

## 完了

- `/private/tmp/xguard-midday-2026-06-05` で `9374f4e Add one-time OAuth state and S256 PKCE` を作成した。
- `/api/x/oauth/start` は一回限り `state` と S256 PKCE `code_challenge` を発行する。
- `code_verifier` はbackend側 `OAuthStateRepository` に保存し、API responseへ返さない。
- `/api/x/oauth/callback` は `state` 不一致、期限切れ、replayを403で拒否する。
- v0 scopeは `tweet.read`, `users.read`, `offline.access` に維持した。
- `docs/API_SPEC.md` にstart/callbackの境界を反映した。

## 未完

- push未完。`git push origin main` は `Could not resolve host: github.com`。
- 正本 `/Users/uryuatsuya/XGuard/xguard` は書き込み不可のまま。
- `npm run check` はsymlinked `node_modules/.vite-temp` 書き込み `EPERM` のため未完。代替で `tsc`、targeted Vitest、全Vitest、build、runner指定web buildはpass。

## 次の実装順

1. `9374f4e` をremote先行分確認後にpushする。
2. 通常writable checkoutまたはCIで `npm run check` を再実行する。
3. backup / proof APIの認証・所有権・visibility/revocation境界へ進む。
4. 実Supabase/Postgres integration testとcost/compliance docs更新を閉じる。
