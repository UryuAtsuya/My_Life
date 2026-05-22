---
date: "2026-05-22"
type: morning-business-meeting
status: complete
---

# 2026-05-22 morning business meeting

## 実行確認

- 日付確認: `2026-05-22 09:29:13 JST`
- 参照: `CLAUDE.md`, `company/sync-policy.md`, automation memory, `company/todos/2026-05-22.md`, `note-editorial-system.md`, `note-article-backlog.md`, `note-growth-editor`, `note-pipeline`, active project files
- 外部research保存先: `/Users/uryuatsuya/note/articles/research/2026-05-22-morning-brief.md` は `operation not permitted`
- 正本: `company/marketing/content-plan/note-research-2026-05-22.md`
- subagents: PM/strategy, creative/content, engineering/production, business/growth を起動し、各役割の結論を統合した。

## 朝会結論

今日もnote成長を優先する。ただし、昼の最初の仕事は新規本文を増やすことではなく、公開済み記事の実測を回収して次の公開順を決めることにする。

AI仕事ログ記事は2026-05-21に公開済みで、24h計測は `2026-05-22 15:04 JST`。MBTI紹介noteは2026-05-19公開済みで、72h計測は `2026-05-22 14:10 JST`。この2つと既存note/coffee管理画面実測を同じ表で回収し、タイトル、冒頭、タグ、CTA、outreach先のどこを直すか1つに絞る。

AI / coffee / MBTI は引き続き分ける。AIは `スマホからCodexを動かせる時代の仕事ログ`、coffeeは `高くなったコーヒーで、豆選びを3基準に絞る`、MBTIは `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方` を今日の候補にする。ただし、AIとMBTIは計測後に公開判断する。

`web-service-new-product` はnoteと混ぜない。Today Board v0は作成済みなので、昼はまずブラウザ表示確認を行い、次のcoding scopeを「手動更新を2日続ける」か「Vault TODOからTop 3を生成する小スクリプト」のどちらか1つに絞る。

## 役割別結論

### PM / strategy

- 結論: 今日の順序は `note反応計測 -> 次の公開順確定 -> AgentRunShowcaseShort公開/outreach -> Today Board次scope確定`。
- リスク: 実測が取れないと公開順が感覚判断に戻る。AI/coffee/MBTIを同日に全部出すと反応差分が読みにくい。
- 次アクション: 14:10 JSTにMBTI 72h、15:04 JSTにAI 24hを回収し、改善対象を1つだけ選ぶ。

### creative / content

- 結論: AI follow-upはCodex mobile機能紹介ではなく、長時間AI作業を止めない仕事ログとして出す。coffeeは価格改定を生活の豆選び3基準に変換する。MBTIは診断結果を会話の質問リストへ変える。
- リスク: AI仕事ログ系が連続すると差分が弱い。coffeeはニュース解説に寄ると一次情報が薄い。MBTIは断定・ランキングに寄ると信頼を損ねる。
- 次アクション: AI 24h反応を続編の冒頭に1段だけ反映する。coffeeは「高いから節約」ではなく「高いから基準を減らす」と明確化する。MBTIは72h反応で続編公開か注意喚起型タイトルかを決める。

### engineering / production

- 結論: note公開経路はブラウザ/手動承認が必要。自動化前提にせず、公開URL、時刻、タグ、初動、24h/72h予定をVaultへ戻す形にする。
- リスク: 外部researchパスは書き込み不可。Today Boardに自動生成や連携を入れると、昼の計測と公開判断を圧迫する。
- 次アクション: 外部ブリーフは company 側を正本にする。Today Boardは表示確認だけ先に済ませ、改善は1点に絞る。

### business / growth

- 結論: 今日の成長レバーはAI先行とMBTI導線。AIは即時性、MBTIは検索・引用・サイト導線、coffeeは生活文脈で読者幅を広げる。
- リスク: 3本を同じ熱量で出すと公開品質と計測が薄くなる。Short/outreachを先にやると、配る資産がない状態で時間を使う。
- 次アクション: note計測表を埋め、MBTIは根拠・比較・内部導線を維持する。余力があればAI記事のShort化を1本だけ作る。

## 今日のTop 3

1. MBTI紹介note72h、AI仕事ログ24h、既存note/coffee管理画面実測を同じ表で回収する。
2. 実測を見て `スマホからCodexを動かせる時代の仕事ログ`、coffee記事、MBTI続編の公開順を1本ずつ決める。
3. `AgentRunShowcaseShort` の公開/outreach台帳と、Today Boardのブラウザ表示確認を閉じる。

## 昼に書く/公開するnote候補

| レーン | 候補 | 昼の最小完了 |
|---|---|---|
| AI | `スマホからCodexを動かせる時代の仕事ログ` | AI仕事ログ24h反応を回収し、続編として公開可否を決める |
| coffee | `高くなったコーヒーで、豆選びを3基準に絞る` | 既公開coffee実測を回収し、公開する場合はURL/時刻/タグ/初動/24h/72hを戻す |
| MBTI | `MBTI×ラブタイプ診断の結果を、会話に変える3つの聞き方` | MBTI紹介note72h反応を回収し、続編として公開可否を決める |

## web-service-new-product 朝企画

- 対象ユーザー: note、Short、webサービスを一人で回し、毎日の公開・計測・次アクション判断が散らばりやすい個人事業者・制作者。
- 痛み: TODO、記事候補、公開状況、反応計測、ブロッカーが別々の場所にあり、朝と夜に同じ判断をやり直している。
- 最小機能: 今日のTop 3、公開待ち、計測待ち、次にやる1手、ブロッカーを1画面で確認する。
- 今日のcoding scope: まず `Projects/solo-business-today-board/index.html` をブラウザ表示確認する。その後、次のscopeを「手動更新を2日続ける」か「Vault TODOからTop 3を生成する小スクリプト」のどちらか1つに決める。
- 作らないもの: 認証、DB、外部連携、通知、複数ユーザー対応。

## 未解決事項

- note管理画面の実測値は未回収。公開ページの可視表示だけで改善判断を確定しない。
- note公開とShort投稿はブラウザ/手動承認経路が必要。
- 外部research保存先は書き込み不可のため、会社側researchファイルを正本にする。
