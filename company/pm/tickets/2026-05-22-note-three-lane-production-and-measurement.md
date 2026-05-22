---
created: "2026-05-22"
project: "note-article-flow"
assignee: "codex"
priority: high
status: active
---

# 2026-05-22 note 3レーン制作と計測ブロッカー

## 目的

AI仕事ログ24h、MBTI紹介note72h、既存note/coffee実測を回収した上で、AI / coffee / MBTI の次公開順を決める。

## 完了条件

- [x] 2026-05-22版AI記事を作成し、採点80点以上を確認する
- [x] 2026-05-22版coffee記事を作成し、採点80点以上を確認する
- [x] 2026-05-22版MBTI記事を作成し、採点80点以上を確認する
- [x] 各記事にタイトル、リード、本文、CTA、タグ、アイキャッチ案、alt text、採点、公開前チェック、投稿後計測欄を入れる
- [x] MBTI記事に参照URL、確認日、追加サイテーション、未確認事項を残す
- [ ] MBTI紹介note72h反応を管理画面または手動で回収する
- [ ] AI仕事ログ記事24h反応を `2026-05-22 15:04 JST` 以降に回収する
- [ ] 既公開note/coffee記事の管理画面実測を同じ表で回収する
- [ ] `/Users/uryuatsuya/note/articles/drafts/` へ構造化ドラフトを保存する
- [ ] noteへ転記し、公開URL、公開時刻、公開タグ、初期反応、24h/72h計測予定を記録する

## 作成済み記事

| レーン | ファイル | スコア | 状態 |
|---|---|---:|---|
| AI | `company/marketing/content-plan/note/AI/2026-05-22-codex-mobile-work-log.md` | 86 | `ready_not_published` |
| coffee | `company/marketing/content-plan/note/coffee/2026-05-22-coffee-bean-three-criteria.md` | 84 | `ready_not_published` |
| MBTI | `company/marketing/content-plan/note/MBTI/2026-05-22-love-type-three-questions.md` | 84 | `ready_not_published` |

## ブロッカー

- `curl` で `note.com` がDNS解決不可のため、公開ページ確認と反応回収ができない。
- note管理画面はブラウザ操作が必要。ログイン状態、公開画面、管理画面数値は未確認。
- `/Users/uryuatsuya/note/articles/drafts/` は `not_writable` のため、外部構造化ドラフト保存ができない。

## 次アクション

1. `2026-05-22 15:04 JST` 以降にAI仕事ログ記事の24h反応を回収する。
2. MBTI紹介note72hと既存coffee実測を同じ表に入れる。
3. 実測が取れたら、公開順を `AI follow-up / coffee / MBTI` から1本だけ確定し、公開URLと時刻をVaultへ戻す。

## 2026-05-22 Evening Closeout

- Done: 2026-05-22版AI/coffee/MBTI記事3本、PMチケット、昼制作ノートを作成済み。
- Verified: `tidy -q -e Projects/solo-business-today-board/index.html` はエラー出力なし。
- Not done: AI仕事ログ24h、MBTI紹介note72h、既存note/coffee管理画面実測、3本のnote転記・公開、外部ドラフト保存。
- Blockers: ローカル `curl` は `note.com` をDNS解決できない。note管理画面は手動またはブラウザ操作権限が必要。`/Users/uryuatsuya/note/articles/drafts/` は `not_writable`。
- Next: 2026-05-23は実測回収を先に閉じ、公開する1本だけを決める。
