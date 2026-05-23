---
created: "2026-05-23"
project: "x-ban-recovery-storage"
assignee: "codex"
priority: high
status: open
---

# X BAN Recovery Storage の要件定義と環境整理

## 内容

XアカウントがBANまたは凍結された人向けに、平常時のXデータをDBへ保管し、BAN後に新アカウントで素早く再起動できるサービスを新規プロジェクトとして立ち上げる。

## 完了条件

- [x] 新規プロジェクトディレクトリを作成する
- [x] 要件定義、環境案、データ要件、復元フローをmdに保存する
- [x] 既存のweb-service優先順位を更新し、この開発・運用を最優先にする
- [ ] X APIの取得可能データ、料金、規約リスクを調査する
- [ ] Supabase前提のv0 DBスキーマを作る
- [ ] HP/LP制作前に、表現を「BAN復活」ではなく「BAN後の再起動支援」に固定する
- [ ] 最小プロトタイプの技術構成を確定する

## 判断ルール

- BANされたアカウントの自動復活を約束しない。
- 自動DM、一括フォロー、規約回避に見える機能は後回しにし、まずはバックアップ、検知、証明ページに絞る。
- 実装より先に、X APIの取得可能範囲と規約リスクを確認する。
- note/Short/Today Boardより、このサービス開発・運用をwebサービス側の最優先にする。

## 次の最小タスク

1. X APIで取得できる投稿、プロフィール、フォロワー/フォロー中、メディア、アカウント状態を調査する。
2. `x_accounts`、`tweet_snapshots`、`profile_snapshots`、`account_health_checks`、`recovery_sessions` のDB設計を作る。
3. LPのファーストビュー文言案を3つ作る。
