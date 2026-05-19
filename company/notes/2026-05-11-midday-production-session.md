---
date: "2026-05-11"
type: midday-production-session
created: "2026-05-11 13:05 JST"
---

# Midday Production Session - 2026-05-11

## 実行対象

今日の最上位テーマは `AgentRunShowcaseShort` の公開、24h/72h計測、5件アウトリーチ接続。外部投稿の実行と実名候補の確定はこの環境だけでは完了できないため、昼の制作では公開後すぐ使える計測・アウトリーチ台帳を作った。

## 作ったもの

- `company/projects/short-video-ops-os-publishing-log.md` を作成。
- 公開URL、公開時刻、投稿先、公開直後メモの記入欄を固定。
- 公開前チェックを `OK / 未確認` で記録できる表にした。
- 24h/72h計測項目を、再生数、3秒維持、完走率、保存、コメント、プロフィールクリック、DM、反応相手の文脈、営業接続メモに固定。
- 初動反応ログに「誰が、何に反応したか、営業接続として意味があるか」を残す欄を作った。
- 5件アウトリーチ候補枠と初回DM文面を用意した。
- `log-to-video-proof.mp4` は初回DMでいきなり押し出さず、相手が反応した後の証拠資産として送る方針にした。

## 検証

- コード・動画生成は行っていないため、lint/render は対象外。
- Markdownの構造確認として、作成後に該当ファイルとPMチケット/TODOの差分を確認する。

## ブロッカー

- `AgentRunShowcaseShort` の実際の公開URL、公開時刻、投稿先は未入力。
- 5件の実名・アカウント名は手元の既存接点から送信直前に埋める必要がある。

## 次の具体アクション

1. `AgentRunShowcaseShort` を公開する。
2. `company/projects/short-video-ops-os-publishing-log.md` にURL、時刻、投稿先を記録する。
3. 24h/72h計測と5件DM送付を開始する。

## 追加実行 - note記事制作 15:55 JST

### 実行対象

午後の優先変更とnote編集部OSに従い、バックログ1位の `note投稿をブラウザ操作で自動化してみた` を制作対象にした。

### 作ったもの

- 記事ファイル: `company/marketing/content-plan/note/AI/2026-05-11-note-browser-publishing-automation.md`
- 本文、CTA、タグ候補、アイキャッチプロンプト3案、alt text、記事スコア、公開前チェック、投稿後計測欄を作成。
- `note-growth-editor` の採点表で87/100と判定。
- PMチケット: `company/pm/tickets/2026-05-11-note-browser-publishing-automation.md`

### 公開状況

- note公開: 実施
- 公開URL: `https://note.com/glad_shrew1020/n/n1513d700bef0`
- 公開時刻: `2026-05-11 16:04 JST`
- タグ: `#AI活用`, `#生成AI`, `#Codex`, `#note`
- 公開条件: 記事品質、証拠素材、CTA、タグ、計測欄を満たした。

### 検証

- 記事採点: 87/100
- 根拠チェック: 公開済みnote URL、Vault内の運用ログ、`note-growth-editor`、automation memoryに基づく。根拠のない数値・実績は入れていない。
- ブラウザ検証: ChromeのComputer Useでタイトル、本文、タグを転記し、ユーザー明示許可に基づいて `投稿する` を実行。
- 公開確認: `curl -L` で公開URLへアクセスし、HTTP 200、title、canonical URL、schema.org `datePublished` を確認。

### 次の具体アクション

1. 24h `2026-05-12 16:04 JST` にスキ、コメント、フォロー、プロフィール遷移、DMを確認する。
2. 72h `2026-05-14 16:04 JST` に同じ項目を再確認する。
3. 反応から次の記事テーマまたはCTA改善を決める。
