---
created: "2026-05-11"
platform: "note"
status: "ready_to_publish"
target_account: "https://note.com/glad_shrew1020"
project: "note-article-flow"
pillar: "Practical AI Production Notes"
score: 87
tags: [note, ai, codex, browser-automation, workflow]
---

# note投稿をブラウザ操作で自動化してみた

## タイトル

note投稿をブラウザ操作で自動化してみた

## リード文

noteを継続したいと思っても、毎回つまずくのは「書くこと」だけではない。タイトルを入れ、本文を整え、タグを決め、公開前チェックをして、URLと公開時刻を記録する。この細かい作業が残るほど、投稿は後回しになる。そこで今回は、Codexとブラウザ操作を使って、note記事の下書き投入から公開記録までをひとつの運用にした。

## 本文

AIで記事を書くこと自体は、もう珍しくない。

でも、実際にnoteを続けようとすると、記事本文よりも周辺作業で止まりやすい。

たとえば、こんな作業がある。

- どの記事を今日書くか決める
- 既存ログや制作物から根拠を拾う
- タイトル、本文、CTA、タグを整える
- noteの編集画面に入れる
- 公開前チェックを通す
- 公開URLと時刻を記録する
- 24時間後、72時間後に見る項目を決める

1つずつは小さい。でも、毎回これを人間が思い出して実行すると、かなり重い。

今回やったのは、この一連の作業を「note編集部OS」として扱うことだった。

まず、会社運用用のVaultに `note-article-backlog.md` を作り、次に書く記事を1本だけ決めた。候補はたくさん出せるが、昼の制作時間で完成させるには、選ぶ記事を絞る必要がある。

次に、`note-growth-editor` というCodex用のスキルを作った。役割は、記事テーマの選定、構成、採点、アイキャッチ方向、公開前チェックをまとめて扱うこと。単に「それっぽい記事を書く」のではなく、公開してよいかを100点満点で採点する。

採点項目は、読者の痛み、具体的な証拠、独自性、構成、実用的な持ち帰り、収益化への接続、タイトルとアイキャッチの7つにした。80点未満なら公開しない。これは、AIで記事を量産するほど、弱い記事も簡単に増えてしまうからだ。

実験として、最初の記事では `Short Video Operations OS` の制作ログを使った。

Codexが記事本文を作り、noteの編集画面にタイトルと本文を入れ、下書き保存し、公開設定画面まで進めた。前回は外部公開操作なので、最後の `投稿する` だけはユーザーが試験的に押した。公開後はURLと時刻をVaultに戻し、記事ファイル、TODO、PMチケットに反映した。

公開された記事はこちら。

`https://note.com/glad_shrew1020/n/nb56ae90688a4`

ここで分かったのは、note投稿の自動化で本当に大事なのは、クリック操作そのものではないということ。

大事なのは、公開前後の判断を運用に入れることだった。

記事に具体的な証拠はあるか。未公開のものを公開済みのように書いていないか。数字を盛っていないか。CTAはあるか。公開後にどのURLを、いつ、どのタグで出したかを記録できるか。

この条件が揃っていれば、ブラウザ操作で公開まで進めてもよい。逆に、条件が揃っていないなら、下書きで止めた方がいい。

つまり、note自動投稿は「人間の代わりに投稿ボタンを押す仕組み」ではなく、「公開してよい記事だけを前に進める編集フロー」だと思っている。

今回の自分用ルールはこうした。

1. 朝に市場や記事テーマを調べる
2. 昼に1本だけ記事化する
3. 80点以上ならnoteへ投稿する
4. 公開URL、公開時刻、タグ、初動状態を記録する
5. 24時間後と72時間後に反応を見る

この流れにすると、noteは気合いで書く場所ではなく、日々の作業ログを読者に届く形へ変換する場所になる。

AIを使っている人は多い。でも、使った結果を継続的に発信し、反応を見て、次の仕事や相談につなげるところまで設計している人はまだ少ない。

しばらくは、このnoteを「AIでひとり会社を回す実験ログ」として運用していく。

ツール紹介ではなく、実際に作ったもの、公開したもの、測ったもの、失敗したものを残す。そのために、記事を書く前のリサーチ、記事採点、アイキャッチ、公開記録までをまとめて自動化していく。

## CTA

noteやSNS投稿を「書いて終わり」ではなく、公開・計測・次の行動までつながる運用にしたい人は、コメントかDMで教えてください。自分の実験ログをもとに、使える型から順番に公開していきます。

## noteタグ候補

- AI活用
- 生成AI
- Codex
- note
- 自動化
- 個人開発
- 事業づくり

