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
- XGuard は `develop` をstaging、`main` をproductionとして扱い、通常実装を `feature/*` または `develop` へ反映する
- XGuard の `main` には直接実装pushせず、staging検証済みの `develop` からproductionへ昇格する
- Codex がsubagentを利用できる場合は、agent id、担当範囲、base SHA、status、成果物を記録し、write agentを分離されたworktree/branchで動かす。重複するfile ownershipを与えず、MyLife共有文書、統合、commit、pushはmain coordinatorが持つ
- Sync担当は `Sync planner` として更新対象と反映案を返し、MyLife共有文書を直接編集しない
- commit前に全agentを完了、失敗、timeoutのいずれかへ確定し、稼働中agentを残さない
- subagentが利用不可または修正再試行後も失敗した場合は、順次role passへ切り替え、同一coordinatorによるfallbackで独立reviewではないことと理由を記録する
- 片方の作業で発生した重要な判断・レビュー結果・未解決事項は `company/` 側へ戻し、次の担当が引き継げる状態にする
- 共有すべき変更は作業完了時に `git commit` して `git push` する

## GitHub / PR 運用

- 共通ルールの正本は `company/engineering/docs/2026-06-24-github-pr-policy.md`
- 実装作業は原則として新しい `feature/*` / `fix/*` / `docs/*` branch を作って進める
- 完了後は検証結果を残し、push して Pull Request を作成する
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く
- merge は原則ユーザーが行う。agent は勝手に merge せず、PR URL と判断材料を返す
- 直接 push は、ユーザーが明示した場合、緊急同期、automation memory など PR より即時反映が重要な小変更に限る

## 同期先

- GitHub: `https://github.com/UryuAtsuya/My_Life`
- Local: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

## 基本フロー

1. `MyLife/company/` を更新する
2. `git status` で差分を確認する
3. 共有対象だけを stage する
4. `git commit` する
5. `git push` する
