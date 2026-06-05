---
date: "2026-06-06"
project: "xguard"
type: evening-code-review
status: completed-with-blockers
---

# 2026-06-06 夜レビュー

XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。local `HEAD` と local tracking `origin/main` は `2b96993 Add OAuth state and PKCE guard` で一致していた。6/5昼時点で未push扱いだったOAuth state / S256 PKCE差分は、今日の正本では反映済み。

production releaseはNo-Go継続。OAuth CSRF/replay blockerは前進したが、backup / proof APIの認証・所有権・visibility/revocation、実Supabase/Postgres検証、cost/compliance release gateが残っている。

## レビュー結果

- P0: なし。
- P1: backup / proof APIはまだ無認証。任意利用者がmock backupを作成し、run idを知っていればproof DTOを読める。
- P1: proof visibility / revocation / owner境界がAPI層にない。
- P1: 実Supabase/Postgres integration testが未実施。今回の実行では対象テストがskip。
- P1: `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` の商用release gateが未完。
- P2: configured OAuth frontendは `authorizationUrl` へ遷移しない。
- P2: `InMemoryOAuthStateRepository` は本番では共有永続storeへ置き換える。

## 検証

- pass: `git diff --check HEAD^ HEAD`, `git diff --check`, `git diff --cached --check`, `npx tsc -p tsconfig.json --noEmit`, backend targeted Vitest, frontend targeted Vitest with `--testTimeout=20000`。
- environment blocker: full `npm run test` はfrontend testの5秒timeout 1件で失敗。targeted timeout延長ではpass。
- environment blocker: `npm run build:api` は `dist/backend/...` 書き込み `EPERM`。
- environment blocker: `npm run build:web` は `node_modules/.vite-temp/...` 書き込み `EPERM`。
- environment blocker: `git ls-remote` はDNS失敗、`git fetch` は `.git/FETCH_HEAD` 書き込み不可。
- skipped: 実Supabase/Postgres integration test。DB URL / `psql` なし。

## 明日の実装順

1. backup / proof APIの認証、user ownership、proof visibility/revocation境界を実装する。
2. 他user・private・revoked proof拒否テストを追加する。
3. 実Supabase/Postgres検証とcost/compliance docsを閉じる。
