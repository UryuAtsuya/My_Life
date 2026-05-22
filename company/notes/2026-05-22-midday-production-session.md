---
date: "2026-05-22"
type: midday-production-session
status: complete
---

# 2026-05-22 midday production session

## 実行確認

- システム日付: `2026-05-22`
- 実行時刻: `2026-05-22 14:23 JST`
- 参照: `CLAUDE.md`, `company/sync-policy.md`, automation memory, `company/todos/2026-05-22.md`, `company/notes/2026-05-22-morning-business-meeting.md`, `company/decisions/2026-05-22.md`, `company/marketing/content-plan/note-research-2026-05-22.md`, note編集OS, noteバックログ, 関連PMチケット, active project files

## 今日作ったもの

| レーン | 成果物 | スコア | 状態 |
|---|---|---:|---|
| AI | `company/marketing/content-plan/note/AI/2026-05-22-codex-mobile-work-log.md` | 86/100 | `ready_not_published` |
| coffee | `company/marketing/content-plan/note/coffee/2026-05-22-coffee-bean-three-criteria.md` | 84/100 | `ready_not_published` |
| MBTI | `company/marketing/content-plan/note/MBTI/2026-05-22-love-type-three-questions.md` | 84/100 | `ready_not_published` |
| PM | `company/pm/tickets/2026-05-22-note-three-lane-production-and-measurement.md` | - | active |

## 判断

- 朝会の結論どおり、今日の本来の最優先は実測回収。ただし `curl` で `note.com` がDNS解決不可のため、MBTI紹介note72h、AI仕事ログ24h、既存coffee実測は未回収。
- AI仕事ログ24hは `2026-05-22 15:04 JST` 到達前のため、AI follow-up記事には反応値を入れていない。
- MBTI紹介note72hは `2026-05-22 14:10 JST` 到達済みだが、管理画面実測は取れていない。MBTI続編には実測値を入れていない。
- 3本とも80点以上だが、実測未取得、note.com到達不可、外部drafts保存不可のため、公開は未実施。

## 検証

- `date +%F` で日付確認済み。
- `tidy -q -e Projects/solo-business-today-board/index.html` はエラー出力なし。
- `curl -L -I --max-time 10 https://note.com/glad_shrew1020/n/neaf5658d3765` は `Could not resolve host: note.com`。
- `curl -L -I --max-time 10 https://note.com/glad_shrew1020/n/n4c24cc339e2a` は `Could not resolve host: note.com`。
- `/Users/uryuatsuya/note/articles/drafts` は `not_writable`。
- `tidy` によるHTML検証後、Chrome表示確認を試したが、`open -a 'Google Chrome'` / `open -b com.google.Chrome` はアプリ解決に失敗し、Computer Useは `approval denied`。実ブラウザ表示確認は未完了。

## 未完了

- note管理画面の実測回収。
- 3本のnote転記、下書き保存、公開URL取得。
- `/Users/uryuatsuya/note/articles/drafts/YYYYMMDD-{slug}.md` への構造化ドラフト保存。
- Today Boardの実ブラウザ表示スクリーンショット取得。

## 午後以降の上位TODO

1. `2026-05-22 15:04 JST` 以降にAI仕事ログ記事24hを回収し、AI follow-upを公開するか決める。
2. MBTI紹介note72hと既存coffee実測を同じ表で回収し、改善対象を1つに絞る。
3. 公開順を1本だけ確定し、noteへ転記・公開後、URL、時刻、タグ、初期反応、24h/72h予定を戻す。
