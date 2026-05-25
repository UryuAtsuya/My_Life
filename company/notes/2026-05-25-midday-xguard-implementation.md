---
date: "2026-05-25"
type: midday-xguard-implementation
project: x-ban-recovery-storage
---

# 2026-05-25 XGuard 昼実装メモ

## 今日の前提

- システム日付: `2026-05-25`
- 実行時刻: `2026-05-25 13:36:37 JST`
- 実装対象: `/Users/uryuatsuya/XGuard/xguard`
- GitHub実装repo: `UryuAtsuya/Xguard`
- MyLife正本: `company/projects/x-ban-recovery-storage/`

## 実装ディレクトリの状態

- `/Users/uryuatsuya/XGuard/xguard` は読み取り可能で、最新確認時点のHEADは `ba98160 Document minimum OAuth scope`。
- ただし現在のCodexサンドボックスからは `test -w /Users/uryuatsuya/XGuard/xguard` が失敗し、`mkdir .codex-write-test` も `Operation not permitted`。
- Vault内へ実装コードを迂回配置せず、`/private/tmp/xguard-midday-2026-05-25` に一時cloneを作成して、同じ `UryuAtsuya/Xguard` `origin/main` へ実装成果をpushした。

## XGuard実装成果

- `tsconfig.build.json` を追加し、production buildから `backend/src/__tests__/**/*.ts` を除外した。
- `package.json` の `build` を `tsc -p tsconfig.build.json` に変更し、`test` を `vitest run --configLoader runner` に変更した。
- `TokenRepository` に `auth_expired` 遷移とtoken削除導線を追加した。
- `SupabaseTokenRepository` と `SupabaseTokenStore` contractを追加し、service role + Vault/encryption前提の置換境界をコード化した。
- `backend/src/__tests__/tokenRepository.test.ts` を追加し、token ref保存、`auth_expired` 遷移、revoked rowのread path除外を検証した。
- `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を追加した。
- `docs/API_SPEC.md` と `README.md` をdocs gate / repository contractに合わせて更新した。

## 安全境界

- v0初期OAuth scopeは `tweet.read`, `users.read`, `offline.access` のまま。
- `follows.read` は追加していない。
- 自動DM、自動follow/unfollow、自動投稿、BAN回避、raw X API payload公開は実装していない。
- token本文は扱わず、backend repository内のtoken refだけを扱う前提にした。

## 検証

- `npm run build`: pass
- `npm run check`: pass。3 files / 5 tests passed。
- `git diff --check`: pass
- `git diff --cached --check`: pass
- 未実施: `npm audit`。理由はこの実行環境では外部registry到達を前提にできないため。
- 注意: 検証は `/private/tmp/xguard-midday-2026-05-25` の一時cloneで実施。指定パス `/Users/uryuatsuya/XGuard/xguard` は書き込み不可のため、ローカル作業ツリー自体は更新できていない。

## GitHub反映

- XGuard commit: `b3bd37c Add token repository contract and docs gates`
- Push先: `https://github.com/UryuAtsuya/Xguard.git` `main`
- Push結果: `ba98160..b3bd37c main -> main`

## 夜レビューへ渡すTODO

1. `/Users/uryuatsuya/XGuard/xguard` のローカル作業ツリーを `b3bd37c` へ同期し、指定パスで `npm run check` を再実行する。
2. `SupabaseTokenStore` の実adapterを作る前に、Supabase Vaultまたは暗号化カラムの実運用方針を1つに決める。
3. 次の実装は `backup_runs` + `api_usage_events` のtransaction service、またはStripe webhook冪等処理のどちらか1本に絞る。
