---
created: "2026-05-24"
project: "xguard"
type: research
status: morning-scan
sources:
  - "https://docs.x.com/x-api/getting-started/pricing"
  - "https://docs.x.com/x-api/fundamentals/rate-limits"
  - "https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code"
  - "https://docs.x.com/developer-terms/policy"
  - "https://docs.x.com/developer-terms/restricted-use-cases"
  - "https://docs.x.com/developer-guidelines"
  - "https://help.x.com/en/rules-and-policies/authenticity"
  - "https://xportkit.com/"
  - "https://bestweet.com/"
  - "https://www.archivlyx.com/"
  - "https://www.unfollr.com/"
  - "https://piunikaweb.com/2026/03/14/x-users-report-wave-of-bans-for-inauthentic-behaviors/"
  - "https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia"
---

# 2026-05-24 XGuard 朝調査: X BAN保護・API・競合・市場シグナル

## 結論

XGuard v0は「BAN復活」ではなく、「本人が事前にOAuth許可したXデータをread-onlyで保存し、BAN後の再起動に使う証明ページDTOを生成する」サービスに固定する。

X APIはPay-per-useで、read系も取得リソース単位で課金される。Owned Readsは安いが、v0の月額3,000円モデルは、ユーザーごとの投稿取得件数、プロフィール取得頻度、followers/followingの扱いを制限しないと原価が読めない。昼はコード本体に広げず、Supabase schema v1とread-only境界の実装準備だけに絞る。

## 今日の判断

1. v0の取得対象は `GET /2/users/me`, `GET /2/users/:id`, `GET /2/users/:id/tweets` をP0にする。
2. `GET /2/users/:id/followers` と `GET /2/users/:id/following` は、個別保存・公開をP1に下げる。今日の昼は集計値と将来拡張用テーブル設計まで。
3. DM、follow/unfollow、投稿、reply、bulk outreachはv0から除外する。
4. 証明ページはraw X API payloadを公開しない。`proof_pages.public_payload` のような公開用DTOだけを生成する。
5. X Contentの削除・protected化・withheld・ユーザー削除要求に追従する `content_compliance_events` をDBに入れる。
6. 価格検証はDeveloper Consoleでendpoint別単価を再確認する。ただし公式docs上でも、Posts/User/Followers/Mediaなどのリソース単価とOwned Reads単価はv0原価見積もりに使える。

## X API / 規約調査

| 観点 | 確認結果 | XGuardへの反映 |
|---|---|---|
| 価格 | X APIはPay-per-use。readは取得リソース単位、write/actionはリクエスト単位。Posts readは$0.005/resource、User readは$0.010/resource、Following/Followers readは$0.010/resource、Owned Reads対象は$0.001/resource。 | 1ユーザーあたり日次で何件取得するかを必ず制限し、`api_usage_events` と `backup_runs.estimated_cost_usd` を持つ。 |
| 課金管理 | Credit balance、auto-recharge、spending limit、Usage endpointがある。 | XGuard側にもユーザー単位の月次上限と停止/通知ルールを作る。 |
| rate limits | rate limitはper-endpoint、per-user/per-app、15分または24時間単位。`GET /2/users/:id/tweets`、`GET /2/users/:id/followers`、`GET /2/users/:id/following` は各rate limitがある。 | `backup_runs` にrate limit headersを保存し、429時は指数バックオフと次回再実行にする。 |
| OAuth | OAuth 2.0 Authorization Code Flow with PKCEでfine-grained scopeを選べる。`offline.access` がある場合のみrefresh tokenが発行される。 | `tweet.read`, `users.read`, `follows.read`, `offline.access` をv0候補にする。tokenは暗号化保存し、frontendへ返さない。 |
| データ保持/公開 | 表示するX Contentは最新状態へ追従し、削除・変更・非公開化などに応じて削除/修正が必要。公開hydrated contentの再配布には制限がある。 | 証明ページはID、件数、期間、代表投稿の限定表示に寄せる。raw payload公開と大量CSV公開は避ける。 |
| automation | write actions、DM、follow/unfollow、auto-replyは明示同意、opt-out、bulk禁止、Automation Rules対応が必要。 | v0から全write scopeを外す。通知はX上の自動送信ではなく、画面内の手動コピー文案にする。 |
| BAN evasion | XのAuthenticity policyは、停止措置回避のための新規アカウント作成、停止アカウントの模倣、別アカウント再利用を禁止する。 | LP文言は「BAN回避」「復活」「迂回」ではなく、「事前バックアップ」「証明ページ」「移行準備」「手動再起動支援」に固定する。 |

## 競合・隣接ツール