## アイキャッチ方向

### Prompt A

Create a clean editorial note.com eyecatch image for a Japanese article.
Theme: browser-based note publishing automation with Codex.
Reader emotion: "投稿作業が整理されて、続けられそうだと感じる".
Central visual: a browser editor screen flowing into a publish checklist and a small measurement table with URL and time fields.
Text on image: "note自動投稿"
Style: practical solo-company AI operations, crisp layout, modern Japanese tech media, high contrast, readable at thumbnail size, no clutter.
Aspect ratio: 16:9.
Avoid: generic robot mascot, sci-fi glow, busy dashboard, tiny unreadable text.

Alt text: noteの編集画面、公開チェックリスト、計測表が横に並び、投稿作業の自動化を表している画像。

### Prompt B

Create a clean editorial note.com eyecatch image for a Japanese article.
Theme: turning a writing workflow into a repeatable publishing operation.
Reader emotion: "面倒な投稿作業を仕組みにできる安心感".
Central visual: a desk with three panels labeled Draft, Check, Publish; a small note article card is moving through the panels.
Text on image: "下書きから公開"
Style: practical solo-company AI operations, crisp layout, modern Japanese tech media, high contrast, readable at thumbnail size, no clutter.
Aspect ratio: 16:9.
Avoid: generic robot mascot, sci-fi glow, busy dashboard, tiny unreadable text.

Alt text: 下書き、チェック、公開の3工程を通ってnote記事が進む様子を表した編集部風の画像。

### Prompt C

Create a clean editorial note.com eyecatch image for a Japanese article.
Theme: safe automation that only publishes articles after a scorecard passes.
Reader emotion: "AI投稿でも品質を守れる".
Central visual: a large scorecard marked 87/100 beside a browser publish button with a guarded checklist.
Text on image: "80点で公開"
Style: practical solo-company AI operations, crisp layout, modern Japanese tech media, high contrast, readable at thumbnail size, no clutter.
Aspect ratio: 16:9.
Avoid: generic robot mascot, sci-fi glow, busy dashboard, tiny unreadable text.

Alt text: 87点の採点表と公開ボタン、チェックリストが並び、品質基準を満たした記事だけを公開する運用を示す画像。

### 推奨

Prompt A。記事の主題である「note編集画面から公開記録まで」を一目で伝えられるため。

## 記事スコア

合計: 87/100

| 観点 | 点 | 理由 |
|---|---:|---|
| 読者の痛み | 13/15 | note継続時の周辺作業の重さを冒頭で示している |
| 具体的な証拠 | 18/20 | 公開済みURL、Vault運用、スキル、採点表に基づいている |
| 独自性 | 14/15 | Codex、ブラウザ操作、会社運用ログを組み合わせた一次情報 |
| 構成 | 13/15 | 問題、実験、学び、運用ルール、CTAの順に読める |
| 実用的な持ち帰り | 14/15 | 5ステップの運用ルールと公開判断がある |
| 収益化への接続 | 7/10 | 相談導線はあるが、有料テンプレの具体名はまだ弱い |
| タイトルとアイキャッチ | 8/10 | タイトルは具体的。アイキャッチは制作前で方向のみ |

## 公開前チェック

- [x] タイトルが具体的
- [x] 導入で読む理由が分かる
- [x] 具体的な証拠素材がある
- [x] 根拠のない数字・実績を含まない
- [x] 未公開物を公開済みと誤認させていない
- [x] CTAがある
- [x] noteタグ候補がある
- [x] アイキャッチ方向がある
- [ ] note投稿画面へ転記する
- [ ] 公開URLを記録する

## 投稿後記録

- 公開URL:
- 公開時刻:
- タグ:
- 初動反応:
- スキ:
- コメント:
- フォロー:
- プロフィール遷移:
- 次回計測チェックポイント:
  - 24h:
  - 72h:

## 制作メモ

- 朝の専用 `note-research-2026-05-11.md` は未作成。
- 代替材料として `note-growth-analysis-2026-05-11.md`、`note-article-backlog.md`、公開済み記事記録、automation memoryを使用した。
- 画像生成/Canva制作は未実施。今回はアイキャッチ方向とalt textを記録し、公開判断の必須条件からは外した。
- 2026-05-11 16:05 JST時点で、Chrome/ArcのComputer Use権限がMCP側で拒否されたため、note編集画面への転記と公開は未実施。
- 次アクション: Browser/Computer Use権限を有効にした状態で、本文・タグをnoteへ転記し、公開URLと公開時刻を記録する。
