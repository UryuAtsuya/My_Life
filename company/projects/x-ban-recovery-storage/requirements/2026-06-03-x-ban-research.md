---
date: "2026-06-03"
project: "xguard"
type: morning-research
status: completed
---

# 2026-06-03 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは `/Users/uryuatsuya/XGuard/xguard` の `HEAD=origin/main=95e6392` をlive GitHubで再確認し、実Supabase/Postgres integration test、OAuth configured modeの `state` / S256 PKCE / callback validation、token schema契約、Developer Console原価確認に集中する。

2026-06-03 08:24 JST時点で、指定実装パスは `exists=yes`, `writable=no`, `main...origin/main`、local `HEAD` / local `origin/main` は `95e6392`。前回夜レビューどおりworking treeはcleanに見えるが、この朝runでもsandboxからは書き込み不可なので、昼runの最初にwrite/fetch/live remoteを再確認する。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。`tweet.read`, `users.read`, `offline.access` 以外のscopeは今日の実装に入れない。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはsubscriptionではなくcredit購入型のpay-per-usageで、readはresource単位、write/actionはrequest単位の課金。 | `api_usage_events`、月次原価上限、Developer Console実画面確認をP0 gateにする。Post readは `$0.005/resource`、User/Followers readは `$0.010/resource` を保守的見積もりの起点にする。 |
| Usage and Billing - X | https://docs.x.com/x-api/fundamentals/post-cap | 使用量はapp単位で追跡され、Developer Consoleでusage/cost/credit balanceを確認し、budgetやalertを管理する。 | XGuardのbackup workerは「取得量を後から見る」ではなく、実行前に月次上限と残予算で停止判断する必要がある。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpointごとにper-user / per-app制限があり、429と `x-rate-limit-*` headers前提で設計する必要がある。 | backup workerはユーザー別queue、backoff、rate-limit headers保存を必須にする。`/2/users/:id/tweets`、`/2/users/me`、followers/following、DM系は別々に扱う。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0はfine-grained scopes、PKCE、exact callback、CSRF対策用 `state` を要求し、`offline.access` がrefresh token発行条件になる。 | 昼の実装は静的 `state` とplain/mock PKCEを解消し、S256固定、一回限り `state` / `code_verifier` 保存、callback照合を入れる。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X Contentの保存、再配布、第三者提供、protected/blocked/DMの扱いには制限があり、XはAPI利用を監視しうる。 | proof pageはraw payload公開を避け、公開DTO、redaction、revocation、compliance queueを必須にする。 |
| Restricted uses of the X APIs | https://docs.x.com/developer-terms/restricted-use-cases | spam、auto response、off-X matching、sensitive情報、surveillance、redistributionなどの制限が明示される。 | XGuardは本人の明示同意なしにX identityと外部識別子を紐づけない。集計・証明・保管の境界をDBとUIで分ける。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | Licensed Materialの再配布、代替サービス化、token/keyの第三者提供、利用tier変更要求などが制限される。 | 商用SaaSとして、X Contentそのものの公開やAPI key共有、X代替サービスに見える機能を避ける。 |
| Automation rules - X Help | https://help.x.com/en/rules-and-policies/x-automation | OAuth同意だけでは自動actionへの同意にならず、bulk/unsolicited DM、bulk follow/unfollow、rate limit回避、非API自動化は強いリスク。 | v0は自動DM、自動follow/unfollow、自動投稿、bulk outreachを作らない。BAN後は告知文生成と手動review queueに止める。 |
| Understanding X limits | https://help.x.com/en/rules-and-policies/x-limits | DM、post、follow、API requestには技術上限があり、混雑時に制限が一時的に下がる可能性もある。 | write/DM/follow導線は機能として魅力があっても、XGuard v0の安定価値から外す。 |
| How to access your X data | https://help.x.com/en/managing-your-account/accessing-your-x-data | X公式にもarchive downloadはあるが、ログイン・request・通知待ちの手順で、deactivation後は30日制限がある。 | 「停止後にarchiveを取れば十分」とは扱わず、平常時にユーザー同意済みのbackupを積む価値を訴求する。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期し、月額 `$8` を掲げるbackup系サービス。 | backup単体は低価格競合があるため、XGuardはproof page、BAN後の再起動導線、compliance追従、原価上限で差別化する。 |
| twtData | https://twtdata.com/ | tweets、followers/following、analyticsをCSVで販売し、tweetsはrecord単価、followers/followingもrecord単価で提供する。 | export需要は明確だが、XGuardは第三者accountのlead extractionではなく本人backupに限定し、policy riskを抑える。 |
| ArchivlyX | https://www.archivlyx.com/ | public profile閲覧、media download、followers/following export、own Twitter Vaultをまとめたall-in-one管理系。 | 「Twitter dataを所有したい」需要は強い。XGuardは匿名閲覧や任意public exportではなく、own accountの証跡保全に寄せる。 |
| SocialVault | https://socialvault.org/ | Xを含む30+ platformsのcontent backup / local storage / creator向けpricingを訴求する。 | 複数SNS backupは隣接市場。XGuardはまずX特化でOAuth、安全保管、proof DTO、復旧導線の深さを優先する。 |
| Backread | https://www.backread.app/ | X bookmarksのarchive/整理に寄せたツール。 | bookmark/likes系は便利だが、BAN後再起動のコア価値ではない。v0ではscope拡大を避ける。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Creator Relay | https://creatorrelay.com/ | 新規creator projectの公式X accountが停止し、appeal通知と実画面状態が食い違ってprojectが止まっている事例。 | 「本人性・活動計画・移行先を外部に示す証拠ページ」の需要を示す。ただしBAN回避や新アカウント自動作成に踏み込まない。 |
| Audience Ownership for Creators | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | creatorsはplatformのterms、distribution、monetization、policy変更に依存しており、followersを所有しているわけではない。 | XGuardの価値はfollowers所有ではなく、本人が管理できる活動証跡と移行導線を持つこと。 |
| EFF is the latest organization to leave X | https://techcrunch.com/2026/04/09/eff-is-the-latest-organization-to-leave-x/ | EFFがX離脱を表明し、Xのengagement/traffic低下が話題になっている。 | creator continuityは「BANだけ」ではなく、platform価値低下・移行準備も含む。 |
| X suspends 800m accounts in one year | https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia | Xが12か月で大量のmanipulative accountsを停止したと報じられた。 | 正当なユーザーもenforcement不安を感じやすい市場環境。XGuardはspam回避ではなく、正当活動の保全に絞る。 |
| Reddit: X suspensions an X killer? | https://www.reddit.com/r/twitterhelp/comments/1tsm1i2/x_suspensions_an_x_killer/ | 2026-05-31の投稿で、Premium+ userが乗っ取り/third-party app起因のspam投稿後に停止されたと訴えている。 | token管理、third-party app revocation、異常検知、証拠保全はcreator protection文脈で重要。 |
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

1. `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/live remoteを確認し、`95e6392` がGitHub `origin/main` と一致するか確認する。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行、`authenticated` 拒否、ownership、同一Xアカウント整合性、存在しない `backup_run`、`x_account_id` 必須、月次上限超過、負値拒否を確認する。
3. OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合を解消し、token repositoryとSupabase schemaの保存契約を一本化する。
4. Developer Consoleでendpoint別単価、credit/spending、Usage endpoint、Owned Reads条件を確認し、XGuard `docs/API_COST_MODEL.md` とcompany gateへ反映する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run test`, `npm run build`, `npm run check`, stage後 `git diff --cached --check` を基本にする。`npm run check` が `dist/` write `EPERM` の場合は理由と代替検証を記録する。
