---
date: "2026-05-23"
type: evening-xguard-code-review
project: "xguard"
status: reviewed-with-blockers
---

# 2026-05-23 Evening XGuard Code Review

## completed

- システム日付を `2026-05-23 18:41:08 JST` と確認した。
- `/Users/uryuatsuya/XGuard/xguard` を確認した。ディレクトリは存在するが、中身は空で、git repoではない。
- 今日の実装レビュー対象を、MyLife側のXGuard計画・DBスキーマ・型ドラフト・技術計画・PMチケットに限定した。
- `company/projects/x-ban-recovery-storage/technical/supabase-v0-schema.sql` のv0 DB設計をレビューした。
- `company/projects/x-ban-recovery-storage/technical/monorepo-plan.md` と `shared-types-draft.md` の実装順・型整合性をレビューした。

## unfinished

- `/Users/uryuatsuya/XGuard/xguard` には実装コードがないため、Next.js / Express / shared package のコードレビューは未実施。
- XGuard実装リポジトリはgit管理されていないため、XGuard側の差分確認、commit、pushは未実施。
- X APIの取得可能データ、料金、規約リスクは未調査のまま。明日のP0として継続する。
- 指定実装パスへの書き込み権限または作業ルートは未解決。

## findings

### P0: X OAuthトークン保管設計が未定義

- 対象: `supabase-v0-schema.sql`, `monorepo-plan.md`
- 問題: X APIで日次バックアップとBAN候補検知を行うには、OAuth token、refresh token、期限、scope、失効理由の保存・更新設計が必要だが、現スキーマに存在しない。
- リスク: 実装時に場当たり的にトークンをDBや環境変数へ置くと、漏洩時の影響が大きく、ユーザー別バックアップも成立しない。
- 修正案: `x_oauth_connections` を別テーブルにし、tokenはSupabase VaultまたはKMS相当で暗号化する。平文tokenをフロントへ返さないRLS/サービス境界を明文化する。

### P0: X API規約・料金・取得範囲が未確認

- 対象: `README.md`, `service-requirements.md`, `supabase-v0-schema.sql`
- 問題: 投稿本文、メディアURL、raw payload、フォロワー/フォロー中候補、証明ページ公開の扱いが、X APIのプラン・利用条件・再配布制限に依存している。
- リスク: DBスキーマやLP訴求を先に固定すると、実際には保存・公開できないデータをサービス価値として約束する可能性がある。
- 修正案: 明日は実装前に、v0で扱うデータを `取得できる / 保存できる / 公開できる / 要削除対応` に分ける。

### P1: tweet snapshotの一意制約とアーキテクチャ記述が矛盾

- 対象: `supabase-v0-schema.sql`, `company/engineering/docs/x-ban-recovery-storage-architecture.md`
- 問題: architectureは「同じ投稿IDはupsertし、反応数や取得時刻をスナップショットとして残す」と書いている。一方でSQLは `unique (x_account_id, tweet_id, captured_at)` のため、実行ごとにほぼ別行になり、tweet単位upsertとは整合しない。
- リスク: 実装時に「最新1行を更新する」のか「時系列履歴を積む」のかが曖昧になり、APIや証明ページの集計がぶれる。
- 修正案: `tweet_snapshots` は時系列履歴として扱い、重複防止に `captured_date date` を追加して `unique (x_account_id, tweet_id, captured_date)` にする。最新状態が必要なら別途 `tweets_current` を作る。

### P1: 証明ページの公開制御が不足

- 対象: `recovery_sessions`, `proof_payload`
- 問題: `proof_page_slug` と `proof_payload` はあるが、公開/非公開、公開開始、取り下げ、閲覧用slug再生成、個人情報マスキング範囲が定義されていない。
- リスク: 第三者情報や不要なraw payloadを証明ページに出しすぎる可能性がある。
- 修正案: `proof_pages` または `recovery_sessions` に `visibility`, `published_at`, `revoked_at`, `redaction_policy_version` を追加する。公開JSONはraw payloadから直接作らず、公開用DTOを生成する。

### P1: Stripe webhookの冪等性設計が未記載

- 対象: `monorepo-plan.md`, `user_profiles`
- 問題: Checkoutとwebhookは計画にあるが、イベントID保存、署名検証、重複処理、購読状態の更新順序が未定義。
- リスク: webhook再送や順不同配送で購読状態が誤更新される。
- 修正案: `stripe_events` テーブルを追加し、`event_id` unique、受信時刻、処理状態、処理エラーを記録する。

### P2: 手動通知キューの状態管理が弱い

- 対象: `manual_notification_queue`
- 問題: `review_status` が自由文字列で、送信禁止、却下、承認、送信済み、失敗などの状態が固定されていない。
- リスク: 将来自動化やUI表示を足した時に、誤送信や二重送信のガードが弱くなる。
- 修正案: enumまたはcheck constraintで `pending`, `approved`, `rejected`, `sent`, `failed` を定義する。

## fixes applied

- 実装コードへの修正はなし。対象リポジトリにコードが存在しないため。
- MyLife側にこの夜レビュー記録、明日TODO、PMチケット追記、プロジェクトレビューnoteを追加する。

## proposed fixes

1. X API規約・料金・取得可能範囲を先に調査し、v0データ範囲を縮小または確定する。
2. OAuth token保存・更新・失効・削除のスキーマとセキュリティ境界を作る。
3. `tweet_snapshots` を時系列履歴にするか最新状態にするか決め、unique制約を直す。
4. 証明ページの公開制御、取り下げ、マスキング方針をスキーマに入れる。
5. Stripe webhook冪等性テーブルを追加する。

## verification

| コマンド | 結果 |
|---|---|
| `date '+%Y-%m-%d %H:%M:%S %Z (%z)'` | `2026-05-23 18:41:08 JST (+0900)` |
| `git status --short --branch` in MyLife | `main...origin/main`、未追跡の `.obsidian/`, `Ideas/`, `Projects/`, `memo/` などのみ |
| `find /Users/uryuatsuya/XGuard/xguard -maxdepth 1 -mindepth 1 -print \| wc -l` | `0`。XGuard実装ディレクトリは空 |
| `git -C /Users/uryuatsuya/XGuard/xguard status --short --branch` | `fatal: not a git repository` |
| `git diff --check` in MyLife | エラーなし |
| `git -C /Users/uryuatsuya/XGuard/xguard diff --check` | git repoではないため未実施 |
| Next.js / Express build, lint, test | 実装コードがないため未実施 |

## tomorrow handoff

1. X APIの取得可能データ、料金、規約リスクを調査し、v0で扱うデータを `取得 / 保存 / 公開 / 削除対応` に分類する。
2. `/Users/uryuatsuya/XGuard/xguard` の書き込み権限または代替の実装作業ルートを解決する。
3. 実装前に、OAuth token保管、証明ページ公開制御、tweet snapshot方針、Stripe webhook冪等性をDB設計へ反映する。
