---
date: "2026-05-21"
type: morning-business-meeting
status: complete
---

# 2026-05-21 morning business meeting

## 実行確認

- 日付確認: `2026-05-21 08:01:49 JST`
- 参照: `CLAUDE.md`, `company/sync-policy.md`, automation memory, note editorial files, note-growth-editor, note-pipeline
- 外部research保存先: `/Users/uryuatsuya/note/articles/research/2026-05-21-morning-brief.md` は `NOT_WRITABLE_OR_MISSING`
- 正本: `company/marketing/content-plan/note-research-2026-05-21.md`

## 朝会結論

今日もnote成長を優先する。ただし、公開待ちと計測待ちが増えているため、朝会の結論は「新規本文を増やす日」ではなく「公開・実測・台帳記入を閉じる日」とする。

AIレーンは意見が分かれた。creative/contentは外部鮮度のある `スマホからCodexを動かせる時代の仕事ログ` を主砲に推した。一方でPM/strategyとbusiness/growthは、5/15から公開待ちの `AI時代に、毎日の仕事ログを残す理由` を先に閉じるべきと判断した。最終決定は、既存AI記事を先に公開し、その公開後記録を使ってCodex mobile記事を続編として出す。

coffee / AI / MBTI は引き続き分ける。coffeeは `高くなったコーヒーで、豆選びを3基準に絞る`、MBTIは `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方` を次候補として維持するが、公開・計測・手動経路の確保を先に置く。

`web-service-new-product` はnoteと混ぜず、昼のproductionで `ひとり事業の次アクション整理ボード` の最小成果物を `Projects/` 配下に置く。朝は対象ユーザー、痛み、最小機能、初回画面を1案に固定する。

## 役割別結論

### PM / strategy

- 結論: 今日の最優先は公開待ちAI記事を出してログ化すること。
- リスク: 公開、計測、outreach、web-service最小成果物を同日に並べると、全部が未完了で残る。
- 次アクション: AI記事公開、MBTI/coffee実測、Short公開判定、web-service最小仮説の順で進める。

### creative / content

- 結論: AI新稿 `スマホからCodexを動かせる時代の仕事ログ` は外部信号が強い。coffeeとMBTIの新稿も公開候補として成立している。
- リスク: AI ready記事が2本あり、同日に近いテーマを並べると食い合う。MBTIは診断断定に寄せない。
- 次アクション: 既存AI記事を公開後、Codex mobile記事を続編として出す。coffee/MBTIはタイトルと導入だけ最終確認する。

### engineering / production

- 結論: note公開・Short投稿は自動化前提にしない。ブラウザまたは手動経路を使い、結果をVaultへ戻す。
- リスク: Chrome/Brave Computer Use approval denied と外部research/draftsの書き込み不可が継続している。
- 次アクション: 朝会でweb-serviceの対象と最小成果物を決め、昼に `Projects/` 配下へ実装または設計メモを置く。

### business / growth

- 結論: 今日の主軸はnote公開と実測回収。公開本数だけでなく、導線、反応、外部接点まで戻す。
- リスク: MBTI 24h、既存note/coffee実測、Short反応/outreachが未回収のままだと、次の記事判断が勘に寄る。
- 次アクション: 公開待ちAI記事を今日の主力として公開し、ready_not_published 3記事は収益導線に近い順で昼以降に処理する。

## 今日のTop 3

1. `AI時代に、毎日の仕事ログを残す理由` をnoteへ公開し、公開URL、時刻、タグ、初期反応、24h/72h予定を戻す。
2. MBTI紹介noteの24h反応と、既存note/coffee記事の管理画面実測を回収し、次に直す場所を1つに絞る。
3. `web-service-new-product` の `ひとり事業の次アクション整理ボード` を昼に最小成果物へ落とす。余力があれば `AgentRunShowcaseShort` の公開台帳も埋める。

## 昼に書く/公開するnote候補

| レーン | 候補 | 昼の最小完了 |
|---|---|---|
| AI | `AI時代に、毎日の仕事ログを残す理由` | 公開と投稿後記録 |
| AI follow-up | `スマホからCodexを動かせる時代の仕事ログ` | 既存AI記事公開後の続編として公開順を決める |
| coffee | `高くなったコーヒーで、豆選びを3基準に絞る` | タイトル、導入、タグを最終確認し、公開可能なら公開 |
| MBTI | `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方` | 24h反応を回収し、会話化の導入を確認 |

## web-service-new-product 朝企画

- 対象ユーザー: note、Short、webサービスを一人で回し、毎朝の優先順位と公開/計測ログが散らばっている個人事業者・制作者。
- 痛み: TODO、記事候補、公開状況、反応計測、次アクションが複数ファイルに分かれ、毎日同じ判断をやり直す。
- 最小機能: 今日のTop 3、公開待ち、計測待ち、次にやる1手、ブロッカーを1画面に表示する静的ボード。
- 初回画面: `Today Board`
  - 左: 今日のTop 3
  - 中央: note公開/計測カード
  - 右: web-serviceの次アクションとブロッカー
- 今日のcoding scope: `Projects/solo-business-today-board/` に静的プロトタイプまたはREADME付き最小設計を作る。認証、DB、外部連携、通知は作らない。
- 成功条件: 夜に「次にやること」が1画面または1枚の設計メモで分かる状態。

## 未解決事項

- note公開とShort投稿はブラウザ/手動承認経路が必要。
- `/Users/uryuatsuya/note/articles/research/` と drafts は現環境では書き込み不可または未作成。
- 既存note/coffee記事の管理画面値は未取得。公開ページの一部表示だけで改善判断を確定しない。
