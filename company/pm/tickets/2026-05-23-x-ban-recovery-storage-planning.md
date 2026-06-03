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

## 2026-05-23 evening code review update

- Reviewed: `company/projects/x-ban-recovery-storage/technical/supabase-v0-schema.sql`
- Reviewed: `company/projects/x-ban-recovery-storage/technical/monorepo-plan.md`
- Reviewed: `company/projects/x-ban-recovery-storage/technical/shared-types-draft.md`
- Reviewed: `/Users/uryuatsuya/XGuard/xguard`
- Result: XGuard実装ディレクトリは空で、git repoではない。コードレビュー対象はMyLife側の設計ドキュメントに限定した。
- P0: X OAuth tokenの保管・更新・失効設計が未定義。
- P0: X APIの取得可能データ、料金、保存・再公開可否、規約リスクが未確認。
- P1: `tweet_snapshots` の一意制約が、時系列snapshotとtweet単位upsertのどちらを採るか曖昧。
- P1: 証明ページの公開/非公開、取り下げ、redaction方針が未定義。
- P1: Stripe webhookの冪等性テーブルが未設計。
- Next: 明日は実装初期化より先に、X APIデータ範囲表とOAuth token保管設計を作る。

## 2026-05-23 development element scan

- Saved: `company/projects/x-ban-recovery-storage/research/2026-05-23-x-api-development-elements.md`
- Saved: `company/projects/x-ban-recovery-storage/technical/pre-implementation-gate.md`
- Finding: X APIはPay-per-use前提で、rate limitとbillingは別。月額3,000円モデルは、ユーザー単位のAPI消費見積もりなしに進めない。
- Finding: OAuth 2.0 PKCE + refresh token前提で、`x_oauth_connections` と暗号化token保管が必要。
- Finding: v0はread-only scopeに寄せる。`tweet.write`, `follows.write`, DM write系scopeは使わない。
- Finding: 証明ページはraw payloadを直接公開しない。公開用DTOとredaction方針を先に作る。
- Done: `/Users/uryuatsuya/XGuard/xguard` をgit repo化し、`README.md`, `docs/X_API_SCOPE.md`, `docs/IMPLEMENTATION_GATE.md` を作成した。
- Next: Supabase schema v1 draftでOAuth token保管、API使用量、proof page公開制御、compliance queue、Stripe webhook冪等性を追加する。

## 2026-05-24 morning research update

- Saved: `company/projects/x-ban-recovery-storage/requirements/2026-05-24-x-ban-research.md`
- Saved: `company/projects/x-ban-recovery-storage/notes/2026-05-24-morning-planning.md`
- Decision: XGuard v0はread-onlyの事前バックアップと証明ページ生成に限定する。
- Decision: 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線はv0から外す。
- Finding: X APIはPay-per-use。Owned Readsは$0.001/resourceだが、followers/following/mediaまで広げると月額3,000円の原価管理が必要。
- Finding: X Contentの削除・変更・protected化・withheld・ユーザー削除要求に追従するcompliance queueが必須。
- Next: 昼は `/Users/uryuatsuya/XGuard/xguard` に `supabase/schema.sql`, `shared/types.ts`, `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` を作る。
- Verification: 朝runではproduction codeを実装しない。

## 2026-05-24 midday implementation update

- Checked: `/Users/uryuatsuya/XGuard/xguard` は既存Git repoで、最新ローカルcommitは `606eb77 Initialize XGuard docs`。
- Checked: 既存ファイルは `README.md`, `docs/X_API_SCOPE.md`, `docs/IMPLEMENTATION_GATE.md`。
- Blocked: Codex実行環境からは `test -w /Users/uryuatsuya/XGuard/xguard` が `not_writable`。`mkdir -p /Users/uryuatsuya/XGuard/xguard/supabase` と `mkdir -p /Users/uryuatsuya/XGuard/xguard/shared` は `Operation not permitted`。
- Decision: 実装コードをMyLife Vault内へ迂回配置しない。Vault側には適用用ドラフトと実績ログだけを残す。
- Completed: `company/projects/x-ban-recovery-storage/technical/supabase-v1-schema-draft.sql` を作成し、OAuth token暗号化保管、API使用量、backup run、proof page公開制御、content compliance、Stripe webhook冪等性を入れた。
- Completed: `company/projects/x-ban-recovery-storage/technical/shared-types-v1-draft.md` を作成し、`ProofPublicPayload`、`BackupRunStatus`、`ProofPageVisibility`、`ContentComplianceEventType`、`ApiUsageEvent` を入れた。
- Not completed: XGuard repo内の `supabase/schema.sql`, `shared/types.ts`, `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` 作成。
- Next: XGuard workspaceを書き込み可能にしてから、v1 draftを実repoへ適用し、`git diff --check` とTypeScript検証を走らせる。

