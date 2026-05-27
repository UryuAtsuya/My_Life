---
date: "2026-05-27"
project: "xguard"
type: project-note
status: partial
---

# 2026-05-27 昼実装メモ

## 進捗

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は昼runでも `NOT_WRITABLE`。作業ツリーには未解決conflictがあるため、ここでは直接編集しなかった。
- Vaultへ実装コードを迂回配置せず、`/private/tmp/xguard-midday-2026-05-27` で実装した。
- `ApiUsageLedgerService` に非負整数validationを追加した。
- 負値、小数、`NaN`, `Infinity` を拒否するテストを追加した。
- validation境界を `docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md` へ反映した。

## GitHub反映

- XGuard commit: `3528e26 Validate API usage ledger inputs`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- remote先行 `045d2d2 Add night-work mobile design wireframes` を取り込んだ上で、`3528e26` までpush済み。

## 検証

- `npm ci`: pass
- `./node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass
- `./node_modules/.bin/vitest run --configLoader runner`: pass, 4 files / 29 tests
- `npm run check`: pass
- `git diff --check`: pass
- `git diff --cached --check`: pass

## 残課題

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` を `origin/main` `3528e26` へ同期する。
2. Developer Console実画面でX API単価とUsage条件を確認する。
3. ledgerをSupabase transaction repository化する。
