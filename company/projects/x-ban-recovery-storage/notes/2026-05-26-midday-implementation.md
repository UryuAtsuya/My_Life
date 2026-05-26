---
date: "2026-05-26"
project: "xguard"
type: midday-implementation
status: pushed
---

# 2026-05-26 XGuard 昼実装

## 結論

`/Users/uryuatsuya/XGuard/xguard` は昼runでも `NOT_WRITABLE` だったため、実装は `/private/tmp/xguard-midday-2026-05-26` の一時cloneで行った。

XGuard repo `UryuAtsuya/Xguard` `origin/main` へ `c7a315c Add API usage ledger contract` をpush済み。

## 反映内容

- `SupabaseTokenRepository.findXToken()` のread pathでv0 scopeを再検査。
- `InMemoryTokenRepository` でも保存・読み取り時に `tweet.read`, `users.read`, `offline.access` 以外を拒否。
- `ApiUsageLedgerService` を追加し、`backup_runs` + `api_usage_events` の最小contract、保守的cost estimate、rate-limit metadata rollupを実装。
- `MockBackupService` からusage eventを記録し、proof DTO生成前のbackup run summaryへ反映。
- `docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md`, `docs/DEPLOY.md` を更新。

## 検証

- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner`: pass（4 files / 9 tests）
- `npm run check`: pass
- `git diff --check`: pass
- `git diff --cached --check`: pass

## 次の具体アクション

1. 指定パスの権限を解消し、`origin/main` `c7a315c` へ同期する。
2. `ApiUsageLedgerService` をSupabase transaction repositoryへ置き換える。
3. Developer Consoleでpricing / spending limit / Usage endpoint / Owned Reads条件を実画面確認する。