## 2026-05-24 evening code review update

- Reviewed: `/Users/uryuatsuya/XGuard/xguard` backend-first prototype.
- Completed: XGuard repoへ `supabase/schema.sql`, `shared/types.ts`, backend mock API, `docs/API_SPEC.md` が作成済み。
- Fixed: v0初期OAuth scopeから `follows.read` を外し、`tweet.read`, `users.read`, `offline.access` に絞った。
- Fixed: mock backup run stateをmodule globalからapp instance内へ移した。
- Fixed: supertest listen依存を避け、no-listenで通るroute境界/サービス境界テストへ寄せた。
- Verification: `git diff --check` pass, `npx tsc -p tsconfig.json --noEmit` pass, `npx vitest run --configLoader runner` pass 2 files / 3 tests.
- Blocked: `npm run check` はこのサンドボックスでは `dist/` emitが `EPERM`。`npm audit` は `registry.npmjs.org` DNS解決不可。
- XGuard push: `ba98160 Document minimum OAuth scope` を `UryuAtsuya/Xguard` `origin/main` へpush済み。
- Not completed: `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md`, Developer Console実画面確認、Supabase repository実装、Stripe webhook handler。
- Next: 2026-05-25はdocs gate、build設定、Supabase repository層の順に進める。

## 2026-05-25 midday implementation update

- Checked: `/Users/uryuatsuya/XGuard/xguard` は読み取り可能だが、現在のCodexサンドボックスからは書き込み不可。`mkdir .codex-write-test` は `Operation not permitted`。
- Decision: 実装コードをMyLife Vaultへ迂回配置しない。今回は `/private/tmp/xguard-midday-2026-05-25` の一時cloneで実装し、GitHubへpushした。
- Completed: `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` をXGuard repoへ追加。
- Completed: `tsconfig.build.json` と `package.json` 更新でbuild/testを分離し、`npm run check` を通した。
- Completed: `TokenRepository` に `auth_expired` 遷移とtoken削除導線を追加し、`SupabaseTokenRepository` contractを追加。
- Completed: token repository境界テストを追加。token ref保存、`auth_expired`、revoked row read除外を確認。
- Verification: `npm run check` pass。3 files / 5 tests passed。`git diff --check` と `git diff --cached --check` pass。
- XGuard push: `b3bd37c Add token repository contract and docs gates` を `UryuAtsuya/Xguard` `origin/main` へpush済み。
- Not completed: Developer Console実画面確認、Stripe webhook handler、`backup_runs` + `api_usage_events` transaction service、指定パス `/Users/uryuatsuya/XGuard/xguard` のローカル同期。
- Next: 夜レビューで `b3bd37c` をレビューし、指定パスを同期できる状態なら同パスで `npm run check` を再実行する。

## 2026-06-03 evening review update

- Reviewed: `/Users/uryuatsuya/XGuard/xguard` at `HEAD=origin/main=03ecd2f Default OAuth status diagnostic to disabled`。
- Status: activeのまま。既定では `/api/x/oauth/status` が404へ倒れるため、昼のproduction status公開blockerは解消。
- Decision: 昼の一時commit `9e8b7c5 Guard OAuth status diagnostic in production` は丸ごとpushしない。必要差分だけ `03ecd2f` の上で扱う。
- P1: `X_OAUTH_STATUS_EXPOSURE=deployment_diagnostic` 有効時の診断endpointが無認証。header secret、admin auth、private health checkのいずれかで閉じる。
- P1: OAuth `state` / S256 PKCE / callback validationが未実装。
- Verification: `git diff --check`, `git diff --cached --check`, targeted Vitest, `tsc --noEmit`, `npm run test` pass。`build:api` / `build:web` は `dist/` 権限blocker。
- XGuard push: local差分なしのためpush対象なし。live remote確認はfetch/DNS/`.git/FETCH_HEAD` blockerで未完了。
- Next: 診断endpoint制限、実Supabase/Postgres integration test、OAuth PKCE/state、Developer Console原価確認をTop 3で進める。
