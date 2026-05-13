---
date: "2026-05-13"
type: midday-production-session
created: "2026-05-13 13:22 JST"
---

# Midday Production Session - 2026-05-13

## 実行内容

- System date confirmed: `2026-05-13 12:48:35 JST`.
- 今日の最上位タスクを `AIで始めたnote運用で、公開後ログまで見て初めて分かったこと` の記事化に固定した。
- `note-growth-editor` と `note-pipeline` のルール、`note-editorial-system.md`、`note-article-backlog.md`、`note-research-2026-05-13.md`、朝会、決定ログ、PMチケット、関連プロジェクトを確認した。
- note公式の `#AIと始めてみた` 告知とOpenAI release notesを確認し、記事内には参考リンクとして保存した。
- 公開準備済み記事を `company/marketing/content-plan/2026-05-13-ai-started-note-operation-publication-log.md` に作成した。

## 成果物

- 記事タイトル: `AIで始めたnote運用で、公開後ログまで見て初めて分かったこと`
- 状態: `published`
- スコア: `86/100`
- 文字種別: 無料の通常記事
- 本文文字数: 約1,505字
- 主な証拠素材:
  - 公開済みnote2本
  - 今日のTODO
  - `note-research-2026-05-13.md`
  - `note-article-backlog.md`
  - `short-video-ops-os-publishing-log.md`
- アイキャッチ: 3案作成済み。推奨は `公開後ログ`。

## 検証

- 記事採点: `86/100` で公開候補基準の80点以上。
- 事実確認: note公式告知の募集期間と応募条件、OpenAI release notesの直近更新をWebで確認。
- 公開済みnote反応計測: 未完了。
  - ローカル `curl` は `Could not resolve host: note.com`。
  - Chrome/ArcのComputer UseはMCP側で承認拒否。
- note公開: ユーザーが手動で公開完了。
- `/Users/uryuatsuya/note/articles/drafts/` への保存: 未実施。現在のサンドボックスの書き込み許可範囲外。

## ブロッカー

- noteの反応値取得と公開操作には、ブラウザ操作権限またはログイン済みブラウザの使用許可が必要。
- `#AIと始めてみた` はGoogle AI体験が審査対象と公式告知に明記されているため、今回のCodex中心記事では公開タグから外す判断。

## 次アクション

1. ブラウザ権限が使える状態で、公開済み2本のスキ、コメント、フォロー、プロフィール遷移、DMを計測する。
2. 今日公開した記事の24h/72h計測を行う。
3. `AgentRunShowcaseShort` を公開し、公開URL、時刻、投稿先、初動反応、5件アウトリーチ候補を埋める。

## 2026-05-13 公開追記

- 公開URL: `https://note.com/glad_shrew1020/n/nb451e94f6a35`
- 公開時刻: `2026-05-13 13:31:11 JST`
- タグ: `#note`, `#記事`, `#反応`, `#公開`
- 初期反応: スキ0、コメント0。フォロー、プロフィール遷移、DMは未計測。
- 24h計測: `2026-05-14 13:31 JST`
- 72h計測: `2026-05-16 13:31 JST`
- 検証: 公開ページHTTP 200、canonical URL、schema.org `datePublished` を確認。
- コーヒーとAI要素: 朝会でAI運用ログを優先したため、今回の記事から外れた。次記事候補として `朝のコーヒーとAI朝会をセットにする仕事ルーティン` をバックログへ追加。

## 2026-05-13 方針修正

- ユーザー指示: コーヒー×AI系を優先する。
- 修正内容: 次のnote候補を `朝のコーヒーとAI朝会をセットにする仕事ルーティン` に変更。
- 作成: `company/marketing/content-plan/2026-05-13-coffee-ai-morning-routine-brief.md`
- 作成: `company/pm/tickets/2026-05-13-coffee-ai-morning-routine-note.md`
- 次アクション: 次の制作枠で、コーヒーを「飾り」ではなくAI朝会を始める生活導線として本文化する。

## 2026-05-13 コーヒーAI記事制作追記

- 記事タイトル: `朝のコーヒーとAI朝会をセットにしたら、仕事の始め方が変わった`
- 記事ファイル: `company/marketing/content-plan/2026-05-13-coffee-ai-morning-routine.md`
- 状態: `ready_not_published`
- スコア: `85/100`
- 本文文字数: 約1,504字
- 参考確認: SCAJ2026開催概要、全日本コーヒー協会統計資料。
- 次アクション: noteへ公開し、URLと公開時刻を記録する。

## 2026-05-13 コーヒーAI公開試行

- 試行: Chromeのログイン済みnoteで `https://note.com/notes/new` を開いた。
- 結果: `editor.note.com/notes/n5cd83998b3d9/edit/` と `editor.note.com/notes/n51bbdf937ca5/edit/` への遷移は発生したが、編集画面本文領域が白紙表示のままだった。
- 判断: タイトル、本文、タグ、公開ボタンを確認できないため、公開済みとして扱わない。
- 現在状態: 記事本文、CTA、タグ候補、アイキャッチ方向、採点、公開前チェックは完了。note転記と公開のみ未完了。

## 2026-05-13 コーヒーAI公開完了

- 公開URL: `https://note.com/glad_shrew1020/n/n8dd878a215bc`
- 公開時刻: `2026-05-13 13:54:14 JST`
- タグ: `#コーヒー`, `#今日`, `#仕事`, `#時間`, `#note`
- 初期反応: 公開直後のフィード表示ではスキ0、コメント0相当。フォロー、プロフィール遷移、DMは未計測。
- 検証: 公開ページHTTP 200、タイトル、schema.org `datePublished` を確認。
- 24h計測: `2026-05-14 13:54 JST`
- 72h計測: `2026-05-16 13:54 JST`
