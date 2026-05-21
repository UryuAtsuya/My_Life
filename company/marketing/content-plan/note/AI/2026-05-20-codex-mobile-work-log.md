---
created: "2026-05-20 13:38 JST"
platform: "note"
status: "ready_not_published"
target_account: "https://note.com/glad_shrew1020"
project: "note-article-flow"
pillar: "AI Solo Company OS"
score: 86
tags: [note, ai, codex, worklog, mobile, ready]
---

# スマホからCodexを動かせる時代の仕事ログ

## タイトル

スマホからCodexを動かせる時代の仕事ログ

## リード文

Codexをスマホから確認できるようになると、作業場所の自由度は上がります。ただ、本当に大事なのは「スマホでも作業できる」ことではなく、途中で判断を引き継げることです。長く動くAI作業ほど、仕事ログがないと進捗も承認も迷子になります。

## 本文

AIエージェントの作業は、だんだん長くなっています。

少し前までは、1つの質問に答えてもらう使い方が中心でした。今は、ファイルを読み、計画を立て、実装し、検証し、差分を残すところまで進みます。

そうなると、問題は「AIが答えられるか」だけではなくなります。

途中で何を承認するのか。どの差分を採用するのか。失敗した検証をどう扱うのか。次に人間が見るべき場所はどこか。

ここを残さないと、作業は速くなっても運用は不安定になります。

OpenAIは2026年5月14日に、CodexをChatGPT mobile app previewから扱えるようにする更新を発表しました。スマホからactive threads、approvals、diff、test resultsなどを確認できる方向です。

これは便利です。

ただ、自分の会社運用で考えると、スマホ対応そのものよりも、ログの価値が上がる更新だと感じています。

スマホでAI作業を確認するとき、画面は小さいです。机の前にいるときほど、全部のファイルを丁寧に読めません。だからこそ、そこに「今日の目的」「採用する判断」「次に見る数字」がまとまっている必要があります。

自分のVaultでは、朝会、昼制作、夕会を分けています。

朝は今日やることを決める。昼は記事や実装を進める。夜は完了、未完了、明日の引き継ぎを書く。毎回、TODO、作ったファイル、ブロッカー、次アクションを残します。

このログがあると、AIに頼む言葉が変わります。

「続きやって」ではなく、「今日のTODOと昨日の未完了を見て、最初に閉じるべき作業を進めて」と言えます。

スマホで確認するときも、「この差分は何のためか」「どの検証が通ったか」「公開してよい条件は満たしたか」を追いやすくなります。

Codex mobileのような流れは、場所の制約を減らします。

でも、場所の制約が減るほど、文脈の整理は必要になります。家でも外でも見られるからこそ、どこから再開するのかが分からないと困る。

仕事ログに残す項目は、最初は多くなくていいです。

- 今日の目的
- 変更したファイル
- 通った検証
- まだ触ってはいけないもの
- 人間が承認する判断
- 次に見る数字や時刻

この6つがあるだけで、AI作業はかなり引き継ぎやすくなります。

特に「まだ触ってはいけないもの」は大事です。既存の未コミット差分、ユーザーが作ったファイル、公開前の数値、未確認の実績。ここをログに残さないと、AIはきれいに進めようとして、余計なものまで動かしてしまいます。

スマホから確認するときは、さらに「今すぐ承認しない判断」も残したほうがいいです。

移動中や外出先では、差分の細部まで見られないことがあります。その状態で大きな変更を承認すると、あとで確認する場所が増えます。

だから、自分ならログを2段階に分けます。

まず、スマホでは「進めてよい小さな作業」だけを見る。たとえば、TODO整理、文章の追記、既存メモの反映、検証結果の記録です。

次に、PCで見るべきものは明確に保留する。たとえば、公開ボタン、削除、広いリファクタ、未確認の数値を使う判断です。

この分け方があると、スマホ対応は雑な承認ではなく、作業を止めないための中継地点になります。

AIが強くなるほど、人間の仕事は減るだけではありません。

むしろ、何を任せるか、何を承認するか、どの証拠が足りないかを残す仕事が増えます。

スマホからCodexを動かせる時代に必要なのは、派手な使い方より、短くても途切れない仕事ログです。

今日の作業を、明日の自分とAIが同じ場所から再開できるようにする。

それができると、AIエージェントは単発の便利ツールではなく、毎日の仕事を進めるチームメンバーに近づきます。

## CTA

AI作業を長く走らせる人は、今日の最後に「目的、変更ファイル、検証、承認待ち、次に見るもの」を残してみてください。スマホで確認するかどうかより、再開できるログがあるかどうかで、翌日の進み方が変わります。

## noteタグ候補

- AI活用
- Codex
- 仕事術
- 生成AI
- 個人事業
- ワークフロー

## 参考リンク・証拠素材

- OpenAI `Work with Codex from anywhere`: `https://openai.com/index/work-with-codex-from-anywhere/`
- OpenAI Help Center `ChatGPT Release Notes`: `https://help.openai.com/en/articles/6825453-chatgpt-release-notes`
- `company/marketing/content-plan/note-research-2026-05-19.md`
- `company/todos/2026-05-20.md`
- `company/projects/codex-active-projects.md`
- 既存AI仕事ログ記事: `company/marketing/content-plan/note/AI/2026-05-15-ai-work-log-reason.md`

