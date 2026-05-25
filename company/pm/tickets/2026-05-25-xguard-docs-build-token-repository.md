---
created: "2026-05-25"
project: "xguard"
assignee: "codex"
priority: high
status: active
---

# XGuard docs gate / build gate / token repository

## 内容

XGuard v0のread-only境界、X API原価、compliance運用、build設定、OAuth token repositoryの最小実装を昼runで進める。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` が昼runから書き込み可能か確認する。Evidence: 昼runでは指定パス書き込み不可、一時cloneで実装。
- [x] `docs/ARCHITECTURE.md` を追加し、frontend/backend/shared/supabase/stripe/X APIの責務境界を書く。Evidence: XGuard local `f60be3e` / 昼メモ上のpush `b3bd37c`。
- [x] `docs/API_COST_MODEL.md` を追加し、Pay-per-usage、Developer Console確認項目、spending limit、ユーザー単位取得上限を書く。Evidence: XGuard local `f60be3e` / 昼メモ上のpush `b3bd37c`。
- [x] `docs/COMPLIANCE.md` を追加し、X Content削除/非公開化/withheld/ユーザー削除要求への追従を書く。Evidence: XGuard local `f60be3e` / 昼メモ上のpush `b3bd37c`。
- [x] `tsconfig.build.json` または同等の設定でproduction buildから `backend/src/__tests__/**` を外す。Evidence: XGuard local `f60be3e`。
- [x] Supabase repository層で `TokenRepository` の最小実装を作る。Evidence: XGuard local `f60be3e`。
- [x] token本文をfrontendへ返さず、`auth_expired` 遷移を扱う。Evidence: `SupabaseTokenRepository`, `markAuthExpired()`。
- [ ] `git diff --check`, `npm run build`, `npm run check`, `npx vitest run --configLoader runner` を実行する。Evidence: `git diff --check` pass, `vitest` pass。`npm run check` は `dist/` emit EPERM、`tsc --noEmit` はtest mock fetch型不一致でfail。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, `dm.read`, `tweet.write`, `follows.write`, `dm.write` は初期同意画面に入れない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線は作らない。
- proof pageはraw X API payloadを公開しない。
- 書き込み不可の場合、MyLife Vaultへ実装コードを迂回配置しない。

## 朝runメモ

- Research: `company/projects/x-ban-recovery-storage/requirements/2026-05-25-x-ban-research.md`
- Handoff: `company/projects/x-ban-recovery-storage/notes/2026-05-25-morning-planning.md`
- 朝run時点で `/Users/uryuatsuya/XGuard/xguard` は存在し、`main...origin/main` はclean。
- 朝run時点のCodexサンドボックスからは `test -w /Users/uryuatsuya/XGuard/xguard` が `NOT_WRITABLE`。

## 夜レビュー

- Review: `company/notes/2026-05-25-evening-xguard-code-review.md`
- Project note: `company/projects/x-ban-recovery-storage/notes/2026-05-25-evening-code-review.md`
- XGuard local HEAD: `91229db Exclude revoked token refs`
- Push status: 未push。`git push -v origin main` はremote先行で `fetch first`。
- Blocker: `git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可。`npx tsc -p tsconfig.json --noEmit` はmock fetch型不一致でfail。
