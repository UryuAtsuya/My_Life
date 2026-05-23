---
created: "2026-05-23"
project: "x-ban-recovery-storage"
assignee: "codex"
priority: high
status: active
---

# X BAN Recovery Storage の要件定義と環境整理

## 内容

XアカウントがBANまたは凍結された人向けに、平常時のXデータをDBへ保管し、BAN後に新アカウントで素早く再起動できるサービスを新規プロジェクトとして立ち上げる。

## 完了条件

- [x] 新規プロジェクトディレクトリを作成する
- [x] 要件定義、環境案、データ要件、復元フローをmdに保存する
- [x] 既存のweb-service優先順位を更新し、この開発・運用を最優先にする
- [x] XGuardのモノレポ開発想定を専用ディレクトリに分けて保存する
- [x] 朝調査・昼実装・夜コードレビューのautomationへ切り替える
- [ ] X APIの取得可能データ、料金、規約リスクを調査する
- [x] Supabase前提のv0 DBスキーマを作る
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

## 2026-05-23 XGuard monorepo assumption

- Saved: `company/projects/x-ban-recovery-storage/requirements/service-requirements.md`
- Saved: `company/projects/x-ban-recovery-storage/notes/2026-05-23-xguard-monorepo-assumption.md`
- Saved: `company/projects/x-ban-recovery-storage/technical/monorepo-plan.md`
- Saved: `company/projects/x-ban-recovery-storage/technical/shared-types-draft.md`
- Decision: まだ実装は開始せず、まずはX API規約、料金、取得可能データを確認する。

## 2026-05-23 automation update

- Morning: X BAN保護、X API、規約、料金、競合、市場シグナルを調査し、昼の実装スコープを決める。
- Midday: `/Users/uryuatsuya/XGuard/xguard` を別ローカルディレクトリとして作成または再利用し、Next.js + ExpressのXGuard実装を進める。
- Evening: XGuardのコードレビュー、修正案の洗い出し、小さな安全修正、翌日Top 3整理を行う。
- Note: MyLife Vaultは会社運用・計画の正本、XGuard実装コードは別ディレクトリで管理する。

## 2026-05-23 midday implementation update

- Attempted: `/Users/uryuatsuya/XGuard/xguard` の作成。
- Result: `mkdir: /Users/uryuatsuya/XGuard: Operation not permitted` のため、指定パスに実装モノレポを作成できなかった。
- Decision: 実装コードをMyLife Vault内へ迂回配置しない。Vaultは計画・PM・判断ログの正本に留める。
- Completed: `company/projects/x-ban-recovery-storage/technical/supabase-v0-schema.sql` にv0 DBスキーマを保存した。
- Safety: 自動DM送信、一括フォロー、BAN回避に見える処理は含めず、通知は `manual_notification_queue` の手動レビュー前提にした。

## 次の最小タスク - 更新

1. `/Users/uryuatsuya/XGuard/xguard` への書き込み権限または作業ルートを解決する。
2. 解決後、`frontend/`, `backend/`, `shared/`, `docs/` を作り、`shared/types.ts` と `docs/ARCHITECTURE.md` から着手する。
3. X APIの取得可能データ、料金、規約リスクを調査し、`supabase-v0-schema.sql` の保存範囲を絞り直す。
