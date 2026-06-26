---
date: 2026-06-24
type: issue-response
source: "https://github.com/UryuAtsuya/My_Life/issues/2"
status: proposed
---

# GitHub Issue #2 対応: 会社運用と marketing 再稼働

## Issue 要約

最近動いていない folder が増えており、特に marketing が止まり気味。加えて、現在の Codex 実行環境では朝会を挟まないまま実装に入ることがあるため、実装タイミングで全体MTGを挟むべきか確認したい。

## 判断

新しい長い会議体は作らない。代わりに、朝会が未実施のまま Codex が GitHub Issue や project 実装へ入る場合だけ、実装前に5項目の短い全体MTGゲートを挟む。

このゲートで、会社全体の優先順位、marketing への戻し、実装 slice、検証条件、記録先を揃える。

## 変更した運用

1. `company/notes/morning-company-automation.md` に `Codex Implementation Meeting Gate` を追加した。
2. `company/marketing/CLAUDE.md` に、止まった marketing lane を再稼働する最小ルールを追加した。

## marketing 再稼働の最小TODO

- 対象: `note-article-flow`
- 次の1手: 既存の `ready_not_published` 記事から今日出す1本だけを選ぶ。
- 配信先: note
- 測定項目: 公開URL、公開時刻、24h反応
- 記録先: `company/marketing/content-plan/note-article-backlog.md` と該当記事ファイル

## 次回 Codex 実装時の扱い

朝会または handoff note がない状態で実装依頼が来た場合は、実装前に次を確認してから着手する。

1. Main Focus と矛盾しないか。
2. marketing / content / sales に戻す成果物があるか。
3. slice は1つに絞れているか。
4. 検証方法は何か。
5. 結果をどこへ記録するか。
