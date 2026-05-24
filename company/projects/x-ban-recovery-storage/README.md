---
created: "2026-05-23"
project: "xguard"
status: planning
priority: highest
tags: [x, sns, backup, recovery, supabase, web-service]
---

# XGuard

## 目的

XアカウントがBANまたは凍結された人向けに、平常時から投稿、プロフィール、フォロワー/フォロー中の履歴、メディア、活動実績をDBへ保管し、BAN後に新アカウントで素早く再起動できる状態を作る。

## ディレクトリ構成

| パス | 用途 |
|---|---|
| `requirements/` | サービス要件、機能要件、収益モデル |
| `notes/` | ユーザーからの想定、メモ、判断ログ |
| `technical/` | 技術スタック、モノレポ構成、開発手順 |

## 現在の開発想定

- サービス名: `XGuard`
- 想定価格: 月額3,000円
- 実装方針: Next.js 14 + Node.js Express + Supabase + Stripe + X API
- リポジトリ案: `xguard/` モノレポ
- デプロイ想定: フロントVercel、バックエンドRailway
- 現段階: 実装前の要件定義・技術メモ整理

## 重要な前提

- このサービスは、BANされたXアカウントを外部から復活させるものではない。
- 「復元」は、保存済みデータを使って本人性、活動実績、移行先を示し、新アカウントで再起動しやすくすることを意味する。
- Xの規約、API制限、スパム防止、個人情報保護を前提に設計する。
- フォロワー通知や一括フォローは、API制限と規約上の可否を調査してから実装判断する。

## 対象ユーザー

- X依存度が高い個人事業者、クリエイター、インフルエンサー、コミュニティ運営者。
- X上の投稿履歴、信頼、フォロワー導線を失うことが事業リスクになる人。
- 日常的なバックアップや移行準備を自分で管理する時間がない人。

## 解決する痛み

- BAN後に過去投稿、プロフィール、活動実績を証明できない。
- 新アカウントを作っても、同一人物であることを伝える証拠ページがない。
- フォロー中リスト、投稿素材、メディア、プロフィール履歴が散らばっている。
- BANが起きてから手作業で復旧導線を作ると遅い。

## コア価値

1. 平常時にXデータを自動保管する。
2. BAN/凍結の兆候またはAPIエラーを検知して通知する。
3. 新アカウント再起動用の証明ページと告知文を生成する。
4. バックアップ対象を新アカウントへ切り替える。

## v0スコープ

### 作る

- ユーザー登録とXアカウント接続。
- 毎日1回の投稿、プロフィール、メトリクスのバックアップ。
- BAN/凍結らしきAPIエラーの検知とメール通知。
- 証明ページ用JSONの生成。
- 復元モードの要件定義と画面ワイヤー。

### まだ作らない

- 自動DM送信。
- 無制限の一括フォロー。
- BAN回避や規約違反を助長する自動運用。
- 認証情報を平文保存する仕組み。
- 複数SNS対応。

## 主要機能要件

| 機能 | 内容 | 優先度 |
|---|---|---|
| データバックアップ | X APIから投稿、プロフィール、メディアURL、フォロワー数推移を取得してDBへ保存 | P0 |
| BAN検知 | アカウント取得時の404/403/認証失敗を分類し、BAN候補として記録 | P0 |
| メール通知 | BAN候補検知時にユーザーへ通知 | P0 |
| 証明ページ生成 | 保存済みデータから公開可能な証明ページJSONを生成 | P0 |
| 復元モード | 新アカウントURL、告知文、証明ページURLをまとめて表示 | P1 |
| フォロワー通知キュー | DM文と送信候補をキュー化。ただし自動送信は規約調査後 | P2 |
| フォロー中リスト移行 | 保存済みフォロー中リストから新アカウントでの再フォロー候補を表示 | P2 |

## データ要件

| データ | 保存目的 | 注意 |
|---|---|---|
| ツイート本文、日時、ID、反応数 | 証明ページ、活動履歴、再投稿素材 | API利用範囲と保存期間を確認 |
| プロフィール履歴 | 同一人物証明、変更履歴 | アイコン画像の扱いに注意 |
| フォロワー数推移 | 活動実績グラフ | 個別フォロワー保存は規約確認 |
| フォロー中リスト | 新アカウント再構築候補 | 自動フォローはレート制限必須 |
| メディアURL/ファイル | 証明ページ表示、再利用素材 | 再配布権利と保存容量に注意 |
| BAN検知ログ | 通知、復旧導線、監査 | 誤検知とAPI障害を区別 |

## 復元フロー