| Source | URL | 1行要約 | なぜ重要か |
|---|---|---|---|
| X API Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIのPay-per-use、リソース別単価、Owned Reads、spending limit、Usage endpointが整理されている。 | 月額3,000円の原価設計と、日次バックアップ件数制限の根拠になる。 |
| X API Rate Limits - X | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別、per-user/per-appのrate limitと429時の前提が示されている。 | backup jobのスケジューリング、429処理、rate-limit header保存が必須だと分かる。 |
| OAuth 2.0 Authorization Code Flow with PKCE - X | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | PKCE、fine-grained scope、`offline.access` とrefresh tokenの扱いが説明されている。 | XGuardの最初の実装をOAuth callback、token repository、scope境界に絞る根拠になる。 |
| X Developer Policy - X | https://docs.x.com/developer-terms/policy | privacy/control、content redistribution、offline storage、削除/修正追従、consentが規定されている。 | proof pageをraw公開せず、compliance queueを先に作る理由になる。 |
| Restricted uses of the X API - X | https://docs.x.com/developer-terms/restricted-use-cases | spam、auto-response、sensitive inference、redistributionの制限が整理されている。 | follower/following個別データや自動通知をv0から外す判断材料になる。 |
| Developer Guidelines - X | https://docs.x.com/developer-guidelines | scraping禁止、bulk DM/unsolicited outreach、rate limit abuseなど禁止事項が実装者向けに整理されている。 | XGuardは公式APIのみ、read-onlyのみ、write automationなしに固定すべき。 |
| Authenticity - X Help | https://help.x.com/en/rules-and-policies/authenticity | ban evasion、inauthentic behavior、bulk DM/follow churn、indiscriminate followingの禁止が説明されている。 | 「BAN後の新アカウント誘導」は、規約回避に見えない表現とUI設計が必要。 |
| Xportkit | https://xportkit.com/ | public Xアカウントのfollowers/following/tweetsをcredit制でexport・分析するツール。 | export/分析需要はあるが、XGuardは「本人の事前保護」と「proof」に寄せて差別化できる。 |
| Bestweet | https://bestweet.com/ | X archive fileから検索可能な独立バックアップを作るベータツール。 | APIだけでなく公式archive uploadを補助経路にする余地がある。 |
| ArchivlyX | https://www.archivlyx.com/ | Twitter/Xの閲覧、download、followers/following export、bookmark/likes管理などの総合ツール。 | 隣接市場は「管理・download・export」が中心で、BAN後の証明ページ特化はまだ空きがある。 |
| Unfollr | https://www.unfollr.com/ | browser extensionでfollowers/following snapshotを比較する無料・privacy-firstツール。 | local/browser型の低コスト競合があるため、XGuardはSaaS運用価値と有事導線を明確にする必要がある。 |
| PiunikaWeb: X users report wave of bans | https://piunikaweb.com/2026/03/14/x-users-report-wave-of-bans-for-inauthentic-behaviors/ | 2026年3月にinauthentic behaviorの誤検知BAN波が報じられ、99%復旧との公式反応も載る。 | creator側の不安は現実にあるが、過度な恐怖訴求ではなく「事前準備」に寄せるべき。 |
| The Guardian: X suspends 800m accounts | https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia | Xがspam/manipulation対策で大規模アカウント停止を行っていると報じている。 | 市場シグナルとして、正当なユーザーも巻き添えを恐れる文脈が強い。 |

## 競合から見たポジショニング

既存の隣接ツールは、tweet delete、archive search、followers/following export、audience analytics、browser extension型snapshotに寄っている。XGuardは以下で差別化する。

- 平常時の自動バックアップと有事のproof pageを一体化する。
- 本人がOAuth許可した自分のアカウントに限定し、第三者アカウント大量exportを主価値にしない。
- 「復旧」ではなく、活動実績・期間・代表投稿・プロフィール履歴を見せる証明ページを中心にする。
- 自動DMや一括followではなく、ユーザーが手動で使う告知文、プロフィール文、固定投稿文の生成にする。

## 市場シグナル

- Xはspam/manipulation対策を強めており、誤検知や復旧遅延への不安がユーザー側にある。
- RedditやX上の個別報告はノイズが大きいが、「なぜ停止されたのか分からない」「appealが機械的」「フォロワー資産を失う」という痛みはXGuardの仮説と一致する。
- creator向けには「BANが怖い」より、「Xだけに信用・収益導線を置くリスクを下げる」という表現が安全。

## 昼の実装スコープ

### 対象ディレクトリ

- `/Users/uryuatsuya/XGuard/xguard`

### 昼に作る/変更するもの

1. `docs/ARCHITECTURE.md`
   - v0構成: Next.js frontend、Express worker/API、Supabase、Stripe、X API。
   - read-only境界、proof DTO、compliance queue、usage trackingを明記する。
2. `supabase/schema.sql`
   - 既存MyLife側の `company/projects/x-ban-recovery-storage/technical/supabase-v0-schema.sql` をv1化する。
   - 追加必須: `x_oauth_connections`, `api_usage_events`, `backup_runs`, `proof_pages`, `content_compliance_events`, `stripe_events`。
   - token値は平文列にしない。暗号化/外部secret store前提の列名にする。
3. `shared/types.ts`
   - `XAccountStatus`, `BackupRunStatus`, `ProofPageVisibility`, `ContentComplianceEventType`。
   - `ProofPublicPayload` はraw X payloadと分離する。
4. `docs/API_COST_MODEL.md`
   - 1日あたり投稿100件、プロフィール1件、followers/followingはP1として未計上の試算。
   - Developer Console確認待ち項目と、X API spending limit運用を記録する。
5. `docs/COMPLIANCE.md`
   - X Content削除/変更追従、ユーザー削除要求、proof page取り下げ、raw payload非公開を明記する。

### 昼に実装しないもの

- LP/HP。
- 自動DM。
- 自動follow/unfollow。
- tweet.write / follows.write / dm.write scope。
- follower/following個別一覧の公開。
- BAN回避に見える新アカウント自動作成・自動誘導。

### 昼の検証

```bash
cd /Users/uryuatsuya/XGuard/xguard
git status --short
test -f docs/X_API_SCOPE.md
test -f docs/IMPLEMENTATION_GATE.md
test -f supabase/schema.sql
test -f shared/types.ts
git diff --check
```

必要なら、コード作成後に `npm`/`pnpm` 初期化と `tsc --noEmit` は昼側で実行する。
