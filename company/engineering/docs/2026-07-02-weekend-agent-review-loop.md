---
date: "2026-07-02"
type: engineering-policy
status: draft
source_issue: "https://github.com/UryuAtsuya/My_Life/issues/14"
---

# Weekend Agent Review Loop

## 目的

土日の automation 枠を、通常の実装継続ではなく `AGENTS.md`、skills、automation memory、error patterns、PR 運用の見直しに使う。

開発を常に続けるほど、良かった判断、繰り返した失敗、保存すべき前提が増える。週末 review loop は、それらを会話ログではなく実際の運用ファイルへ戻すための時間にする。

## 設計・方針

- 土日の主目的は新規実装ではなく、運用品質の改善にする。
- 対象は `AGENTS.md`、`CLAUDE.md`、skills、`company/engineering/error-patterns.md`、`~/.codex/automations/*/memory.md`、GitHub / PR policy とする。
- 変更は必ず branch を切り、PR で人間が review できる状態にする。
- 1 run で扱う改善は1テーマに絞る。例: branch 運用、memory 肥大化、error pattern 昇格、XGuard loop の読み込み順。
- 実装 repo の production code は原則触らない。必要な場合は通常の実装 Issue として別 branch に分ける。

## 標準 loop

| 段階 | やること | 完了条件 |
|---|---|---|
| Discover | 直近の Issue / PR / closeout / automation memory から再発ミスや良い判断を探す | 1テーマを選ぶ |
| Triage | そのテーマが `AGENTS.md`、skill、policy、memory のどこに属するか決める | 保存先を1つに絞る |
| Execute | 対象ファイルを最小差分で更新する | 不要な再説明を増やさない |
| Verify | `git diff --check`、リンク確認、必要なら該当 repo の軽い test を行う | 1つ以上の確認結果を残す |
| Record | Issue / PR / commit / verification / unresolved を evidence に残す | PR から追える |
| Decide next | 次週に回す改善を1つだけ残す | TODO を増殖させない |

## PR ルール

- branch 名は `docs/weekend-agent-review-YYYY-MM-DD` または `docs/<topic>`。
- PR base は原則 `main`。
- PR 本文には `Closes #<issue>` を入れる。
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く。
- merge はユーザー判断。agent は merge 可能な状態を作るところまで。

## 見直し対象

優先度順:

1. branch / PR を飛ばして直接作業した原因の修正。
2. 2回以上起きた同じエラーの `error-patterns.md` への追加。
3. prompt に貼り続けている長い前提の doc / skill への移動。
4. 古くなった automation memory の短縮。
5. XGuard / MyLife / 診断 repo など、複数 repo 横断で混線したルールの分離。

## 禁止事項

- 週末 review を理由に production code を広く refactor しない。
- 「改善案」だけを増やして PR なしで終えない。
- automation memory に履歴全文を追記しない。
- 既存の未完了 Issue を読まずに新しい運用ルールを増やさない。
- 人間が読んでいない loop 出力を merge / publish の根拠にしない。

## 最小チェックリスト

- [ ] 今回の review テーマは1つか。
- [ ] 保存先は会話外の正本か。
- [ ] PR で人間が差分を確認できるか。
- [ ] 検証結果が1つ以上あるか。
- [ ] 次回へ残す情報は最新状態、未解決 blocker、次の1手だけか。
