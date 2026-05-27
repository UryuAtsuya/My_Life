---
date: "2026-05-27"
project: "xguard"
type: morning-planning
status: handoff-ready
---

# 2026-05-27 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。今日は新規機能を広げる前に、指定パスcheckoutをpush済み正本へ揃え、API usage ledgerの入力validationとDeveloper Console原価確認を閉じる。

v0のプロダクト境界は維持する。

- 作る: read-only OAuth backup、profile/post snapshot、usage/cost ledger、proof DTO、削除/非公開/取り下げ追従queue。
- 作らない: 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線、復旧保証表現。
- OAuth scope: `tweet.read`, `users.read`, `offline.access` のみ。`follows.read` はP1まで保留。

## 現在の実装workspace状態

- Local: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`
- Git状態: `## main...origin/main [ahead 4, behind 2]`
- Local HEAD: `d735ffa Wire mock backups through usage ledger`
- 指定パス直近履歴: `d735ffa`, `0991eeb`, `91229db`, `f60be3e`, `ba98160`
- Push済み正本: `/private/tmp/xguard-midday-2026-05-26` の `c7a315c Add API usage ledger contract`
- Remote: `https://github.com/UryuAtsuya/Xguard.git`

## 昼の実装スコープ

### 作業場所

1. まず `/Users/uryuatsuya/XGuard/xguard` で書き込み可否を再確認する。
2. 書き込み可能なら、remoteをfetchし、`origin/main` の `c7a315c` 以降とlocal差分を整理する。
3. 書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-27` に一時cloneして作業する。
4. 成果は `UryuAtsuya/Xguard` `origin/main` へcommit/pushし、MyLife側には報告だけを別commitで同期する。

### 作る・直すファイル

- `backend/src/services/apiUsageLedger.ts`
  - `resourceCount`, `estimatedCostCents`, `tweetLimit`, `tweetRemaining`, `tweetsCaptured`, `profilesCaptured` などを非負整数として検証する。
  - 不正入力時はDBへ書く前に明示的なvalidation errorにする。
- `backend/src/__tests__/apiUsageLedger.test.ts`
  - 負値、小数、`NaN`、`Infinity` を拒否する失敗テストを追加する。
- `docs/API_COST_MODEL.md`
  - Developer Consoleで確認したendpoint別単価、spending limit、Usage endpoint、Owned Reads条件を追記する。
  - 実画面確認できない場合は、確認できない理由、代替根拠、次の確認手順を明記する。
- `docs/ARCHITECTURE.md` または `docs/API_SPEC.md`
  - usage/cost ledgerのvalidation境界がAPI request boundaryかrepository boundaryかを短く反映する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx vitest run --configLoader runner`
- `npm run check`
- push前に `git status --short --branch`

`npm run check` が環境制約で落ちる場合は、`tsc --noEmit` とvitest通過を最低限の合格線にし、理由を昼メモへ残す。

## リスク

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` はまだCodexサンドボックスから書き込み不可。実装repo正本が一時cloneに偏るとレビュー対象が分裂する。
2. X API価格はDeveloper Consoleを正とする公式説明があるため、画面実値未確認のまま月額3,000円の利益率を固定しない。
3. `Owned Reads` の安価枠は魅力的だが、第三者ユーザー向けSaaS通常運用では主前提にしない。
4. BAN不安の訴求は強いが、自動DM・自動新アカウント誘導・BAN回避に見える表現はpolicy riskが高い。
