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
- **Claude Code** — CEO / PM / 秘書寄りの判断、会社運用、意思決定支援、方針整理、ドキュメント作成
- **Codex** — 開発、コードレビュー、技術検証、実装タスク、PR ベースの変更管理

## Loop Engineering 運用
- MyLife の recurring work は、単発プロンプトではなく loop として設計する。正本は `company/engineering/docs/2026-06-22-loop-engineering-policy.md`。
- 部門横断の company work は、Secretary → CEO → PM → Research / Engineering → Reviews → Record の stage として接続する。正本は `company/engineering/docs/2026-06-24-company-harness-engineering-policy.md`。
- loop は Discover → Triage → Execute → Verify → Record → Decide next の順で進める。
- 1 loop は原則1 objective、1 slice、1 verification に絞る。
- 完了条件は作業前に test / lint / diff / source / human review のいずれかで確認可能にする。
- recurring context は prompt に貼り足さず、`AGENTS.md`、`CLAUDE.md`、skill、project docs、automation memory へ外出しする。
- 実装者と検証者の役割を分ける。sub-agent が使えない場合も、Implementation / Review / Verification / Sync を報告上で分離する。
- state は会話ではなく disk に残す。最新状態、未解決 blocker、次の1手は `company/`、対象 repo、`~/.codex/automations/*/memory.md` に戻す。
- loop の出力を読まずに merge / publish / production promotion しない。

### 並行運用ルール
- Claude Code と Codex は同じ `company/` を正本として扱い、担当が違っても記録先を分けすぎない。
- CEO 判断、優先順位、事業方針、部署振り分けは Claude Code を主担当にする。
- コード変更、実装レビュー、テスト、技術的リスクの洗い出しは Codex を主担当にする。
- 両方が触る案件は、Claude Code が「何をやるか」を決め、Codex が「どう実装・検証するか」を詰める。
- Codex が技術的に重要な判断をした場合は、`company/decisions/` または対象プロジェクトの `notes/` に戻す。

### Codex 連携ルール
1. コーディングタスクは GitHub Issue として起票
2. Codex に Issue を割り当て、実装を委譲
3. PR が作成されたら Codex でレビュー
4. マージ後、Projects/ 内のドキュメントを更新

### GitHub / PR 運用
- 共通ルールの正本は `company/engineering/docs/2026-06-24-github-pr-policy.md`。
- 実装作業は原則として新しい `feature/*` / `fix/*` / `docs/*` branch で行い、完了後に push して PR を作成する。
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く。
- merge は原則ユーザーが行う。Codex / Claude Code は merge 可能な状態を作り、PR URL と未解決事項を報告する。

## 関連 Vault
- **EngineerBrain** (`~/Documents/ObsidianVault/EngineerBrain/`) — 技術ナレッジ・スキル・成長記録

## Git 管理
- リモート: `https://github.com/UryuAtsuya/My_Life`
- `.gitignore` に `.obsidian/workspace.json`, `node_modules/` を含める
- company Todo など共有すべき変更は、作業完了時に commit して push する

## ハーネス運用ルール
- automation は週次トークン予算を優先し、同じ調査・TODO・説明を無変更で再生成しない。
- GitHub Issue や外部リンクから始まる依頼は、まず run objective、owner、success check、required artifacts に落としてから部門へ渡す。
- 実装系 automation は差分がある場合だけ重い検証や文書更新を行う。差分がなければ短い状態確認で終了する。
- 1 run は原則1つの実装 slice、1つの検証結果、1つの簡潔な同期記録に絞る。
- 同じ objective が未完了の場合、新しい日次計画を複製せず既存 run を継続する。
- エラーは `code_failure`, `environment`, `network`, `permission`, `credential`, `external_service` に分類する。
- 同じ原因が2回発生した場合、再発防止策を `company/engineering/error-patterns.md` に追加する。
- 原因と対処が再利用可能なら、`harness-self-correction` に従ってルールまたは skill に昇格する。
- automation memory は最新状態、未解決 blocker、次の1手だけを保持し、履歴全文を積み増さない。