1. 平常時に毎日バックアップを実行する。
2. 毎時のヘルスチェックでBAN候補を検知する。
3. BAN候補をDBに記録し、ユーザーへメール通知する。
4. ユーザーがダッシュボードで復元モードを開始する。
5. 証明ページ、告知文、新アカウント固定投稿案を生成する。
6. ユーザーが新アカウントを作成し、手動確認後にバックアップ対象を切り替える。

## 環境案

| 領域 | 候補 |
|---|---|
| フロント | Next.js |
| API/バックエンド | Next.js API Routes または Node.js worker |
| DB | Supabase Postgres |
| 認証 | Supabase Auth |
| ジョブ | Supabase Edge Functions / cron / GitHub Actions / dedicated scheduler |
| メール | Resend または nodemailer + SMTP |
| ホスティング | Vercel |
| 監視 | Supabase logs + Vercel logs |
| 決済 | Stripe |

## 必要な環境変数

```env
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
X_CLIENT_ID=
X_CLIENT_SECRET=
X_CALLBACK_URL=
MAIL_FROM=
SMTP_HOST=
SMTP_PORT=
SMTP_USER=
SMTP_PASS=
APP_BASE_URL=
TEST_MODE=true
```

## 初期DBテーブル案

- `users`
- `x_accounts`
- `tweet_snapshots`
- `profile_snapshots`
- `follower_count_snapshots`
- `following_snapshots`
- `media_snapshots`
- `account_health_checks`
- `recovery_sessions`
- `dm_queue`

## 技術リスク

- X APIの有料プラン、取得上限、保存可能範囲が事業性に直結する。
- フォロワーリストやDM送信は規約、API権限、スパム判定のリスクが高い。
- BAN判定はAPI障害、認証切れ、鍵の失効と区別する必要がある。
- 証明ページで個人情報や第三者情報を公開しすぎない設計が必要。

## 最初の検証項目

1. X APIでv0に必要なデータを取得できるか。
2. Supabaseに1日1回のスナップショット保存が現実的なコストか。
3. BAN検知を404/403だけで判定してよいか、認証切れとどう分けるか。
4. 証明ページに載せてよいデータ範囲を決める。
5. HP/LPで訴求する言葉を「自動復元」ではなく「再起動支援」「証明ページ生成」に寄せる。

## 次アクション

1. Developer ConsoleでX APIのendpoint別単価を確認し、v0の月次原価を見積もる。
2. `/Users/uryuatsuya/XGuard/xguard` をgit repoとして初期化し、まず `docs/X_API_SCOPE.md` とDB schema v1 draftを作る。
3. HP制作前に、LPの約束を「BAN復活」ではなく「BAN後の再起動支援」「証明ページ生成」に固定する。
4. OAuth token保管、proof DTO、compliance delete queue、backup jobの最小設計を書く。

## 2026-05-23 midday implementation update

- v0 DBスキーマを `technical/supabase-v0-schema.sql` に追加した。
- `/Users/uryuatsuya/XGuard/xguard` の作成は `Operation not permitted` で失敗した。
- 実装コードはMyLife Vaultへ迂回せず、指定のVault外ワークスペース権限を解決してから作る。
- 通知機能は自動DMではなく、手動レビュー用の `manual_notification_queue` として扱う。

## 2026-05-23 development element scan

- 初期調査: `research/2026-05-23-x-api-development-elements.md`
- 実装前ゲート: `technical/pre-implementation-gate.md`
- XGuard repo初期docs: `/Users/uryuatsuya/XGuard/xguard/docs/X_API_SCOPE.md`, `/Users/uryuatsuya/XGuard/xguard/docs/IMPLEMENTATION_GATE.md`
- v0はread-only OAuth接続、投稿/プロフィール取得、proof用DTO生成、compliance delete queueを優先する。
- 自動DM、自動follow/unfollow、raw payload公開、BAN回避に見える機能はv0から外す。
- X API価格はPay-per-use前提。endpoint別の実単価はDeveloper Consoleで確認してから月額3,000円の原価を判断する。

## 2026-05-24 midday implementation update

- XGuard repoは `/Users/uryuatsuya/XGuard/xguard` に存在し、`README.md`, `docs/X_API_SCOPE.md`, `docs/IMPLEMENTATION_GATE.md` がある。
- ただしCodex実行環境からは書き込み不可。`test -w /Users/uryuatsuya/XGuard/xguard` は `not_writable`、`supabase/` と `shared/` の作成は `Operation not permitted`。
- 実装コードはVault内へ迂回しない。代わりに適用用ドラフトとして `technical/supabase-v1-schema-draft.sql` と `technical/shared-types-v1-draft.md` を保存した。
- 次はXGuard repoの書き込み権限を解決し、ドラフトを `/Users/uryuatsuya/XGuard/xguard/supabase/schema.sql` と `/Users/uryuatsuya/XGuard/xguard/shared/types.ts` へ配置する。
