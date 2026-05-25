---
date: "2026-05-26"
project: "xguard"
type: morning-planning
status: handoff-ready
---

# 2026-05-26 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。新機能追加より先に、指定パスとremoteの分岐、TypeScript検証失敗、X API原価の未確定を閉じる。

v0のプロダクト境界は昨日から変えない。

- 作る: read-only OAuth backup、profile/post snapshot、usage/cost ledger、proof DTO、削除/非公開/取り下げ追従queue。
- 作らない: 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線、復旧保証表現。
- OAuth scope: `tweet.read`, `users.read`, `offline.access` のみ。`follows.read` はP1まで保留。

## 現在の実装workspace状態

- Local: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`
- Git状態: `## main...origin/main [ahead 2]`
- Remote: `https://github.com/UryuAtsuya/Xguard.git`
- 前日夜レビュー上の問題:
  - remote `origin/main` に昼push済み `b3bd37c` があり、指定パスlocalの `f60be3e`/`91229db` と分岐。
  - `git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可で失敗していた。
  - `npx tsc -p tsconfig.json --noEmit` は `tokenRepository.test.ts` のmock fetch型不一致で失敗。

## 昼の実装スコープ

### 作業場所

1. まず `/Users/uryuatsuya/XGuard/xguard` で書き込み可否を再確認する。
2. 書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-26` に一時cloneして作業する。
3. 成果は `UryuAtsuya/Xguard` `origin/main` へcommit/pushし、MyLife側には報告だけを別commitで同期する。

### 作る・直すファイル

- `backend/src/__tests__/tokenRepository.test.ts`
  - mock `fetchImpl` を `typeof fetch` と整合させる。
- `backend/src/repositories/supabaseTokenRepository.ts`
  - `findXToken()` のread pathで `assertReadOnlyXScopes(row.scope)` を再検査する。
- `backend/src/repositories/tokenRepository.ts`
  - 必要ならtoken contract上の戻り値/型を最小修正する。
- `backend/src/services/` または既存構成に合う場所
  - `backup_runs` + `api_usage_events` transaction serviceの最小contractを追加する。
- `docs/API_COST_MODEL.md`
  - Developer Consoleで確認したendpoint単価、spending limit、Usage endpoint確認結果を追記する。未確認なら未確認理由を明記する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx vitest run --configLoader runner`
- `npm run check`

`npm run check` が `dist/` emitの権限制約で落ちる場合は、`tsc --noEmit` とvitest通過を最低限の合格線にし、EPERM理由を報告に残す。

## リスク

1. X API価格は公式docs上もDeveloper Console確認を正としているため、画面実値未確認のまま月額3,000円の原価判断を固定しない。
2. `Owned Reads` は安いが、第三者ユーザー向けSaaSの通常課金前提にできるかは未確定。通常のPost/User/Followers read単価で保守的に見積もる。
3. BAN不安の訴求は強いが、自動DM・自動新アカウント誘導・BAN回避に見える表現はX policyリスクが高い。
