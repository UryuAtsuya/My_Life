---
date: "2026-05-20"
type: morning-business-meeting
status: complete
---

# 2026-05-20 morning business meeting

## 実行確認

- 日付確認: `2026-05-20`
- 実行時刻: `2026-05-20 15:11 JST`
- 参照: `CLAUDE.md`, `company/sync-policy.md`, automation memory, note editorial files, note-growth-editor, note-pipeline
- 外部research保存先: `/Users/uryuatsuya/note/articles/research/2026-05-20-morning-brief.md` は `NOT_WRITABLE_OR_MISSING`

## 朝会結論

今日もnote成長を優先する。ただし新規本文を増やす前に、`AI時代に、毎日の仕事ログを残す理由` の公開、MBTI紹介noteの24h反応、既存note/コーヒー記事の管理画面実測、`AgentRunShowcaseShort` の公開台帳を閉じる。

coffee / AI / MBTI は分けて扱う。昼の本命は、AIレーンでは公開待ち記事の公開、coffeeレーンでは反応実測後の `高くなったコーヒーで、豆選びを3基準に絞る`、MBTIレーンでは24h反応を使った `診断結果を恋愛の会話に変える3つの聞き方`。

`web-service-new-product` はnoteと混ぜず、朝は対象ユーザー、痛み、最小機能、初回画面だけを決める。今日の最小候補は `ひとり事業の次アクション整理ボード` とし、昼の実装は仮データ付き初回画面までに絞る。

## 役割別結論

### PM / strategy

- 結論: 公開待ちAI記事を出してログ化することが最優先。
- リスク: 記事3本、Short、webサービスを同時に広げると、公開・計測ログがまた欠ける。
- 次アクション: AI記事公開、既存note/coffee実測、Short公開判定、webサービス最小仮説の順で進める。
- 補正: PM入力ではMBTI 24h計測日が1日ずれていたが、公開は `2026-05-19 14:10 JST` のため、24h計測は `2026-05-20 14:10 JST` 以降。

### creative / content

- 結論: AIレーンは `AI時代に、毎日の仕事ログを残す理由` の公開が最優先。coffeeは単独記事として `高くなったコーヒーで、豆選びを3基準に絞る`、MBTIは24h反応後に会話への使い方へ展開する。
- リスク: AI記事を放置すると運用停滞が目立つ。coffeeにAIを混ぜると分離方針が崩れる。
- 次アクション: AI ready記事を公開、MBTI 24h数値を確認、coffee記事は3基準だけ決めて昼以降へ渡す。

### engineering / production

- 結論: 実行順は、ブラウザ/手動承認経路の確保、AI記事公開と記録、MBTI 24hと既存note実測、Short投稿台帳、web-service-new-product最小実装。
- リスク: Chrome/Brave Computer Use承認拒否が続く限り、note公開、Short投稿、公開URL取得は自動完了できない。
- 次アクション: 手動または承認済みブラウザ経路を使い、公開結果だけでもVaultへ戻す。

### business / growth

- 結論: noteは主軸だが、今日は新規量産ではなく公開・計測・台帳記入を閉じる日。
- リスク: MBTI/既存noteの実測がないと、タイトル、冒頭、タグ、CTAの改善判断ができない。Short公開証跡なしのoutreachは弱い。
- 次アクション: AI公開、MBTI 24h、既存note実測、Short公開/outreach、webサービス最小企画の順に進める。

## 今日のTop 3

1. `AI時代に、毎日の仕事ログを残す理由` をnoteへ公開し、URL、時刻、タグ、初動反応、24h/72h予定を戻す。
2. `MBTI×ラブタイプ診断は、相性の答えより会話の入口になる` の24h反応と既存note/coffee記事の管理画面実測を回収する。
3. `AgentRunShowcaseShort` を既存素材で公開し、公開台帳と1件outreach送付記録を埋める。

## 昼に書く/進めるnote候補

| レーン | 候補 | 昼の最小完了 |
|---|---|---|
| AI | `AI時代に、毎日の仕事ログを残す理由` | 公開と投稿後記録 |
| coffee | `高くなったコーヒーで、豆選びを3基準に絞る` | 実測後に構成、出典、3基準を確定 |
| MBTI | `診断結果を恋愛の会話に変える3つの聞き方` | 24h反応を確認し、構成へ反映 |

## web-service-new-product 朝企画

- 対象ユーザー: note、Short、webサービスを一人で回す個人事業者/クリエイター。
- 痛み: TODO、公開ログ、計測、次アクションが分散し、毎日同じ判断をやり直す。
- 最小機能: 今日の3タスク、公開/計測ステータス、次アクション1つを1画面で確認できるボード。
- 初回画面: `Today Board`。左にTop 3、中央に公開/計測カード、右に次アクションとブロッカー。
- 今日のcoding scope: `Projects/` 配下で既存候補を確認し、静的プロトタイプまたはREADME付き最小設計を作る。認証、DB、外部連携は作らない。

## 未解決事項

- note公開とShort投稿はブラウザ/手動承認経路が必要。
- `/Users/uryuatsuya/note/articles/research/` はこの環境では書き込み不可または未作成。
- 既存note/coffee記事の管理画面値は未取得。公開ページの一部表示だけで改善判断を確定しない。
