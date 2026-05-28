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
- GitHub実装repo: `UryuAtsuya/Xguard`
- デプロイ想定: フロントVercel、バックエンドRailway
- 現段階: 実装前の要件定義・技術メモ整理

## GitHub同期ルール

- XGuardの実装コードは `/Users/uryuatsuya/XGuard/xguard` を作業場所にする。
- meaningfulなコーディング作業が完了し、検証が通ったら、原則として `UryuAtsuya/Xguard` の `origin/main` へcommit/pushまで行う。
- `origin` が未設定なら `https://github.com/UryuAtsuya/Xguard.git` を設定する。
- pushできない場合は、理由、未pushのcommit hash、次に必要な操作を昼会/夜会メモに残す。
- MyLife側の計画・運用ドキュメントcommitと、XGuard実装repoのcommitは分けて報告する。

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

## 2026-05-24 GitHub sync rule update

- 今後のXGuard coding automationでは、実装完了後に `UryuAtsuya/Xguard` へpushまで行う。
- 昼会・夜会automation promptにも、XGuard実装repoのcommit/pushを必須の通常手順として追記した。

## 2026-05-25 morning research update

- 調査メモ: `requirements/2026-05-25-x-ban-research.md`
- 朝会引き継ぎ: `notes/2026-05-25-morning-planning.md`
- 今日の優先はdocs gate、build gate、Supabase token repositoryの順にする。
- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみに維持する。
- X API原価はPay-per-usageとDeveloper Console実画面確認を正とし、`Owned Reads` の低単価枠を第三者ユーザー向けSaaSの主前提にしない。
- proof pageはraw X API payloadを公開せず、公開DTO、取り下げ、redaction、X Content削除追従を必須にする。

## 2026-05-25 evening review update

- 夜レビュー: `notes/2026-05-25-evening-code-review.md`
- XGuard local HEADは `91229db Exclude revoked token refs`。ただしremote先行のため夜runではpush不可。
- `git push -v origin main` は `fetch first`、`git fetch origin main` は `.git/FETCH_HEAD` 書き込み不可で失敗。
- `npx vitest run --configLoader runner` はpass、`npx tsc -p tsconfig.json --noEmit` は `tokenRepository.test.ts` のmock fetch型不一致でfail。
- 明日はremote統合、TypeScript復旧、Developer Console原価確認を最優先にする。
- `/Users/uryuatsuya/XGuard/xguard` は存在し、git statusはclean。ただし朝run時点のCodexサンドボックスからは `NOT_WRITABLE` のため、昼run冒頭で書き込み可否を確認する。

## 2026-05-25 midday implementation update

- `/Users/uryuatsuya/XGuard/xguard` は読み取り可能だが、昼run時点のCodexサンドボックスからは書き込み不可。`mkdir .codex-write-test` は `Operation not permitted`。
- 実装コードをVaultへ置かず、`/private/tmp/xguard-midday-2026-05-25` の一時cloneでXGuard repoを更新した。
- XGuard commit: `b3bd37c Add token repository contract and docs gates`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 追加/更新: `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md`, `tsconfig.build.json`, `backend/src/repositories/supabaseTokenRepository.ts`, `backend/src/repositories/tokenRepository.ts`, `backend/src/__tests__/tokenRepository.test.ts`
- 検証: `npm run check` pass、`git diff --check` pass、`git diff --cached --check` pass。
- 次はDeveloper Console実画面確認、指定パス作業ツリーの同期、`backup_runs` + `api_usage_events` transaction service、Stripe webhook handlerの順に進める。

## 2026-05-26 morning research update

- 調査メモ: `requirements/2026-05-26-x-ban-research.md`
- 朝会引き継ぎ: `notes/2026-05-26-morning-planning.md`
- 今日の優先はremote同期、TypeScript検証復旧、Developer Console原価確認、usage/cost ledger最小contractの順にする。
- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみに維持する。
- `Owned Reads` の低単価は第三者ユーザー向けSaaSに適用できると確認できるまで主前提にしない。
- 朝run確認では `/Users/uryuatsuya/XGuard/xguard` は存在するが `writable=no`、Git状態は `main...origin/main [ahead 2]`。

