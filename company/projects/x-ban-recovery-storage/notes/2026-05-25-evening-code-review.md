---
created: "2026-05-25"
project: "xguard"
type: evening-code-review
status: push-blocked
---

# 2026-05-25 XGuard 夜レビュー要約

## 今日の実装repo状態

- Local: `/Users/uryuatsuya/XGuard/xguard`
- Remote: `https://github.com/UryuAtsuya/Xguard.git`
- Local HEAD: `91229db Exclude revoked token refs`
- Local previous commit: `f60be3e Add Supabase token repository gate`
- Tracking `origin/main`: `ba98160 Document minimum OAuth scope`
- 昼メモ上のGitHub反映済みcommit: `b3bd37c Add token repository contract and docs gates`
- Push status: 夜runでは未push。`git push -v origin main` はremote先行のため `fetch first` で拒否。

## レビュー結論

docs gate、build gate、token repository contractは前進しているが、指定パスのローカル履歴とremoteが揃っていない。まずremote `b3bd37c` を取り込み、`91229db` のrevoked token ref除外を型修正込みで統合する必要がある。

`vitest` は7件passした一方、`tsc --noEmit` はtest mock fetchの型不一致で失敗している。明日は新規機能より、remote同期と型検証復旧を先に閉じる。

## 主要指摘

1. P0: XGuard指定パスがremoteと分岐しており、pushできない。
   - Status: blocked by local `.git` write restriction and remote ahead state.
2. P1: `tokenRepository.test.ts` のmock fetch型が `typeof fetch` と一致せず、TypeScript検証が失敗する。
   - Status: fix first tomorrow.
3. P1: token read pathでscope再検査がない。
   - Status: proposed fix. `revoked_at=is.null` だけでなく `assertReadOnlyXScopes(row.scope)` を追加する。
4. P1: Developer Console実値が未確認。
   - Status: carry over.
5. P2: Stripe webhook冪等handlerとbackup/API usage transaction serviceは未実装。
   - Status: pick one after verification is green.

## 検証

- `git diff --check`: pass
- `npx vitest run --configLoader runner`: pass, 3 files / 7 tests
- `npx tsc -p tsconfig.json --noEmit`: fail, mock `fetchImpl` type mismatch
- `npm run check`: fail, `dist/` emit `EPERM`
- `git fetch origin main`: fail, `.git/FETCH_HEAD` write `Operation not permitted`
- `git push -v origin main`: fail, remote rejected with `fetch first`

## 明日

1. 書き込み可能なXGuard作業ツリーでremoteをfetchし、`b3bd37c`, `f60be3e`, `91229db` を整理してpushする。
2. `tokenRepository.test.ts` の型修正と `findXToken()` scope再検査を入れ、`npm run check` をpassに戻す。
3. Developer Console原価確認後、backup/API usage transaction serviceかStripe webhook冪等handlerのどちらか1本を実装する。
