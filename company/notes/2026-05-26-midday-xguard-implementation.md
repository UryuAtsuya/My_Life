---
date: "2026-05-26"
project: "xguard"
type: implementation-note
---

# 2026-05-26 XGuard Midday Implementation

## 結論

指定パス `/Users/uryuatsuya/XGuard/xguard` は今回もCodex実行環境から `NOT_WRITABLE` だったため、実装コードはVaultへ置かず `/private/tmp/xguard-midday-2026-05-26` の一時cloneで進めた。

XGuard実装repoは `UryuAtsuya/Xguard` `origin/main` へ `c7a315c Add API usage ledger contract` としてpush済み。

## 実装したこと

- remote `b3bd37c` を起点に一時cloneを作成し、指定パスlocalの `f60be3e` / `91229db` で指摘されていたscope境界を現行構成へ反映した。
- `SupabaseTokenRepository.findXToken()` のread pathで `assertReadOnlyXScopes(row.scope)` を再検査するようにした。
- `InMemoryTokenRepository` でも保存時・読み取り時にv0 scopeを検査するようにした。
- `ApiUsageLedgerService` を追加し、`backup_runs` と `api_usage_events` の最小contract、保守的なX API read cost見積もり、rate-limit metadataのrollupを実装した。
- `MockBackupService` からusage ledgerへ `GET /2/users/me` と `GET /2/users/:id/tweets` 相当のusage eventを記録するようにした。
- `docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md`, `docs/DEPLOY.md` を更新・追加した。

## 検証

- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner`: pass（4 files / 9 tests）
- `npm run check`: pass
- `git diff --check`: pass
- `git diff --cached --check`: pass

補足: 一時cloneは `node_modules` を持たないため、検証時だけ `/Users/uryuatsuya/XGuard/xguard/node_modules` へのsymlinkを使い、検証後に削除した。`npx tsc` はネットワーク名前解決不可でregistry取得に行くため使わず、ローカルの `tsc` binaryを使った。

## Git

### XGuard

- Commit: `c7a315c Add API usage ledger contract`
- Push先: `https://github.com/UryuAtsuya/Xguard.git` `origin/main`
- Push結果: success

### MyLife

- このメモと関連company更新を別commitで同期予定。

## 未解決

- `/Users/uryuatsuya/XGuard/xguard` 自体はまだ `NOT_WRITABLE` で、作業ツリーも `main...origin/main [ahead 2]` のまま残っている。次回は権限解決後に `origin/main` の `c7a315c` へ同期する。
- Developer Console実画面のendpoint別単価、spending limit、Usage endpoint可否、Owned Reads適用条件は未確認。docsには未確認理由と保守的な暫定見積もりを記録した。
- Stripe webhook handlerの冪等処理は未着手。

## 夜レビューへ渡すTop 3

1. `/Users/uryuatsuya/XGuard/xguard` の権限を直し、`origin/main` の `c7a315c` を指定パスへ同期する。
2. `ApiUsageLedgerService` をSupabase transaction repositoryへ置き換え、`monthly_api_cost_limit_usd` 超過前停止を実装する。
3. Developer Consoleでpricing / spending limit / Usage endpoint / Owned Reads条件を確認し、`docs/API_COST_MODEL.md` の暫定値を実値へ更新する。