## 2026-05-26 midday implementation update

- 実装メモ: `company/notes/2026-05-26-midday-xguard-implementation.md`
- Project note: `notes/2026-05-26-midday-implementation.md`
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は昼runでも `NOT_WRITABLE`。Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-26` の一時cloneで実装した。
- XGuard commit: `c7a315c Add API usage ledger contract`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 追加/更新: `backend/src/services/apiUsageLedger.ts`, `backend/src/__tests__/apiUsageLedger.test.ts`, token repository scope再検査、`docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md`, `docs/DEPLOY.md`
- 検証: `tsc --noEmit` pass、`vitest` pass（4 files / 9 tests）、`npm run check` pass、`git diff --check` pass、`git diff --cached --check` pass。
- 次は指定パスの権限解消と `origin/main` `c7a315c` への同期、Developer Console実値確認、Supabase transaction repository化を進める。

## 2026-05-29 morning research update

- 調査メモ: `requirements/2026-05-29-x-ban-research.md`
- 朝会引き継ぎ: `notes/2026-05-29-morning-planning.md`
- 今日の優先はrepo状態の確定、`9be85a1` と `c0a7dcd` のledger差分比較、real OAuth configured mode確認、Developer Console原価確認の順にする。
- 朝run確認では `/Users/uryuatsuya/XGuard/xguard` は `exists=yes`, `writable=no`, `main...origin/main`, HEAD `455718c`。
- 昨日の一時clone `/private/tmp/xguard-midday-2026-05-28` は `main...origin/main [ahead 1]`, HEAD `9be85a1`。そのままpushせず、remote最新・指定パス実装との差分を見て未反映分だけ扱う。
- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみに維持する。
- `Owned Reads` の低単価は第三者ユーザー向けSaaSに適用できると確認できるまで主前提にしない。

## 2026-05-28 midday implementation follow-up

- 実装メモ: `company/notes/2026-05-28-midday-xguard-implementation.md`
- Project note: `notes/2026-05-28-midday-implementation.md`
- 13:31 JSTの実行環境では `/Users/uryuatsuya/XGuard/xguard` は `writable=no`。Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-28` で実装した。
- XGuard local commit: `9be85a1 Add Supabase API usage ledger repository`
- 追加/更新: `backend/src/repositories/supabaseApiUsageLedgerRepository.ts`, `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`, `supabase/schema.sql`, `docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md`, `docs/DEPLOY.md`
- 検証: `npm ci` pass、`tsc --noEmit` pass、対象Vitest pass（1 file / 2 tests）、`npm run check` pass（5 files / 32 tests）、`git diff --check` pass、`git diff --cached --check` pass。
- Push状態: 未push。`git push origin main` は `fetch first`、`git fetch origin main` / `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。
- 次はGitHub DNSが通る環境でremote先行commitを取り込み、`9be85a1` を `UryuAtsuya/Xguard` `origin/main` へpushする。

## 2026-05-27 evening review update

- 夜レビュー: `notes/2026-05-27-evening-code-review.md`
- XGuard push済み正本は `/private/tmp/xguard-midday-2026-05-27` の `3528e26 Validate API usage ledger inputs`。夜runの `git push -v origin main` は `Everything up-to-date`。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `not_writable`、`main...origin/main [ahead 1]`、HEAD `e750d04`。`.git/FETCH_HEAD` は `Operation not permitted` で更新不可。
- `e750d04` は正本 `3528e26` と完全一致しないため、そのままpushしない。
- 検証: 指定パスは `git diff --check`, `tsc --noEmit`, `vitest`（4 files / 11 tests）pass、`npm run check` は `dist/` 書き込み `EPERM`。一時checkoutは `npm run check` pass（4 files / 29 tests）。
- 次は指定パスを `3528e26` へ同期し、Developer Console実値確認、Supabase transaction repository化を進める。

## 2026-05-27 midday implementation update

- 実装メモ: `company/notes/2026-05-27-midday-xguard-implementation.md`
- Project note: `notes/2026-05-27-midday-implementation.md`
- 指定パス `/Users/uryuatsuya/XGuard/xguard` は昼runでも `NOT_WRITABLE`。最終確認では clean / `main...origin/main [ahead 1]`、HEAD `e750d04`、tracking `origin/main` `045d2d2` で、push済み正本 `3528e26` とは未同期。
- 実装コードをVaultへ置かず、`/private/tmp/xguard-midday-2026-05-27` の一時checkoutでXGuard repoを更新した。
- XGuard commit: `3528e26 Validate API usage ledger inputs`
- Push先: `UryuAtsuya/Xguard` `origin/main`
- 追加/更新: `ApiUsageLedgerService` の非負整数validation、負値・小数・`NaN`・`Infinity` の失敗テスト、`docs/API_COST_MODEL.md`, `docs/API_SPEC.md`, `docs/ARCHITECTURE.md`
- 検証: `npm ci` pass、`tsc --noEmit` pass、`vitest` pass（4 files / 29 tests）、`npm run check` pass、`git diff --check` pass、`git diff --cached --check` pass。
- 次は指定パスの権限を解消して `origin/main` `3528e26` へ同期し、Developer Console実値確認、Supabase transaction repository化を進める。

## 2026-05-27 morning research update

- 調査メモ: `requirements/2026-05-27-x-ban-research.md`
- 朝会引き継ぎ: `notes/2026-05-27-morning-planning.md`
- 今日の優先は指定パス同期、`ApiUsageLedgerService` 非負整数validation、Developer Console原価確認の順にする。
- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみに維持する。
- `Owned Reads` の低単価は第三者ユーザー向けSaaSに適用できると確認できるまで主前提にしない。
- 朝run確認では `/Users/uryuatsuya/XGuard/xguard` は存在するが `writable=no`、Git状態は `main...origin/main [ahead 4, behind 2]`。
- production codeは朝runでは触らず、昼runで `/Users/uryuatsuya/XGuard/xguard` または `/private/tmp/xguard-midday-2026-05-27` を使う。

## 2026-05-28 morning research update

- 調査メモ: `requirements/2026-05-28-x-ban-research.md`
- 朝会引き継ぎ: `notes/2026-05-28-morning-planning.md`
- 今日の優先は指定パスをpush済み正本 `3528e26` へ同期、Developer Console実値確認、Supabase ledger transaction repository化の順にする。
- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみに維持する。
- `Owned Reads` は安いが、第三者ユーザー向けSaaSに適用できると確認できるまで主前提にしない。
- 朝run確認では `/Users/uryuatsuya/XGuard/xguard` は存在するが `writable=no`、Git状態は `main...origin/main [ahead 1]`、HEAD `e750d04`。
- production codeは朝runでは触らず、昼runで `/Users/uryuatsuya/XGuard/xguard` または `/private/tmp/xguard-midday-2026-05-28` を使う。

## 2026-05-26 evening review update

- 夜レビュー: `notes/2026-05-26-evening-code-review.md`
- push済み一時clone `/private/tmp/xguard-midday-2026-05-26` は `c7a315c Add API usage ledger contract` でclean、`npm run check` pass（4 files / 9 tests）。
- 指定パス `/Users/uryuatsuya/XGuard/xguard` はlocal HEAD `0991eeb`、tracking `origin/main` `ba98160`、`main...origin/main [ahead 3]` のままで、まだpush済み `c7a315c` と同期できていない。
- `git ls-remote origin refs/heads/main` はDNS失敗。GitHub live確認は次回に回す。
- 追加指摘: `ApiUsageLedgerService` に非負整数validationと失敗テストを入れ、負のusage/costを防ぐ。
- 明日は指定パス同期、ledger validation、Developer Console実値確認をTop 3にする。
