---
date: "2026-06-02"
project: "xguard"
type: morning-research
status: completed
---

# 2026-06-02 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定実装パス `/Users/uryuatsuya/XGuard/xguard` のdirty差分とlive remote状態を最初に確認し、実Supabase/Postgres integration test、OAuth state / S256 PKCE / callback validation、Developer Console原価確認に集中する。

2026-06-02 08:14 JST時点で、指定パスは `exists=yes`, `writable=no`, `main...origin/main`, local `HEAD` / local `origin/main` は `4e6258c`。`supabase/schema.sql` と `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts` に未コミット変更があり、`backend/src/__tests__/supabaseSchemaContract.test.ts` が未追跡。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`、`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com` で未完了。

昨日夜に正本として扱った `8aa0910 Require X account for backup usage events` はlive remote再確認が必要。指定パス側には同等に見える差分が未コミットで残っているため、昼runは巻き戻しではなく、差分内容とremote正本の照合から始める。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。`tweet.read`, `users.read`, `offline.access` 以外のscopeは今日の実装に入れない。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはDeveloper Consoleの現在価格を正本とし、reads/actionsの従量課金、spending controls、Usage APIが事業運用に直結する。 | `api_usage_events`、月次原価上限、Developer Console実画面確認をP0 gateにする。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpointごとにper-user / per-app制限があり、429とrate-limit headers前提で設計する必要がある。 | backup workerはユーザー別queue、backoff、`x-rate-limit-*` 記録を必須にする。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0はfine-grained scopesとPKCEを使い、`offline.access` がrefresh token発行条件になる。 | 静的 `state`、plain/mock PKCE、callback未照合を昼のP1実装課題にする。 |
| X API Scopes | https://docs.x.com/fundamentals/authentication/oauth-2-0/scopes | `tweet.read`, `users.read`, `offline.access` などのscope単位で同意範囲を制御する。 | v0同意画面にwrite/follow/DM scopeを入れない根拠にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | Commercial use、Licensed Materials、policy変更、利用条件が規定される。 | XGuardは商用SaaS候補なので、価格・保存・公開・削除追従を運用記録に残す。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X Contentの保存、表示、削除・非公開化追従、再配布に制限がある。 | proof pageはraw payload公開を避け、公開DTO、redaction、revocation、compliance queueを必須にする。 |
| X Automation Rules | https://help.x.com/en/rules-and-policies/x-automation | 自動DM、bulk follow/unfollow、重複投稿、ユーザー期待を外す自動actionは制限対象になりやすい。 | BAN後通知は自動DMではなく、告知文生成と手動レビューqueueに止める。 |
| X Direct Message FAQs | https://help.x.com/en/using-x/direct-message-faqs | DM送信には日次上限やspam判定があり、同種メッセージの大量送信はリスクが高い。 | `dm.write` はv0から外し、LPでも自動通知を約束しない。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期する低価格backup系サービス。 | backup単体は低価格競合があるため、XGuardはproof pageとcompliance追従で差別化する。 |
| Cyd | https://cyd.social/ | X/Bluesky dataをlocalにbackup/delete/migrateするopen source tool。 | privacy-first需要は強い。SaaSにするならtoken保護、削除追従、説明責任を強める。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制でexport/analyzeする。 | followers/following export需要はあるが、`follows.read` はscope・原価・policy riskが大きい。 |
| Circleboom Plans and Pricing | https://circleboom.com/plans-and-pricing | Twitter/X management、analytics、delete、schedulerなど運用管理機能を提供する。 | XGuardは一般SNS管理ではなく、事前backup、証明ページ、原価上限の狭い用途に寄せる。 |
| Fedica Pricing | https://fedica.com/pricing | Xを含むSNS分析・投稿予約・audience機能をサブスクで提供する。 | 競合は運用効率化が中心。XGuardは「停止時の継続性」と「本人証跡」を中心価値にする。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X says it will suspend creators from revenue-sharing program for unlabeled AI posts of 'armed conflict' | https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/ | creator monetizationはpolicy enforcementにより停止・制限される可能性がある。 | XGuardは規約違反の保険ではなく、正当な活動履歴の保全と説明導線に寄せる。 |
| X says it's reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | Xはclickbaitや低品質投稿への支払い削減を強めている。 | LP文言は収益化の抜け道ではなく、本人性・実績・移行準備に限定する。 |
| X Cracks Down On Accounts That 'Game The Revenue Share Program' | https://www.forbes.com/sites/conormurray/2026/05/29/x-cracks-down-on-stolen-content-demonetizes-major-account-for-gaming-monetization-system/ | revenue share悪用アカウントのdemonetizeが報じられている。 | creatorはplatform enforcementで信用や収益を失うリスクを感じやすい。 |
| Audience Ownership for Creators: Legal Realities and Risk Mitigation Strategies | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | platform上のfollowersや配信面はcreatorが所有していないため、停止や規約変更が事業リスクになる。 | XGuardの価値はfollowers所有ではなく、本人が管理できる活動証跡と移行導線を持つこと。 |
| Reddit: Can I download all my data when I'm suspended? | https://www.reddit.com/r/twitterhelp/comments/1t4xhli/can_i_download_all_my_data_when_im_suspended/ | 停止後のarchive取得でerrorや空データに悩む投稿がある。 | 「停止後にdownloadすればよい」では遅い可能性があり、平常時backupの訴求根拠になる。 |

## 今日のPM判断

### 維持する

- v0 scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: own profile/post backup、usage/cost ledger、proof DTO、削除/非公開/取り下げ追従queue、OAuth configured modeの安全化
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### v0に入れない

- `follows.read` を使うfollowers/following保存
- `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、auto follow/unfollow、bulk outreach、AI auto replies
- BAN回避、新アカウント自動作成、復旧保証に見える表現

### 昼に確認・実装する

1. `/Users/uryuatsuya/XGuard/xguard` のdirty差分、write/fetch可否、live remote、local `HEAD` / `origin/main` `4e6258c` と昨日push済み記録 `8aa0910` の関係を確認する。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行、`authenticated` 拒否、ownership、同一Xアカウント整合性、存在しない `backup_run`、月次上限超過、負値拒否を確認する。
3. OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消し、token repositoryとSupabase schemaの保存契約を一本化する。
4. Developer Consoleでendpoint別単価、credit/spending、Usage endpoint、Owned Reads条件を確認し、XGuard `docs/API_COST_MODEL.md` とcompany gateへ反映する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, stage後 `git diff --cached --check` を基本にする。
