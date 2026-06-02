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

## フォルダ構成
- `docs/` - 技術ドキュメント・設計書
- `debug-log/` - デバッグ・バグ調査ログ
