# Company Sync Policy

## 方針

`MyLife/company/` を会社運用、Todo、意思決定、会議メモ、プロジェクト進行の正本として扱う。

`Skills_Export` は日常運用名として分かりにくくなったため、今後は company Todo やプロジェクト管理の作業場所にしない。旧場所に情報が残っている場合は、必要な内容を整理してこの Vault に取り込む。

## 同期ルール

- company Todo は `company/todos/` と `company/secretary/todos/` に集約する
- 意思決定は `company/decisions/`、会議・作業メモは `company/notes/` に残す
- 進行中プロジェクトの管理メモは `company/projects/` に置く
- Claude Code と Codex はこのディレクトリを共通の作業ルートとして扱う
- Claude Code は CEO / PM / 秘書寄りの判断、優先順位整理、会社運用、ドキュメント作成を主担当にする
- Codex は開発、コードレビュー、技術検証、実装タスク、PR ベースの変更管理を主担当にする
- 並行作業では Claude Code が「何をやるか」を整理し、Codex が「どう実装・検証するか」を具体化する
- 片方の作業で発生した重要な判断・レビュー結果・未解決事項は `company/` 側へ戻し、次の担当が引き継げる状態にする
- 共有すべき変更は作業完了時に `git commit` して `git push` する

## 同期先

- GitHub: `https://github.com/UryuAtsuya/My_Life`
- Local: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

## 基本フロー

1. `MyLife/company/` を更新する
2. `git status` で差分を確認する
3. 共有対象だけを stage する
4. `git commit` する
5. `git push` する