## アイキャッチ方向

### Prompt A

Create a clean editorial note.com eyecatch image for a Japanese AI operations article.
Theme: continuing Codex work from desktop to mobile through clear work logs.
Reader emotion: calm continuity.
Central visual: a phone showing an AI thread beside a laptop diff and a small work-log checklist.
Text on image: "途切れない仕事ログ"
Style: practical solo-company AI operations, crisp layout, modern Japanese tech media, high contrast, readable at thumbnail size, no clutter.
Aspect ratio: 16:9.
Avoid: generic robot mascot, sci-fi glow, busy dashboard, tiny unreadable text.

Alt text: スマホのAIスレッド、PCの差分画面、仕事ログのチェックリストが並び、作業の引き継ぎを示す画像。

### Prompt B

Create a clean editorial note.com eyecatch image for a Japanese article.
Theme: approvals, diffs, and test results becoming a simple decision log.
Reader emotion: organized and confident.
Central visual: three cards labeled Approval, Diff, Test connected to a notebook called Work Log.
Text on image: "承認を残す"
Style: practical AI workflow editorial, clean composition, high contrast, readable at thumbnail size.
Aspect ratio: 16:9.
Avoid: dark hacker terminal, robot face, crowded UI.

Alt text: Approval、Diff、Testの3枚のカードが仕事ログのノートにつながっている画像。

### Prompt C

Create a clean editorial note.com eyecatch image for a Japanese solo-company AI article.
Theme: a daily company workflow that can be resumed from phone because tasks and decisions are logged.
Reader emotion: steady progress.
Central visual: morning, midday, evening columns on a board with a phone notification beside it.
Text on image: "スマホで再開"
Style: modern Japanese tech media, practical solo-company operations, no clutter.
Aspect ratio: 16:9.
Avoid: futuristic city, generic robot, unreadable small text.

Alt text: 朝、昼、夜の作業ボードとスマホ通知があり、仕事ログで作業を再開できることを表す画像。

### 推奨

Prompt A。Codex mobileと仕事ログの関係が最も直接伝わるため。

## 記事スコア

合計: 86/100

| 観点 | 点 | 理由 |
|---|---:|---|
| 読者の痛み | 14/15 | 長く走るAI作業で判断と承認が迷子になる課題を示している |
| 具体的な証拠 | 17/20 | OpenAIのCodex mobile更新、Vault運用、既存AI仕事ログ記事を根拠にしている |
| 独自性 | 14/15 | 機能紹介ではなく、仕事ログと承認運用へ寄せている |
| 構成 | 14/15 | 背景、問題、運用例、チェック項目、CTAの順で読める |
| 実用的な持ち帰り | 14/15 | 6項目の仕事ログチェックをすぐ使える |
| 収益化への接続 | 6/10 | AI運用相談やテンプレ化に接続できるが、本文内の導線は控えめ |
| タイトルとアイキャッチ | 7/10 | タイトルは明確。アイキャッチはプロンプト段階 |

## 公開前チェック

- [x] タイトルが具体的
- [x] 導入で読む理由が分かる
- [x] 具体的な証拠素材がある
- [x] 根拠のない実績・数字を含まない
- [x] 未公開物を公開済みと誤認させていない
- [x] CTAがある
- [x] noteタグ候補がある
- [x] アイキャッチ方向とalt textがある
- [ ] note投稿画面へ転記する
- [ ] 公開URLを記録する

## 投稿後記録

- 公開URL:
- 共有URL:
- 公開時刻:
- タグ:
- 初動反応:
- スキ:
- コメント:
- フォロー:
- プロフィール遷移:
- DM:
- 次回計測チェックポイント:
  - 24h:
  - 72h:

## 制作メモ

- 2026-05-20 13:38 JSTにシステム日付を確認した。
- 2026-05-19夕会の翌日候補 `スマホからCodexを動かせる時代の仕事ログ` を本文化した。
- 既存の `AI時代に、毎日の仕事ログを残す理由` は引き続き公開優先の `ready_not_published` として別管理する。
- 外部構造化ドラフト `/Users/uryuatsuya/note/articles/drafts/20260520-codex-mobile-work-log.md` は、現セッションの書き込み許可外のため未保存。

## 2026-05-21 昼最終確認

- 2026-05-21の朝会、decision、`note-research-2026-05-21.md` を確認し、この記事は既存AI仕事ログ記事の続編として維持する。
- OpenAI公式発表とChatGPT Release Notesの参考リンク、company朝昼夜ログ、既存AI仕事ログ記事への接続を確認した。
- `note-growth-editor` の採点表で再確認し、スコアは86/100のまま。80点以上のため公開候補。
- 同日にAI仕事ログ系を2本並べると食い合うため、公開順は `AI時代に、毎日の仕事ログを残す理由` の公開後にする。
- Google Chrome Computer Useが `approval denied` のため、note転記、下書き保存、投稿、公開URL取得は未実施。
- 外部構造化ドラフト `/Users/uryuatsuya/note/articles/drafts/20260520-codex-mobile-work-log.md` は現在の書き込み許可範囲外のため未保存。
