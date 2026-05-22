---
date: "2026-05-21"
type: pm-ticket
status: open
project: web-service-new-product
---

# 2026-05-21 web-service Today Board

## Goal

`ひとり事業の次アクション整理ボード` を、昼に `Projects/` 配下で最小成果物へ落とす。

## Target User

note、Short、webサービスを一人で回し、毎日の公開・計測・次アクション判断が散らばりやすい個人事業者・制作者。

## Pain

TODO、記事候補、公開状況、反応計測、ブロッカーが別々の場所にあり、朝と夜に同じ判断をやり直している。

## Minimum Feature

今日のTop 3、公開待ち、計測待ち、次にやる1手、ブロッカーを1画面で確認できる静的ボード。

## First Screen

`Today Board`

- 左: 今日のTop 3
- 中央: note公開/計測カード
- 右: 次アクションとブロッカー

## Today's Coding Scope

- `Projects/solo-business-today-board/` に静的プロトタイプまたはREADME付き最小設計を作る。
- 認証、DB、外部連携、通知、複数ユーザー対応は作らない。
- 夜にスクリーンショットまたは設計メモで「次にやることが1画面で分かる」状態を確認する。

## Done Criteria

- `Projects/solo-business-today-board/` に成果物がある。
- 対象ユーザー、痛み、最小機能、初回画面がREADMEまたは画面に残っている。
- 次の改善点が1つだけ書かれている。

## 2026-05-21 Midday Production Update

- `Projects/solo-business-today-board/README.md` を作成し、対象ユーザー、痛み、最小機能、確認方法、次の改善点を記録した。
- `Projects/solo-business-today-board/index.html` を作成し、Top 3、note公開/計測カード、次にやる1手、ブロッカーを1画面で見られる静的プロトタイプにした。
- 認証、DB、外部連携、通知、複数ユーザー対応は作っていない。
- 検証: `Projects/solo-business-today-board/index.html` の存在確認とHTML内の主要文言確認を行う。ブラウザ表示確認は、Chrome Computer Useが `approval denied` のため未実施。

## 2026-05-21 Evening Feedback

- Status: v0 prototype done / browser verification pending.
- Verified: `README.md` と `index.html` は存在。`index.html` 内に `Today Board`, `今日のTop 3`, `note公開/計測カード`, `次にやる1手`, `ブロッカー` があることを確認。
- Not verified: 実ブラウザ表示、モバイル幅、スクリーンショット。
- Next: 2026-05-22にブラウザ表示確認を行い、次の最小coding taskを1つだけ選ぶ。

## 2026-05-22 Morning Planning Update

- Status: v0 prototype done / browser verification still first task.
- Today's target user: note、Short、webサービスを一人で回し、朝と夜に同じ優先順位整理をやり直している個人事業者・制作者。
- Today's pain: Top 3、公開/計測カード、ブロッカーが別ファイルに散り、次の1手を毎回探している。
- Today's minimum feature: `Projects/solo-business-today-board/index.html` を開き、今日のTop 3、note公開/計測カード、次にやる1手、ブロッカーが1画面で読めるか確認する。
- Today's scope choice after verification:
  1. 手動更新を2日続けるため、HTML上部に更新用dataセクションを寄せる。
  2. Vault TODOからTop 3/計測カードを生成する小さなスクリプトを作る。
- Out of scope: 認証、DB、外部連携、通知、複数ユーザー対応。

## 2026-05-22 Evening Feedback

- Planned: `Projects/solo-business-today-board/index.html` を表示確認し、次のcoding scopeを1つ決める。
- Coded: 今日の追加実装はなし。既存v0は2026-05-21時点の静的データを持つ。
- Verified: `tidy -q -e Projects/solo-business-today-board/index.html` はエラー出力なし。主要HTMLは読める。
- Not verified: 実ブラウザ表示、モバイル幅、スクリーンショット。`playwright` はローカルに未導入。
- Blockers: 表示確認用ブラウザ経路が使えず、v0のデータもHTML本文内に散っていて日次更新しにくい。
- Next minimum coding task: HTML上部へ手動更新用dataセクションを寄せ、2026-05-23のTop 3と公開/計測カードを1か所で差し替えられる形にする。自動生成スクリプトはその後。
