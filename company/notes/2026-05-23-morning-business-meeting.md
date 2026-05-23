---
date: "2026-05-23"
type: morning-business-meeting
status: complete
---

# 2026-05-23 morning business meeting

## 実行確認

- 日付確認: `2026-05-23 08:01:32 JST`
- 参照: `CLAUDE.md`, `company/sync-policy.md`, automation memory, `company/todos/2026-05-23.md`, `company/notes/2026-05-22-evening-closeout-review.md`, `note-editorial-system.md`, `note-article-backlog.md`, `note-growth-editor`, `note-pipeline`, active project files
- 外部research保存先: `/Users/uryuatsuya/note/articles/research/2026-05-23-morning-brief.md` は `not_writable`
- 正本: `company/marketing/content-plan/note-research-2026-05-23.md`
- subagents: PM/strategy, creative/content, engineering/production, business/growth を起動し、各役割の結論を統合した。

## 朝会結論

今日もnote成長を最優先にする。ただし、新規本文を増やすより先に、公開済みnoteの実測を回収して公開候補を1本に絞る。

AI仕事ログ記事 `AI時代に、毎日の仕事ログを残す理由` の24h反応、MBTI紹介note `MBTI×ラブタイプ診断は、相性の答えより会話の入口になる` の72h反応、既存note/coffee管理画面実測を同じ表で回収する。実測が取れるまで、AI follow-up / coffee / MBTI の公開順は確定しない。

昼の公開候補は3レーンを維持するが、公開は1本だけにする。AIは `スマホからCodexを動かせる時代に、仕事ログへ残すこと`、coffeeは `高くなったコーヒーで、豆選びを3基準に絞る`、MBTIは `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方`。AI仕事ログ24hが一定以上ならAI follow-up、弱いまたは未回収ならcoffeeを先にする。MBTIは72h反応が確認できるまで保留寄りにする。

`web-service-new-product` はToday Board v0を実用化する段階。今日のcoding scopeは自動生成スクリプトではなく、`Projects/solo-business-today-board/index.html` の手動更新用dataセクションをHTML上部へ寄せ、日付、Top 3、公開/計測カードを差し替えやすくすることに絞る。

## 役割別結論

### PM / strategy

- 結論: 今日の優先順位は `note実測回収 -> 公開1本決定 -> Today Board最小改修`。
- リスク: 実測未回収のまま3本公開すると、どの記事が効いたか分からなくなる。AI follow-upは前記事の24h反応が弱い場合、連投で弱点を増幅する。
- 次アクション: AI仕事ログ24h、MBTI紹介note72h、既存note/coffee実測を同じ表で回収し、公開候補を1本だけ選ぶ。

### creative / content

- 結論: AIはCodex mobileの機能紹介ではなく、承認、差分、ログを残せばAIエージェント作業を止めずに進められる話にする。coffeeは値上がり局面でも豆選びを3基準へ減らす記事にする。MBTIは診断結果を会話へ変える3つの聞き方にする。
- リスク: AIは前記事実測が弱い場合、続編公開より改善が先。coffeeはニュース解説に寄りすぎると生活感が弱い。MBTIはタイプ断定や相性ランキングに寄ると信頼を落とす。
- 次アクション: 昼の最初に実測を回収し、公開する1本だけにタイトル、冒頭、CTAの最小調整を入れる。

### engineering / production

- 結論: note公開・計測は自動で進めず、手動または承認済みブラウザで実測し、Vaultへ戻すのが安全。
- リスク: `note.com` のDNS解決不可とChrome/Brave Computer Useの承認拒否が続くと、管理画面値と公開操作は証拠付きで完了できない。
- 次アクション: 未取得項目は理由付きで残す。Today BoardはHTML上部の手動更新dataセクション化を今日の最小scopeにする。

### business / growth

- 結論: 今日の成長レバーは、管理画面実測から営業接続しやすい1本を選ぶこと。
- リスク: 記事公開だけで終わると、問い合わせ、資料請求、Short実績提示への導線が残らない。
- 次アクション: 公開記事の末尾に相談導線を入れ、`AgentRunShowcaseShort` やoutreachへつながる一文を作る。

## 今日のTop 3

1. AI仕事ログ24h、MBTI紹介note72h、既存note/coffee管理画面実測を同じ表で回収する。
2. 実測後、AI / coffee / MBTI から公開する1本だけを決め、公開後記録までVaultへ戻す。
3. Today Boardの手動更新用dataセクションをHTML上部へ寄せるcoding scopeを昼へ渡す。

## 昼に書く/公開するnote候補

| レーン | 候補 | 昼の最小完了 |
|---|---|---|
| AI | `スマホからCodexを動かせる時代に、仕事ログへ残すこと` | AI仕事ログ24h反応が取れたら公開候補。弱ければタイトル/冒頭/CTA改善に回す。 |
| coffee | `高くなったコーヒーで、豆選びを3基準に絞る` | AI実測が弱い、または計測が取れない場合の第一公開候補。 |
| MBTI | `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方` | MBTI紹介note72h反応が確認できたら続編公開。未確認なら既存記事導線改善を先にする。 |

## web-service-new-product 朝企画

- 対象ユーザー: note、Short、webサービスを一人で回し、毎日の公開・計測・次アクション判断が散らばりやすい個人事業者・制作者。
- 痛み: Top 3、公開待ち、計測待ち、ブロッカーが別々のファイルにあり、朝と夜に同じ整理をやり直している。
- 最小機能: Today Boardで、日付、Top 3、公開/計測カード、次にやる1手、ブロッカーを1画面で確認する。
- 今日のcoding scope: `Projects/solo-business-today-board/index.html` の上部に手動更新用dataセクションを寄せ、2026-05-23のTop 3と公開/計測カードを1か所で差し替えられる形にする。
- 作らないもの: 認証、DB、外部連携、通知、複数ユーザー対応、Vault TODO自動生成スクリプト。

## 未解決事項

- note管理画面の実測値は未回収。公開ページの可視表示だけで改善判断を確定しない。
- note公開、Short投稿、管理画面値回収はブラウザ/手動承認経路が必要。
- 外部research保存先は書き込み不可のため、会社側researchファイルを正本にする。
