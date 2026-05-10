# MyLife Vault

## プロジェクト概要
日常運用・会社管理・プロジェクト進行を一元管理する Obsidian Vault。
GitHub (UryuAtsuya/My_Life) と同期し、履歴管理を行う。

## 今後の運用方針
- `Skills_Export` はスキル配布・退避名として分かりにくくなったため、日常運用・会社Todo・プロジェクト管理の主作業場所にはしない。
- company Todo、意思決定、会議メモ、プロジェクト進行はこの `MyLife` Vault の `company/` を正とする。
- Claude Code と Codex はこのディレクトリを共通の作業ルートとして扱い、同じ GitHub リポジトリへ反映する。
- 旧場所に残っている情報を見つけた場合は、削除より先に `company/` へ整理して取り込む。

## Vault構造
| パス | 用途 |
|------|------|
| `company/` | 会社運用（部署別: secretary, ceo, pm, engineering, marketing, research, reviews） |
| `Projects/` | 進行中プロジェクト（Video_Automation, AIRS, agency-agents 等） |
| `Ideas/` | アイデア・構想 |
| `memo/` | ブレインストーミング・雑記 |

## ツール役割分担
- **Claude Code** — プロジェクト管理・会社運用・意思決定支援・ドキュメント作成
- **Codex** — Projects/ 内のコーディング・実装タスク（issue 駆動・PR ベース）

### Codex 連携ルール
1. コーディングタスクは GitHub Issue として起票
2. Codex に Issue を割り当て、実装を委譲
3. PR が作成されたら Codex でレビュー
4. マージ後、Projects/ 内のドキュメントを更新

## 関連 Vault
- **EngineerBrain** (`~/Documents/ObsidianVault/EngineerBrain/`) — 技術ナレッジ・スキル・成長記録

## Git 管理
- リモート: `https://github.com/UryuAtsuya/My_Life`
- `.gitignore` に `.obsidian/workspace.json`, `node_modules/` を含める
- company Todo など共有すべき変更は、作業完了時に commit して push する
