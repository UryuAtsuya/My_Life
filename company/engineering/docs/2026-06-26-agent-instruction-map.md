# Agent Instruction 分割ルール

## 目的

`AGENTS.md` と `CLAUDE.md` を長い運用マニュアルにしすぎず、agent が最初に読む入口と、用途別の詳細ルールを分ける。

## 基本方針

- root の `AGENTS.md` / `CLAUDE.md` は、Vault の目的、役割分担、必読ルールへの導線だけを持つ。
- 実行ルールは用途別 md を正本にする。
- 新しい recurring rule を追加するときは、root に長文を足さず、まず該当する用途別 md に追記する。
- root に追記するのは、将来の agent が詳細mdへ到達するための短い参照に限る。
- 既存ルールと矛盾する場合は、より具体的な用途別 md を優先し、必要なら root の参照を更新する。

## 正本の分け方

| 領域 | 正本 | 用途 |
|------|------|------|
| Vault 全体の入口 | `AGENTS.md`, `CLAUDE.md` | 目的、役割分担、必読ルールへの導線 |
| Company 同期 | `company/sync-policy.md` | company の保存先、commit / push、Claude Code / Codex の連携 |
| Loop Engineering | `company/engineering/docs/2026-06-22-loop-engineering-policy.md` | recurring work、1 objective / 1 slice / 1 verification |
| Company stage / handoff | `company/engineering/docs/2026-06-24-company-harness-engineering-policy.md` | Secretary -> CEO -> PM -> Engineering -> Reviews -> Record |
| GitHub Issue / PR / 証拠 | `company/engineering/docs/2026-06-24-github-pr-policy.md` | Issue 起票、既存Issue確認、branch、PR、証拠md |
| CEO 判断 | `company/ceo/CLAUDE.md` | 優先順位、Go / No-Go、Codex へ渡す条件 |
| Engineering 実行 | `company/engineering/CLAUDE.md` | 実装、レビュー、検証、技術判断の戻し先 |
| Active project inventory | `company/projects/codex-active-projects.md` | Codex 管理対象、現状、次の1手 |

## 追加時の判断

- GitHub、branch、PR、commit、証拠mdに関わるなら `2026-06-24-github-pr-policy.md`。
- loop、automation、繰り返し実行の完了条件なら `2026-06-22-loop-engineering-policy.md`。
- 部署間の受け渡し、owner、handoff、stageなら `2026-06-24-company-harness-engineering-policy.md`。
- CEO の判断軸、優先順位、Go / No-Goなら `company/ceo/CLAUDE.md`。
- プロジェクトの現状、未解決 blocker、次の1手なら `company/projects/codex-active-projects.md` または対象 project note。

## root 更新の型

root に足す場合は、詳細説明ではなく次の形にする。

```markdown
- <領域> の正本は `<path>`。
```

root で運用手順を再説明しない。同じ内容が複数箇所にあると、agent が古い片方だけを読んで誤動作するため。
