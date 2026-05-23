---
created: "2026-05-23"
project: "note-article-flow"
assignee: "codex"
priority: high
status: active
---

# 2026-05-23 note実測回収と公開1本決定

## 目的

AI仕事ログ24h、MBTI紹介note72h、既存note/coffee管理画面実測を回収し、AI / coffee / MBTI から今日公開する1本だけを決める。

## 完了条件

- [ ] AI仕事ログ記事 `AI時代に、毎日の仕事ログを残す理由` の24h反応を回収する
- [ ] MBTI紹介note `MBTI×ラブタイプ診断は、相性の答えより会話の入口になる` の72h反応を回収する
- [ ] 既公開note/coffee記事の管理画面実測を同じ表で回収する
- [ ] 実測後、AI / coffee / MBTI から公開する1本だけを決める
- [ ] 公開する1本に必要なタイトル、冒頭、CTAの最小調整を入れる
- [ ] noteへ転記し、公開URL、公開時刻、公開タグ、初期反応、24h/72h計測予定を記録する
- [ ] 記録を記事ファイル、`note-article-backlog.md`、このPMチケットへ戻す
- [ ] 実測または公開ができない場合は、理由と次アクションを残す

## 公開候補

| レーン | ファイル | スコア | 状態 | 今日の判断 |
|---|---|---:|---|---|
| AI | `company/marketing/content-plan/note/AI/2026-05-22-codex-mobile-work-log.md` | 86 | `ready_not_published` | AI仕事ログ24hが一定以上なら公開候補。弱ければ改善へ回す。 |
| coffee | `company/marketing/content-plan/note/coffee/2026-05-22-coffee-bean-three-criteria.md` | 84 | `ready_not_published` | AI実測が弱い、または未回収なら第一公開候補。 |
| MBTI | `company/marketing/content-plan/note/MBTI/2026-05-22-love-type-three-questions.md` | 84 | `ready_not_published` | MBTI紹介note72h確認後に続編公開を判断。未確認なら保留寄り。 |

## ブロッカー

- `note.com` は前回ローカル `curl` でDNS解決不可だった。
- note管理画面値はブラウザまたは手動経路が必要。
- 外部research保存先 `/Users/uryuatsuya/note/articles/research/2026-05-23-morning-brief.md` は `not_writable`。

## 次アクション

1. 昼の最初にnote管理画面または手動経路で実測表を埋める。
2. 実測を見て公開候補を1本だけ決める。
3. 公開後記録をVaultへ戻し、未取得項目は未取得のまま理由を書く。
