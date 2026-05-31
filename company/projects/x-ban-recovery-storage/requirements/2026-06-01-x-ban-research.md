---
date: "2026-06-01"
project: "xguard"
type: morning-research
status: completed
---

# 2026-06-01 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定パス `/Users/uryuatsuya/XGuard/xguard` のlive remote確認、実Supabase/Postgres migration test、Developer Console原価実値確認に絞る。

2026-06-01 08:01 JST時点で、指定パスは `exists=yes`, `writable=no`, `main...origin/main`, local `HEAD` / local `origin/main` は `2655267 Filter revoked tweet snapshots from proof DTO`。`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted` で未完了。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。`tweet.read`, `users.read`, `offline.access` 以外のscopeは昼実装に入れない。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはpay-per-usageで、readsはresource単位、writes/actionsはrequest単位。Developer Consoleが現在価格の正本。 | `api_usage_events` と `monthly_api_cost_limit_usd` はP0。価格はdocsだけで確定せずDeveloper Console実画面で確認する。 |
| Pricing - X: Owned Reads / Spending limits / Usage endpoint | https://docs.x.com/x-api/getting-started/pricing | Owned Readsは自分のdeveloper appで自分のdataを読む場合に低単価枠があり、spending limitとUsage endpointも用意されている。 | 第三者ユーザー向けSaaSでOwned Readsを主前提にしない。Usage endpointとspending limitを運用ゲートに入れる。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpointごとにper-user / per-appの制限があり、429とrate-limit headersを前提にする。 | backup workerは429 backoff、ユーザー別queue、`x-rate-limit-*` 記録を必須にする。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0はfine-grained scopesを使い、`offline.access` がrefresh token発行条件になる。 | v0 consentは `tweet.read`, `users.read`, `offline.access` のみに固定し、write/follow/DM scopeを避ける。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | 2026-04-27更新の契約条件で、Licensed Materialの利用、商用利用、更新・削除追従が規定される。 | XGuardはcommercial prototypeとして、Developer Console・policy変更・削除要求に追従できる設計が必要。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | offline保存したX Contentは、削除・変更・非公開化に追従して削除または変更する必要がある。 | proof pageはraw payload公開ではなく、公開DTO、revocation、redaction、compliance queueを実装境界にする。 |
| X Automation Rules | https://help.x.com/en/rules-and-policies/x-automation | 自動DM、bulk follow/unfollow、無差別list追加、ユーザー期待を外す自動actionは強い制限がある。 | 自動DM、自動follow/unfollow、自動投稿、bulk outreachはv0から外し、手動支援に止める。 |
| X Direct Message FAQs | https://help.x.com/en/using-x/direct-message-faqs | DM送信には日次上限やspam判定があり、重複DMは制限対象になり得る。 | BAN後通知をDM自動送信に寄せず、告知文生成と手動レビューqueueにする。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期し、月額8ドルを訴求している。 | backup単体は低価格帯競合がある。XGuardはproof page、BAN後の再起動導線、compliance追従で差別化する。 |
| Cyd | https://cyd.social/ | X/Bluesky dataをlocalにbackup/delete/migrateするopen source tool。API依存を避ける思想も訴求。 | privacy-first/local backup需要は強い。XGuardはSaaS型にするならtoken保護・削除追従・説明責任を前面に出す。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制でexport/analyzeする。 | followers/following export需要はあるが、v0で `follows.read` を入れるとscope・原価・policy riskが跳ねる。 |
| Circleboom Plans and Pricing | https://circleboom.com/plans-and-pricing | Twitter management、analytics、delete、search、schedulerなど運用管理機能を提供。 | 一般SNS管理ではなく、XGuardは「事前backup + 証明ページ + 原価上限」に狭く寄せる。 |
| Xarchive | https://xarchive.net/ | Wayback Machine上の公開snapshotを検索し、削除済みpostやprofile historyの検証に使える。 | public archiveは補助証拠にはなるが、本人OAuthに基づく事前backupの代替にはならない。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X says it will suspend creators from revenue-sharing program for unlabeled AI posts of 'armed conflict' | https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/ | AI生成の紛争映像を未ラベル投稿したcreatorはrevenue sharing停止対象になると報じられている。 | creator収益はplatform enforcementに左右される。XGuardは「規約違反の保険」ではなく正当な活動履歴の保全に寄せる。 |
| X says it's reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | Xはclickbaitやrepost aggregatorへの支払い削減を進めている。 | LP文言は収益化の抜け道ではなく、本人性・実績・移行準備の安全側に置く。 |
| X Cracks Down On Accounts That 'Game The Revenue Share Program' | https://www.forbes.com/sites/conormurray/2026/05/29/x-cracks-down-on-stolen-content-demonetizes-major-account-for-gaming-monetization-system/ | Xがrevenue share悪用アカウントをdemonetizeしていると報じられている。 | creatorは収益停止・信用喪失リスクを感じやすい。proof pageは「正当な本人活動」を示す用途に限定する。 |
| Audience Ownership for Creators: Legal Realities and Risk Mitigation Strategies | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | creatorはplatform上のfollowersを所有しておらず、停止やpolicy changeで収益・接点を失うリスクがある。 | XGuardの価値はfollowersを所有することではなく、本人が管理できる活動証跡と移行導線を持つこと。 |
| Reddit: Can I download all my data when I'm suspended? | https://www.reddit.com/r/twitterhelp/comments/1t4xhli/can_i_download_all_my_data_when_im_suspended/ | 停止後のarchive取得でerrorや空データを経験する投稿がある。 | 「BAN後にdownloadすればよい」では遅い可能性がある。平常時backupの訴求根拠になる。 |

## 今日のPM判断

### 維持する

- v0 scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: own profile/post backup、usage/cost ledger、proof DTO、削除/非公開/取り下げ追従queue、real OAuth設定確認
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### v0に入れない

- `follows.read` を使うfollowers/following保存
- `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、auto follow/unfollow、bulk outreach、AI auto replies
- BAN回避、新アカウント自動作成、復旧保証に見える表現

### 昼に確認・実装する

1. `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch可否、live remote、local `HEAD` / `origin/main` `2655267` の一致を確認する。
2. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` のservice-role実行、authenticated拒否、所有関係、同一Xアカウント整合性、存在しない `backup_run`、月次上限超過、負値拒否を確認する。
3. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
4. `/api/x/oauth/status` は本番公開前にadmin認証付きhealth checkまたはdeployment-only routeへ寄せる。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, stage後 `git diff --cached --check` を基本にする。
