---
date: "2026-06-07"
project: "xguard"
type: midday-implementation
status: completed-with-followups
---

# 2026-06-07 昼実装 - XGuard docs release gate

## 実装スライス

- 対象: XGuard docs release gate 更新のみ。
- 作業コピー: `/private/tmp/xguard-midday-2026-06-07-1331`
- 起点: `/Users/uryuatsuya/XGuard/xguard` `9ac4f2f Add proof visibility management route`
- 変更対象:
  - `docs/API_COST_MODEL.md`
  - `docs/COMPLIANCE.md`

## サブエージェント分担

- Implementation agent: coordinator が担当。`/private/tmp` clone で docs 2ファイルだけを編集。
- Review agent: `code-reviewer` subagent を使用。P1 2件、P2 2件を指摘。
- Verification agent: subagent を使用。`npx tsc` は registry DNS で blocker。coordinator が正本 `node_modules` symlink を使って `tsc --noEmit` を再検証。
- Documentation/Sync agent: `explorer` subagent を使用。MyLife 更新先と既存note未作成を確認。

## 変更内容

### `docs/API_COST_MODEL.md`

- X API の通常 read 単価を release gate として明記:
  - `post`: `$0.005/resource`
  - `user`: `$0.010/resource`
- `Owned Reads` は developer app owner 本人向け条件として扱い、複数顧客 SaaS の原価計算には使わない方針を明記。
- Usage endpoint を `GET https://api.x.com/2/usage/tweets` に更新。
- post read は Usage API と internal ledger で突合し、user read / total spend / credit balance は Developer Console evidence として保存する方針を追加。
- `Spending limit` と internal monthly budget の 80% 到達時点で backup run を停止し、100% 到達後は retry しない方針を追加。

### `docs/COMPLIANCE.md`

- Enterprise 適用要否チェックリストを追加。
- 月次 tweet read 100万件は X 公式capではなく、XGuard内部の conservative review threshold と明記。
- 24時間削除SLAを追加。
- 退会・削除要求は backup / proof data を削除、proof revoke 単体は公開payload停止として分離。
- API access 終了時の全削除runbookを追加。

## Review agent 指摘と対応

- P1: 退会・削除と proof revoke が同じ「非公開化可」に読める。対応済み。退会・削除は削除、proof revoke は公開payload停止に分離。
- P1: Usage API 突合が post read のみで user read / total spend が不足。対応済み。Developer Console evidence と internal ledger 差分確認を追加。
- P2: 月次100万tweet readが公式capに見える。対応済み。内部review threshold と明記。
- P2: Usage endpoint host が `api.twitter.com`。対応済み。`api.x.com` に修正。

## 検証

- `git diff --check`: pass
- `git diff --cached --check`: pass
- `npx tsc -p tsconfig.json --noEmit`: temp clone に `node_modules` がなく、registry DNS `ENOTFOUND registry.npmjs.org` で blocker
- `/Users/uryuatsuya/XGuard/xguard/node_modules/.bin/tsc -p tsconfig.json --noEmit`: pass（temp clone に正本 `node_modules` symlinkを一時作成して実行。symlinkはcommit対象外）
- `git status --short --branch`: XGuard temp clone clean after push

## Commit / push

- XGuard commit: `c4403d8 Document XGuard release gates`
- push先: `UryuAtsuya/Xguard` `origin/main`
- push結果: 成功。`9ac4f2f..c4403d8 main -> main`
- 追加確認: `git ls-remote origin refs/heads/main` は push 後に `Could not resolve host: github.com` で失敗。push出力と local tracking `origin/main` 更新を evidence とする。

## 未完了

- 実Supabase/Postgres integration test は DB URL / `psql` 条件不足のため未実施。
- OAuth configured mode の実 X token exchange、subject/account検証、production mock callback禁止は未実装。
- X Developer Console 実画面の最新pricing / credit balance / spending limit確認は未完。

## 夜レビューへ渡すTop 3

1. OAuth configured mode で実 X token exchange + subject/account検証 + production mock callback禁止を実装する。
2. `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実DBで実行し、usage ledger境界を確認する。
3. `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` の release gate を runtime/CI gate へ落とし込む。
