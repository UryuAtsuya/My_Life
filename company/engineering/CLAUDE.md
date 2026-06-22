# 開発

## 役割
技術ドキュメント、設計書、デバッグログを管理する。

Codex を主担当にし、実装、コードレビュー、テスト、技術検証を進める。Claude Code は CEO / PM 側の判断、優先順位、ドキュメント整理で連携する。

## ルール
- 技術ドキュメントは `docs/topic-name.md`
- デバッグログは `debug-log/YYYY-MM-DD-issue-name.md`
- デバッグのステータス: open → investigating → resolved → closed
- 設計書は必ず「概要」「設計・方針」「詳細」の構成にする
- バグ修正時は「再発防止」セクションを必ず記入
- 技術的な意思決定はCEOのdecisionsにもログを残す
- Codex が実装やレビューを行った場合は、対象リポジトリ、検証結果、未解決事項、次の候補を `company/projects/` または `company/notes/` に戻す
- CEO 判断が必要な仕様変更、優先順位変更、リスク受容は Claude Code 側へ返す
- loop engineering の正本は `docs/2026-06-22-loop-engineering-policy.md` とする
- 開発 automation は Discover → Triage → Execute → Verify → Record → Decide next の順で主導する
- 1回の開発 loop は最小の unfinished slice を1つだけ扱い、検証結果を1つ以上残す
- 実装者と検証者を分ける。sub-agent が使えない場合も、Implementation / Review / Verification / Sync を分けて記録する
- 同じ前提説明や手順が2回出たら、prompt ではなく `docs/`、`error-patterns.md`、skill、automation memory のいずれかに昇格する
- loop が止まった場合は `code_failure`, `environment`, `network`, `permission`, `credential`, `external_service` に分類し、再発する原因は `error-patterns.md` に追加する

## フォルダ構成
- `docs/` - 技術ドキュメント・設計書
- `debug-log/` - デバッグ・バグ調査ログ
