# Claude Code 定時運用プロンプト

## 目的
Claude Code を CEO / PM / 秘書寄りの判断と会社運用に使い、Codex を開発・レビュー・技術検証に集中させる。

## 推奨スケジュール
| 時刻 | プロンプト | 主担当 | 役割 |
|------|------------|--------|------|
| 07:30 | `0730-ceo-morning-planning.md` | Claude Code | 今日の優先順位、判断、Codex への実装スコープ整理 |
| 12:45 | `1245-pm-codex-handoff.md` | Claude Code | 昼の Codex 実装前に、入力情報と完了条件を整える |
| 19:00 | `1900-ceo-evening-closeout.md` | Claude Code | Codex 実装・レビュー結果を読んで、明日の Top 3 と意思決定を整理 |

## Codex 側との分担
- Claude Code は「何をやるか」「なぜやるか」「何を引き継ぐか」を決める。
- Codex は「どう実装するか」「どう検証するか」「レビューで何が危ないか」を詰める。
- Claude Code は、Codex の実装時間中に同じ実装リポジトリを直接編集しない。
- 両方が更新する正本は `company/` にし、重要な判断は `company/decisions/` に残す。

## 実行前提
- 作業ルート: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`
- GitHub 同期先: `https://github.com/UryuAtsuya/My_Life`
- XGuard 実装リポジトリ: `/Users/uryuatsuya/XGuard/xguard`
- XGuard GitHub: `https://github.com/UryuAtsuya/Xguard`

## 共通ルール
- まず `git pull --ff-only` または同等の同期確認を行い、remote 先行があれば無理に書かない。
- 既存の無関係な変更や未追跡ファイルは巻き戻さない。
- 更新対象は `company/` の会社運用ドキュメントを中心にする。
- 共有すべき変更がある場合は、対象ファイルだけを commit / push する。
- 変更がない場合は、無理に空の記録を作らない。
