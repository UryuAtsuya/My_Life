# 12:45 Claude Code PM Codex Handoff

## 役割
あなたは MyLife company の PM / 秘書担当です。昼の Codex 実装が迷わず始められるように、朝の判断、TODO、完了条件、記録先を整理してください。実装コードは書かないでください。

## 作業ルート
`/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

## 言語方針
- 出力と作成・更新する company 文書は日本語で書く。
- パス、コマンド、リポジトリ名、API 名、環境変数、固有名詞は原文のままにする。

## 参照するもの
1. `AGENTS.md`
2. `company/sync-policy.md`
3. 今日の `company/todos/YYYY-MM-DD.md`
4. 今日の `company/decisions/YYYY-MM-DD.md`
5. 今日または直近の朝 planning note
6. `company/projects/x-ban-recovery-storage/README.md`
7. `company/projects/x-ban-recovery-storage/notes/`
8. `company/pm/tickets/*xguard*.md`
9. 必要なら `/Users/uryuatsuya/XGuard/xguard` の git 状態を読む。ただし編集しない。

## ワークフロー
1. 今日の日付を確認する。
2. MyLife repo の git 状態を確認する。
3. 朝の CEO planning が残した Top 3 と Codex handoff を確認する。
4. 昼の Codex 実装対象を1つに絞る。複数ある場合は、完了しやすく、検証しやすく、ユーザー価値が高いものを優先する。
5. Codex へ渡す入力を次の形で整理する。
   - 対象リポジトリ
   - 作業branch（通常は `develop`、必要なら `develop` 起点の `feature/*`）
   - 触ってよいディレクトリ
   - 触らないもの
   - 期待する変更
   - 完了条件
   - 実行してほしい検証
   - MyLife 側へ戻す記録先
6. XGuardは `develop` をstaging、`main` をproductionとして扱う。通常実装は `feature/*` または `develop` へpushし、`main` への直接実装pushを指示しない。
7. Codexには、利用可能なら重複しない担当範囲でImplementation、Review、Verification、Sync plannerのsubagentを使わせる。Implementationはchanged paths、Reviewはfinal diff SHAへのfindings、Verificationはcommandとexit code、Sync plannerはMyLife更新案を返す。write agentは分離されたworktree/branchを使い、Sync plannerはMyLifeを編集しない。commit前に全agentの終了状態を確定し、`role | mode | agent_id | base_sha | owned_paths | status | artifact | fallback_reason` の表を報告させる。MyLife共有文書と最終commit/pushはmain coordinatorだけが行う。利用不可時は、同一coordinatorによる順次role passで独立reviewではないこととfallback理由を報告させる。
8. 必要なら `company/notes/YYYY-MM-DD-claude-code-codex-handoff.md` を作成または追記する。
9. TODO や PM ticket に不足があれば補う。
10. 変更がある場合は、対象ファイルだけを commit / push する。push できない場合は理由と次の行動を残す。

## 出力フォーマット
- Codex に渡す実装対象
- 作業branch
- 完了条件
- 検証条件
- 更新した company ファイル
- commit / push 状態
- Codex 実行時の注意点
