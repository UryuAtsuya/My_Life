---
date: "2026-06-24"
type: engineering-policy
status: draft
source_issue: "https://github.com/UryuAtsuya/My_Life/issues/4"
sources:
  - "https://developers.gmo.jp/technology/81389/"
  - "https://qiita.com/nogataka/items/d1b3fcf355c630cd7fc8"
  - "https://openai.com/ja-JP/index/harness-engineering/"
---

# Company Harness Engineering Policy

## 目的

MyLife の `company/` を、部署別の文書置き場ではなく、部門が同じ objective を受け渡しながら完了まで進める実行ハーネスにする。

ここでのハーネスは、AI agent の出力を人間の注意力だけに依存させず、ルール、スキル、実行契約、検証、記録、復旧で制御する仕組みである。

## 採用する考え方

- ルールは「お願い」ではなく、完了条件と検証手段に接続する。
- 部門は自由に文書を増やす単位ではなく、run の中で役割を持つ stage として扱う。
- AI agent の自律性は、観測、実行、検証、復旧、エスカレーションが揃った範囲だけで上げる。
- prompt を増やして制御するのではなく、`AGENTS.md`、`CLAUDE.md`、policy、skill、automation memory、GitHub Issue / PR に制御を分散する。
- ハーネスそのものも保守対象にする。古いルール、重複 TODO、動いていない automation は定期的に減らす。

## Company 部門接続モデル

| Stage | 主担当 | 受け取るもの | 返すもの | 保存先 |
|---|---|---|---|---|
| Intake | secretary | GitHub Issue、inbox、外部リンク、ユーザー指示 | objective 草案、分類、期限 | `company/secretary/`, GitHub Issue |
| Direction | ceo | objective 草案、事業上の制約 | 優先順位、Go / No-Go、成功条件 | `company/ceo/`, `company/decisions/` |
| Planning | pm | 優先順位、成功条件 | 最小 slice、owner、完了条件 | `company/pm/`, `company/todos/` |
| Research | research | 未検証の前提、外部変化 | source summary、リスク、判断材料 | `company/research/`, `company/reading/` |
| Implementation | engineering | slice、完了条件、対象 repo | 実装、文書更新、verification result | 対象 repo、`company/engineering/` |
| Review | reviews | diff、result、source | P0/P1/P2 指摘、merge 判断材料 | `company/reviews/` |
| Growth | marketing | 完了済み成果、公開可否 | 発信案、キャンペーン、顧客接点 | `company/marketing/` |
| Record | secretary / pm | 完了結果、未解決事項 | 次の1手、blocker、closeout | `company/notes/`, automation memory |

## Run Contract

部門横断の recurring work は、次の情報を持つ run として扱う。

```yaml
run_id: company-YYYY-MM-DD-topic
source_issue: https://github.com/UryuAtsuya/My_Life/issues/N
status: planned|ready|running|blocked|failed|verified|closed
objective: 1文の目的
owner: secretary|ceo|pm|research|engineering|reviews|marketing
handoff_from: path-or-url
handoff_to: next-stage
success_check:
  type: diff|source|test|lint|human_review
  command_or_evidence: TODO
required_artifacts:
  - updated_policy
  - verification_summary
blockers: []
next_action: 1つだけ
```

`status` は自由文で増やさない。未実行は `planned`、人間判断待ちは `blocked`、実行したが失敗したものは `failed` と分ける。

## 部門別の運用ルール

### Secretary

- Issue、会話、外部リンクを受けたら、まず objective と分類を1文にする。
- 同じ依頼を別 TODO として複製せず、既存 run または project note に接続する。
- closeout では履歴全文ではなく、最新状態、未解決 blocker、次の1手だけを残す。

### CEO

- 優先順位、事業判断、Go / No-Go を決める。
- 判断がないまま engineering に流さない。
- production promotion、外部公開、費用発生、法務・規約リスクは CEO stage を必須にする。

### PM

- objective を 1 slice に切る。
- 完了条件を test / lint / diff / source / human review のどれで確認するか明記する。
- owner、期限、解除条件がない blocker を日次 TODO に増やさない。

### Research

- 外部リンクは source title、URL、1行要約、なぜ重要かに圧縮する。
- 調査結果は実装 TODO に直接膨らませず、CEO / PM の判断材料として渡す。
- 古い調査を再利用する場合は、更新確認が必要かを明記する。

### Engineering

- 実装、検証、PR は `company/engineering/docs/2026-06-24-github-pr-policy.md` に従う。
- 重要な技術判断は `company/decisions/` または対象 project note に戻す。
- 繰り返す失敗は `company/engineering/error-patterns.md` に分類、検出、回復、停止条件として残す。

### Reviews

- 指摘は P0 / P1 / P2 で分類し、merge blocker と改善候補を分ける。
- 変更を読まずに承認しない。
- verification result がない場合は「未検証」として返す。

### Marketing

- 完了していない実装を公開予定やキャンペーンにしない。
- 公開前に CEO の Go と Reviews の未解決 P0 / P1 なしを確認する。
- 成果物は顧客接点、事例、LP、投稿案に変換するが、実装 source of truth を置き換えない。

## Policy 追加・修正候補

### 追加する

- `company/automation/runs/` に run contract の実体を置く。
- `company/automation/blockers/` に人間対応が必要な blocker を owner / due /解除条件つきで置く。
- `company/reviews/` に PR / docs / automation の review note を集約する。
- `company/marketing/` は verified 成果だけを受け取るルールを持つ。

### 修正する

- `AGENTS.md` と `CLAUDE.md` は詳細ルールを増やさず、この policy と Loop Engineering Policy へ誘導する。
- `company/sync-policy.md` は部門別の保存先に加え、stage と handoff の考え方を反映する。
- automation memory は履歴ではなく、最新状態、未解決 blocker、次の1手に限定する。
- GitHub Issue は intake、PR は review / merge 判断の窓口として扱い、Issue 本文を作業ログ化しない。

### まだ自動化しない

- 全部門の hook 化。
- merge / production promotion の自動実行。
- 外部公開や marketing 発信の自動実行。
- credentials、billing、法務判断を伴う処理の自動解決。

## 導入順序

1. Issue #4 をこの policy として採用し、root 指示から参照する。
2. `company/automation/runs/` の最小 run contract template を作る。
3. XGuard など既存 recurring work を1件だけ run contract 化する。
4. Secretary -> CEO -> PM -> Engineering -> Reviews -> Record の受け渡しを1 loop で試す。
5. 週次で重複 TODO、未検証 done、古い automation memory を削る。

## 参照

- `company/engineering/docs/2026-06-22-loop-engineering-policy.md`
- `company/engineering/docs/2026-06-11-agent-harness-audit.md`
- `company/engineering/docs/2026-06-24-github-pr-policy.md`
