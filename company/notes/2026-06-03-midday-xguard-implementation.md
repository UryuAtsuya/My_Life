---
date: "2026-06-03"
project: "xguard"
type: midday-implementation
status: completed_local_unpushed
---

# 2026-06-03 XGuard 昼実装

## 実装スライス

`/api/x/oauth/status` をproductionで無認証公開しないようにした。`NODE_ENV=production` では `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` が設定され、request header `x-xguard-diagnostic-token` が一致した場合のみstatus responseを返す。非productionでは従来どおりtokenなしで確認できる。

v0 scopeは `tweet.read`, `users.read`, `offline.access` のまま維持した。自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線は追加していない。

## 作業場所

- 正本確認: `/Users/uryuatsuya/XGuard/xguard`
- 正本状態: `HEAD=95e6392`, `main...origin/main`, `writable=no`
- 作業コピー: `/private/tmp/xguard-midday-2026-06-03-1339`
- GitHub実装repo: `UryuAtsuya/Xguard`
- origin: `https://github.com/UryuAtsuya/Xguard.git`

## サブエージェント分担

- Implementation agent: `/api/x/oauth/status` production diagnostic token gateを実装。
- Review agent: security / policy / TypeScript / docs差分をP0/P1/P2でレビュー。
- Verification agent: targeted Vitest、typecheck、build、test、whitespaceを検証。
- Documentation/Sync agent: MyLife更新候補と夜TODOを整理。
- Coordinator: 最終差分確認、P2対応、commit/push試行、MyLife同期を担当。

実サブエージェントは利用できた。`supertest` によるHTTP経路確認はsandboxの `listen EPERM` で使えず、既存のExpress handler直呼びテストで代替した。

## 変更内容

- `backend/src/config/runtimeConfig.ts`: `NODE_ENV` と `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` をruntime configへ追加。
- `backend/src/app.ts`: production時のみ `x-xguard-diagnostic-token` を要求し、不一致または未設定なら `401 oauth_status_diagnostic_token_required` を返す。
- `backend/src/__tests__/api.test.ts`: production token gate、token未設定時の拒否、secret/client id/diagnostic token非露出を追加。
- `docs/API_SPEC.md`: route一覧にproduction access列を追加し、`/api/x/oauth/status` のheader必須を明記。
- `docs/DEPLOY.md`: backend runtime secretとして `X_OAUTH_STATUS_DIAGNOSTIC_TOKEN` を追加。

## Review agent findings

- P0/P1: なし。
- P2: `docs/API_SPEC.md` の表だけ見るとproduction制御を誤認する可能性があったため、Production access列を追加して対応。
- P2: `supertest` で実HTTP header経路を検証するとより堅い。ただしこのsandboxでは `listen EPERM` で失敗したため、handler直呼びテストを維持し、未実施検証として残す。

## Verification

通過:

- `git diff --check`
- `git diff --cached --check`
- `./node_modules/.bin/vitest run --configLoader runner backend/src/__tests__/api.test.ts`（1 file / 7 tests）
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`
- `npm run build:api`
- `npm run build:web -- --configLoader runner`
- `npm run test`（7 passed / 1 skipped files, 42 passed / 2 skipped tests）

未完了 / 環境blocker:

- `npm run check`: Vite既定config loaderが symlinked `node_modules/.vite-temp` へ書こうとして `EPERM`。
- `supertest` status route検証: `listen EPERM: operation not permitted 0.0.0.0`。
- 実Supabase/Postgres integration test: DB URL/credential未提供のため未実行。
- Developer Console原価確認: console accessなし。

## Commit / push

- XGuard local commit: `9e8b7c5 Guard OAuth status diagnostic in production`
- push先: `UryuAtsuya/Xguard` `origin/main`
- push結果: 未push。`git push origin main` はGitHubに到達したが `fetch first` で拒否。
- 追加確認: `git fetch origin main` と `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- 判断: force pushしない。次回、remoteをfetchして先行差分を確認し、`9e8b7c5` をrebase/cherry-pickしてからpushする。

## 追記: 指定パス側の先行反映

push後の最終確認で、指定パス `/Users/uryuatsuya/XGuard/xguard` は `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled` へ進んでいた。履歴には `591c7d7 Gate OAuth status diagnostic exposure` も含まれる。

`03ecd2f` は `X_OAUTH_STATUS_EXPOSURE` 未設定時に `/api/x/oauth/status` を環境名に関係なく404へ倒し、`deployment_diagnostic` 明示時だけstatus responseを返す方式で、今日のP1 blockerに対して `9e8b7c5` と同じ目的をより強く満たしている。次回は `9e8b7c5` をそのままcherry-pickせず、`03ecd2f` を正として必要差分だけ比較する。

指定パス `03ecd2f` の追加検証:

- `git diff --check`: pass
- targeted Vitest `backend/src/__tests__/api.test.ts`: pass（10 tests）
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npm run build:api`: `dist/backend/...` write `EPERM`
- `npm run build:web -- --configLoader runner`: `dist/frontend/assets` rm `EPERM`

## 夜レビューTODO

1. 指定パス `03ecd2f` を正として、`9e8b7c5` に残すべき差分があるか比較し、必要な場合だけrebase/cherry-pickする。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role/grant/ownership/月次上限/負値拒否を確認する。
3. OAuth `state` / S256 PKCE / callback validation / token schema契約とDeveloper Console原価確認を続ける。
