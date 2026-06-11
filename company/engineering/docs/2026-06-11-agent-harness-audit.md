---
date: "2026-06-11"
type: engineering-audit
status: proposed
scope: MyLife company automation / XGuard execution harness
---

# エージェントハーネス稼働監査

## 目的

MyLife の会社運用を、文書を作るだけの定時処理から、実装・検証・記録まで完了する実行ハーネスへ移行する。

## 現状サマリ

| 領域 | 状態 | 判定 |
|---|---|---|
| `company/automation/claude-code/` | 07:30 / 12:45 / 19:00 の役割と出力形式を定義済み | 定義済み |
| Morning XGuard research meeting | `ACTIVE`。最終実績は 2026-06-07 | 停止疑い |
| Midday XGuard implementation session | `ACTIVE`。最終実装実績は 2026-06-07 | 停止 |
| Evening XGuard code review | `ACTIVE`。最終実績は 2026-06-07 | 停止疑い |
| MyLife 日次文書 | 2026-06-10 までは planning / handoff が生成済み | 部分稼働 |
| 2026-06-11 日次文書 | TODO / decision / morning planning が未生成 | 未稼働 |
| XGuard 実装 repo | local `7e33e9f`、remote `c4403d8` で ahead 1 / behind 1 | 4日以上停滞 |
| 実 Supabase test | DB URL / `psql` / Supabase CLI 条件不足で継続 skip | ブロック |
| Vault の Git 管理 | `company/` は管理済み。`Projects/` は約 969MB の大部分が未追跡 | 境界不明瞭 |

## 主要な問題

### P0: ハンドオフが実行を保証していない

12:45 のハンドオフ文書は詳細だが、Codex 実行の run ID、開始時刻、終了状態、成果物が関連付けられていない。2026-06-08 から 2026-06-10 は同じ Top 3 が繰り返され、実装 note が作られていない。

**原因**

- planning と implementation が別々の cron で、依存関係がない
- 前段の出力を後段が受領したことを示す機械可読な状態がない
- run 未実施時に再試行または代替実行へ進む契約がない

### P0: `ACTIVE` と実際の稼働が一致しない

automation 設定の `status = "ACTIVE"` は、直近実行成功を意味しない。最終成功時刻、連続失敗数、次回実行時刻、停止理由を Vault 側から確認できない。

### P1: 完了条件が文書内に閉じている

検証コマンドや push 条件は書かれているが、結果を構造化して判定する仕組みがない。結果として「今日必ず完了」のような強い表現が増えても、未実施を止められない。

### P1: ブロッカーの期限管理が弱い

Supabase CLI、live credentials、DB URL など、人間対応が必要な項目が日次 TODO に転記され続けている。所有者、期限、解除条件、期限超過時の代替策が一つの状態レコードになっていない。

### P1: 観測情報が分散している

実行履歴は `~/.codex/automations/*/memory.md`、業務状態は `company/todos/`、判断は `company/decisions/`、実装状態は XGuard repo に分散している。最新状態を決める優先順位が明文化されていない。

### P2: Vault の管理境界が曖昧

Vault 全体は約 987MB、`Projects/` は約 969MB で、Git 追跡は 2 ファイルのみ。132個の未追跡ファイルがあり、試作、生成物、運用対象の区別がつかない。`Projects/Social_Automation/agent.py` は旧 `Skills_Export` の絶対パスを参照しており、現方針と不整合。

## 強化後の基本構造

```text
Planner
  -> run manifest
  -> Executor
  -> verification result
  -> Reviewer / Closeout
  -> next run or escalation
```

### 1. Run manifest

各日・各案件に一つ、機械可読な実行契約を作る。

```yaml
run_id: xguard-2026-06-11-midday
project: xguard
status: ready
owner: codex
source_handoff: company/notes/2026-06-11-claude-code-codex-handoff.md
workspace: /Users/uryuatsuya/XGuard/xguard
objective: Rebase and push the OAuth production boundary
success_commands:
  - git diff --check
  - npx tsc -p tsconfig.json --noEmit
  - npx vitest run --configLoader runner
required_artifacts:
  - commit_hash
  - push_result
  - verification_summary
retry_limit: 2
fallback: escalate_to_ceo
```

状態は `planned -> ready -> running -> blocked|failed|completed -> verified -> closed` に限定する。

### 2. Executor contract

Executor は自由文だけでなく、必ず次を返す。

```yaml
status: success|warning|error
summary: 一行の結果
next_actions: []
artifacts: []
root_cause: null
retry_instruction: null
stop_condition: null
```

`blocked` と `failed` を分ける。外部 credential 不足は `blocked`、テスト失敗は `failed` とする。

### 3. Watchdog

- 予定時刻から30分後に `running` でなければ1回再実行
- 2回失敗または2時間経過で `escalated`
- 前日と同じ objective が未完了なら、新しい planning 文書を増やさず既存 run を継続
- `ACTIVE` でも24時間実績がなければ警告を生成

### 4. Verification gate

完了は文章ではなく、次を満たした場合だけ確定する。

- success command がすべて exit code 0
- 必須 artifact が存在
- GitHub 反映対象なら remote との差分確認済み
- MyLife 記録先が更新済み
- Reviewer が P0 / P1 未解決を明示

### 5. Single source of truth

優先順位を次に固定する。

1. 実装 repo の live Git 状態
2. run manifest と verification result
3. automation memory
4. TODO / decision / handoff 文書

文書は状態の説明であり、実状態そのものにはしない。

## 実装アプローチ

### Phase 1: 可視化

1. `company/automation/runs/` に run manifest と result schema を追加する。
2. 3つの active automation の最終成功、最終失敗、連続失敗、次回予定を一覧化する。
3. 2026-06-08 から停滞している XGuard run を1件の未完了 run として復元する。

**完了条件:** 「何が動いていないか」を1ファイルで判定できる。

### Phase 2: planning と execution の接続

1. 12:45 handoff は新規文書作成ではなく `ready` manifest 作成を主成果物にする。
2. Midday automation は最新の `ready` manifest だけを取得する。
3. 実行開始時に `running`、終了時に result と status を更新する。

**完了条件:** handoff だけ作られて implementation が未実施、という状態を watchdog が検知できる。

### Phase 3: 回復とエスカレーション

1. network、permission、credential、test failure の分類を統一する。
2. 安全な retry を1回だけ自動実行する。
3. credential や CEO 手動作業は `company/automation/blockers/` に切り出す。
4. 期限超過時は翌日 TODO の複製ではなく、owner への escalation を作る。

**完了条件:** 同じ TODO が3日連続で複製されない。

### Phase 4: 評価

週次で次を計測する。

- scheduled runs
- started runs
- completed runs
- verified runs
- completion rate
- retries per run
- blocker age
- handoff-to-start latency
- start-to-verified latency
- pass@1 / pass@2

初期目標:

- run start rate 95%以上
- verified completion rate 80%以上
- handoff-to-start 45分以内
- blocker age 3日以内
- 同一 TODO の無変更転記 0件

## 最初に着手する順序

1. XGuard の停滞 run を再開し、rebase / verify / push を完了または明確な blocker にする。
2. `company/automation/runs/` の最小 schema と XGuard run manifest を作る。
3. Midday automation prompt を manifest 駆動へ変更する。
4. Morning / Evening automation に watchdog と close 条件を追加する。
5. `Projects/` を `active source`、`archive`、`generated output` に分類し、Git 管理方針を決める。

## 今回変更しないもの

- active automation のスケジュール
- XGuard production code
- 未追跡の `Projects/`、`.obsidian/`、`output/playwright/`
- live credentials と Supabase 環境
