---
created: "2026-08-27"
topic: "AI開発ツールの役割分担"
type: engineering-policy
status: active
tags:
  - company/engineering
  - ai-development
  - tooling
source: "ChatGPT会話『Superpowersとは何か』（2026-08-27）"
---

# AI開発ツールの役割分担

## 概要

2026年8月27日のChatGPT会話を起点に、AI開発で使うプロセス、最新仕様、コード理解、ブラウザ検証、LLM評価、運用監視の役割を整理する。

この文書は、すべての候補を一度に導入する計画ではない。
MyLifeの既存方針を正本に保ち、不足が確認できた層だけにツールを追加するための選定基準である。

> [!warning] 情報の確度
> 元会話はツール選定の二次情報であり、各製品の最新版、ライセンス、料金、対応環境、セキュリティ要件はこの取り込みでは再検証していない。
> 導入時は公式情報をContext7または対象の公式リポジトリで確認する。
> MyLifeは公開リポジトリのため、private ChatGPT会話のURLは記録しない。

## 設計と方針

役割が重複するツールは併用を前提にしない。
既存の仕組みで完了条件を満たせない場合に限り、候補を一つずつ試す。

| 層 | MyLifeでの扱い | 判断 |
|---|---|---|
| 開発プロセス | [[2026-06-22-loop-engineering-policy\|Loop Engineering Policy]] | 現行の正本を継続する。Superpowersは置き換え候補ではなく、30分以上の実装で差分を測る試行候補とする |
| 最新仕様 | Context7 | ライブラリ、SDK、API、CLIの確認に継続利用する |
| コード探索 | `rg`と既存の言語ツール | まず現行手段を使う。Serenaは大規模リポジトリで参照関係の追跡がボトルネックになった場合だけ評価する |
| ブラウザ検証 | Playwright CLIまたは導入済みブラウザSkill | 画面変更後の主要フロー、レスポンシブ表示、コンソールエラーを確認する |
| LLMリリース前評価 | Promptfoo | AI出力の品質またはプロンプトインジェクション耐性をCIで比較する段階で評価する |
| LLM本番監視 | Langfuse | 実利用者のトレース、コスト、遅延、評価結果を継続観測する必要が生じた段階で評価する |
| パーソナルAI基盤 | OpenClaw、Hermes Agent | Jarvis系の構想で比較対象にする。OpenClawはデバイス連携、Hermes Agentは長期記憶とクラウド常駐の仮説として扱い、採用は別の技術調査で決める |

## 適用基準

次のいずれかに当てはまる作業は、設計、実装、レビュー、検証を分離した開発loopで扱う。

- 30分以上を見込む機能追加または不具合調査
- 複数ファイル、API、DB、認証、決済をまたぐ変更
- productionへの影響または外部公開リスクがある変更
- AIに長時間の自律実行を任せる変更

文言修正、リンク差し替え、明確な一行修正では、重い設計承認を必須にしない。
ただし、対象差分の確認と最小の検証は省略しない。

## 導入順

1. MyLifeのLoop Engineering、Context7、ブラウザ検証を標準経路として使う。
2. Superpowersは非productionの1リポジトリ、1Issueで試し、現行運用との差分を測る。
3. コード探索に実測上の問題がある場合だけSerenaを試す。
4. AI機能を公開する前にPromptfooの必要性を判断する。
5. 実利用のトレースが必要になった時点でLangfuseを判断する。
6. Jarvis系の実装に入る前にOpenClawとHermes Agentの適合性を別資料で比較する。

Superpowers、Spec Kit、OpenSpecのように仕様作成と承認手順が重なる仕組みは、同じリポジトリへ同時導入しない。
導入する場合は、どの文書が正本か、どの承認ゲートを残すかを先に決める。

## 現在の判断

### 運用中

- MyLifeの開発プロセスは[[2026-06-22-loop-engineering-policy|Loop Engineering Policy]]を正本とする。
- ライブラリ、フレームワーク、SDK、API、CLIの最新仕様はContext7で確認する。
- UI変更は対象に応じてPlaywrightまたはブラウザSkillで検証する。

### 評価候補

- Superpowers
- Serena
- Promptfoo
- Langfuse
- OpenClaw
- Hermes Agent

### 未確認

- 各候補の現行バージョン、ライセンス、料金、導入手順
- MyLifeで使うCodexおよびClaude Codeとの最新互換性
- 各リポジトリでのインストール状態
- 外部接続、ログ保存、権限管理に伴うセキュリティ要件

## 次の一手

Superpowersを導入する前に、既存のLoop Engineeringとの差分を、要件整理、計画、TDD、レビュー、完了確認の5項目で比較する。
重複しない利点が見つかった場合だけ、非productionの1Issueで試行する。

## 参考

- ChatGPT会話「Superpowersとは何か」（2026年8月27日）
- [[2026-06-22-loop-engineering-policy|Loop Engineering Policy]]
- [[2026-06-26-agent-instruction-map|Agent Instruction 分割ルール]]
