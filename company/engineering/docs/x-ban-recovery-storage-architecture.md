---
created: "2026-05-23"
project: "x-ban-recovery-storage"
status: planning
tags: [architecture, x-api, supabase, recovery]
---

# X BAN Recovery Storage Architecture

## 概要

Xアカウントの平常時データを定期保存し、BANまたは凍結後に新アカウントで再起動するための証明ページ、告知文、バックアップ切り替えを支援する。

## 設計・方針

- v0は「バックアップ」「BAN候補検知」「証明ページ生成」に絞る。
- 復元はアカウント復活ではなく、新アカウントへの再起動支援として扱う。
- X API、メール、DB、ジョブ実行を分離し、`TEST_MODE=true` で外部副作用を止められるようにする。
- DM送信や一括フォローは規約とAPI制限の確認が終わるまで実装対象外にする。

## 詳細

### バックアップジョブ

- 毎日1回、接続済みXアカウントのプロフィール、投稿、メディア、フォロワー数、フォロー中リストを保存する。
- 取得できないデータはエラーとして記録し、ジョブ全体を落とさない。
- 同じ投稿IDはupsertし、反応数や取得時刻をスナップショットとして残す。

### BAN候補検知

- 毎時、X APIでアカウント情報を取得する。
- 404/403、認証失敗、レート制限、API障害を分類して `account_health_checks` に保存する。
- BAN候補は複数回連続失敗、またはAPIレスポンス分類で判定する。
- BAN候補になったら `x_accounts.banned_at` ではなく、まず `suspected_banned_at` を記録する。

### 証明ページ生成

- `recovery_sessions` を作成し、公開可能なプロフィール履歴、投稿最新100件、フォロワー数推移、活動統計をJSONで返す。
- 証明ページには第三者の個人情報を直接出しすぎない。
- 公開URLは `APP_BASE_URL/proof/:slug` を想定する。

### 復元モード

- ユーザーが新アカウントURLを登録する。
- 告知文、固定投稿文、プロフィール文の候補を生成する。
- 旧アカウントの保存データから、再フォロー候補と通知候補を表示する。
- 自動送信はv0ではしない。

### 初期モジュール案

- `src/xClient.js`: X APIクライアント
- `src/backup.js`: 定期バックアップ
- `src/recovery.js`: BAN候補検知、証明ページJSON、復元モード
- `src/mail.js`: 通知
- `src/scheduler.js`: ジョブ実行

### 初期関数案

- `detectBan(userId)`
- `generateProofPage(userId)`
- `buildFollowerNotificationQueue(userId, newAccountUrl)`
- `transferFollowingList(oldUserId, newApiCredentials)`

`buildFollowerNotificationQueue` と `transferFollowingList` は、v0では「候補生成」までに留める。
