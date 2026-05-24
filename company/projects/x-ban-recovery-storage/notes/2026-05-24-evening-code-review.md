---
created: "2026-05-24"
project: "xguard"
type: evening-code-review
status: reviewed-and-pushed
---

# 2026-05-24 XGuard 夜レビュー要約

## 今日の実装repo状態

- Local: `/Users/uryuatsuya/XGuard/xguard`
- Remote: `https://github.com/UryuAtsuya/Xguard.git`
- Latest pushed commit: `ba98160 Document minimum OAuth scope`
- Branch: `main`
- Push status: `origin/main` と一致

## レビュー結論

backend-first prototypeは、read-only backup、proof DTO、token repository境界、Supabase schema v1の初期形まで到達した。夜レビューでは、v0の初期OAuth scopeから `follows.read` を外し、`tweet.read`, `users.read`, `offline.access` に絞った。

まだAPI原価モデル、compliance docs、architecture docs、Supabase repository実装、Stripe webhook冪等処理本体は未完了。明日はdocs gateを閉じてからrepository実装へ進む。

## 主要指摘

1. P0: `follows.read` はP1対象なので初期OAuth scopeから外す。
   - Status: fixed and pushed.
2. P1: mock backup run stateはmodule globalにしない。
   - Status: fixed and pushed.
3. P1: `npm run check` がこの環境では `dist/` emit不可で落ちる。
   - Next: build用tsconfigと通常環境確認。
4. P1: API原価・compliance・architecture docsが未作成。
   - Next: 2026-05-25 Top 3へ移管。

## 検証

- `git diff --check`: pass
- `npx tsc -p tsconfig.json --noEmit`: pass
- `npx vitest run --configLoader runner`: pass, 2 files / 3 tests
- `npm run check`: fail, `dist/` emitが `EPERM`
- `npm audit --audit-level=moderate --omit=dev`: fail, DNS `ENOTFOUND registry.npmjs.org`

## 明日

1. `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を作る。
2. `tsconfig.build.json` を追加し、test fileをproduction build対象から外す。
3. Supabase repository層とStripe webhook冪等処理の実装順を決める。
