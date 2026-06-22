---
date: "2026-06-22"
type: engineering-policy
status: active
source: "https://addyosmani.com/blog/loop-engineering/"
---

# Loop Engineering Policy

## 目的

MyLife の Codex / Claude Code automation は、単発プロンプトの積み増しではなく、発見、割当、検証、記録、次アクションを回す loop として設計する。

Loop engineering は「人間が毎回 agent に指示する」のではなく、「agent に何を見つけ、どう実行し、何を完了条件にし、どこへ記録するか」を先に設計する運用である。

## 採用する考え方

- automation は heartbeat として扱う。定時に状況を見て、やることがなければ短く終了する。
- worktree / branch / thread を分け、複数 agent や複数 slice が同じ checkout を壊さないようにする。
- recurring context は prompt へ貼らず、`AGENTS.md`、`CLAUDE.md`、skill、project docs、automation memory に外出しする。
- connector / plugin は、filesystem だけでは完結しない issue、PR、mail、calendar、Slack、GitHub、Notion などの実環境接続に使う。
- sub-agent または role split を使い、実装者と検証者を分ける。少なくとも report 上では Implementation / Review / Verification / Sync を分離する。
- state は会話内ではなく disk に残す。MyLife では `company/`、対象 repo、`~/.codex/automations/*/memory.md` を正とする。

## MyLife での標準 loop

| 段階 | 役割 | MyLife での置き場所 |
|---|---|---|
| Discover | 未完了、blocker、差分、外部変化を見つける | `company/todos/`, `company/projects/`, repo git state |
| Triage | 今日扱う最小 slice を1つに絞る | `company/notes/`, automation memory |
| Execute | 対象 repo で実装または文書更新を行う | project repo / `company/engineering/docs/` |
| Verify | test、lint、diff review、source check を行う | terminal output, PR, review note |
| Record | 何を変えたか、なぜ、未解決事項を戻す | `company/notes/`, `company/projects/`, `company/decisions/` |
| Decide next | 次回の1手だけを残す | automation memory |

## 運用ルール

1. 1 loop は原則1 objective、1 slice、1 verification に絞る。
2. loop の完了条件は、作業開始前に検証可能な形で書く。
3. 「done」は agent の主張ではなく、確認済みの証拠で扱う。
4. 同じ説明を2回以上 prompt に貼ったら、skill、policy、runbook、memory のいずれかへ移す。
5. loop が失敗した場合は、再試行より先に category を `code_failure`, `environment`, `network`, `permission`, `credential`, `external_service` に分類する。
6. 同じ blocker が続く場合、新しい TODO を増やさず、解除条件だけを更新する。
7. token cost が見合わない loop は止める。特に調査系 loop は、前回情報が古いか判断に必要な時だけ実行する。
8. 人間が理解していない変更を、loop の成果として production へ進めない。

## 禁止事項

- prompt を巨大化して loop の代わりにしない。
- 検証 agent と実装 agent を同じ判断基準にしない。
- automation memory を履歴ログとして肥大化させない。
- CI / test 未確認のまま「自動で直った」と記録しない。
- worktree や branch の分離なしに、複数 agent へ同じ repo の編集を任せない。
- loop の出力を読まずに merge / publish / production promotion しない。

## XGuard / MyLife への適用

- XGuard weekday implementation は既存方針どおり、最新状態の確認、最小 slice、targeted verification、push、MyLife sync までを1 loop とする。
- Monday planning は、新規計画を増やす loop ではなく、未完了 objective の重複を防ぐ triage loop とする。
- IT / coffee reading は production TODO に展開しない。読み物 loop は `company/reading/` で完結させる。
- エラー再発時は `company/engineering/error-patterns.md` に原因、検出、回復、停止条件を残す。
- 重要な技術判断は `company/decisions/` または対象 project note に戻す。

## 最小チェックリスト

- [ ] この loop の objective は1文で言えるか。
- [ ] 完了条件は test / lint / diff / source / human review のどれで確認するか。
- [ ] 状態の正本は会話外にあるか。
- [ ] 実装者と検証者の役割が分かれているか。
- [ ] 次回に必要な情報だけが memory に残っているか。
- [ ] 人間が読むべき差分、リスク、未解決事項が明記されているか。

## 参照

- Addy Osmani, "Loop Engineering", 2026-06-07: https://addyosmani.com/blog/loop-engineering/
- MyLife: `company/engineering/docs/2026-06-11-agent-harness-audit.md`
- MyLife: `company/engineering/docs/2026-06-11-automation-token-budget.md`
