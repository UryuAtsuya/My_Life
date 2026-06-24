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

## Loop Engineering 運用
- recurring work は単発プロンプトではなく loop として扱う。正本は `company/engineering/docs/2026-06-22-loop-engineering-policy.md`。
- 部門横断の company work は stage 接続として扱う。正本は `company/engineering/docs/2026-06-24-company-harness-engineering-policy.md`。
- Claude Code は What / Why / Priority / Record を主導し、Codex は How / Implementation / Verification を主導する。
- loop は Discover → Triage → Execute → Verify → Record → Decide next の順で進める。
- 1 loop は原則1 objective、1 slice、1 verification に絞り、未完了 objective の日次複製を避ける。
- 完了条件は作業前に test / lint / diff / source / human review のいずれかで確認可能にする。
- recurring context は prompt に貼り足さず、`AGENTS.md`、`CLAUDE.md`、skill、project docs、automation memory へ外出しする。
- state は会話ではなく disk に残す。最新状態、未解決 blocker、次の1手は `company/`、対象 repo、`~/.codex/automations/*/memory.md` に戻す。

### Codex 連携ルール
1. コーディングタスクは GitHub Issue として起票
2. Codex に Issue を割り当て、実装を委譲
3. PR が作成されたら Claude Code でレビュー
4. マージ後、Projects/ 内のドキュメントを更新

### GitHub / PR 運用
- 共通ルールの正本は `company/engineering/docs/2026-06-24-github-pr-policy.md`。
- 実装作業は原則として新しい `feature/*` / `fix/*` / `docs/*` branch で行い、完了後に push して PR を作成する。
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く。
- merge は原則ユーザーが行う。Claude Code / Codex は merge 可能な状態を作り、PR URL と未解決事項を報告する。

## 関連 Vault
- **EngineerBrain** (`~/Documents/ObsidianVault/EngineerBrain/`) — 技術ナレッジ・スキル・成長記録

## Git 管理
- リモート: `https://github.com/UryuAtsuya/My_Life`
- `.gitignore` に `.obsidian/workspace.json`, `node_modules/` を含める
- company Todo など共有すべき変更は、作業完了時に commit して push する
