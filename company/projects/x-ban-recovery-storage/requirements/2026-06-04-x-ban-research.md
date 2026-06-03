---
date: "2026-06-04"
project: "xguard"
type: morning-research
status: completed
---

# 2026-06-04 XGuard 朝調査

## 結論

XGuardは今日も事業最優先にする。v0は本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。

今日の重要な調査差分は3点ある。

1. X公式料金ページの `Owned Reads` は、認証ユーザーがdeveloper appのowner本人である場合に限定される。複数顧客向けXGuardでは主原価に使わず、Post read `$0.005/resource`、User read `$0.010/resource` などの通常read単価で見積もる。
2. X Developer Agreementは、限定ユーザー向けの初期開発を超える商用利用ではEnterprise planへの申請または加入が必要になりうる。公開有料ローンチ前のP0事業ゲートにする。
3. offline保存したX Contentは、削除・非公開化・停止・変更への追従が必要で、削除要求等には24時間以内の対応が求められる。proof pageとbackup snapshotにはcompliance queue、redaction、取り下げ証跡が必要である。

朝runではproduction codeを実装しない。昼runは `/Users/uryuatsuya/XGuard/xguard` のlocal正本 `6024667 Restrict production CORS origins` を起点に、診断endpoint制限、実Supabase/Postgres integration test、OAuth安全化の順で進める。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはcredit購入型のpay-per-usageで、Post readは `$0.005/resource`、User readは `$0.010/resource`。`Owned Reads` はdeveloper app owner本人のデータに限定される。 | XGuard顧客のbackupを `$0.001/resource` 前提にしない。通常read単価、24時間deduplication、spending limitを原価モデルへ反映する。 |
| X API Rate Limits - X | https://docs.x.com/x-api/fundamentals/rate-limits | endpointごとにper-user / per-app制限があり、429と `x-rate-limit-*` headersで復帰時刻を判断する。 | backup workerはユーザー別queue、rate-limit header保存、reset時刻までのbackoffを必須にする。 |
| OAuth 2.0 Authorization Code Flow with PKCE - X | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0 user-contextはfine-grained scopesとPKCEを使い、`offline.access` がrefresh token取得に必要。 | 現在の固定 `state`、plain/mock PKCE、callback未照合を解消し、S256と一回限り照合を実装する。 |
| X Developer Policy - X | https://docs.x.com/developer-terms/policy | X Contentをoffline保存する場合、X上の削除・変更・非公開化・停止状態へ追従し、要求時は24時間以内に削除・変更する必要がある。 | proof pageはraw payloadを公開せず、redaction、revocation、compliance delete queue、対応証跡を持つ必要がある。 |
| Developer Guidelines - X | https://docs.x.com/developer-guidelines | X Content削除要求、user要求、X上の削除・停止への対応期限は24時間、API access終了時はX dataを10営業日以内に削除する。 | compliance jobのSLA、access終了時の全削除runbook、監査ログをrelease gateにする。 |
| X Developer Agreement - X | https://docs.x.com/developer-terms/agreement | 初期開発・限定ユーザー向けを超える商用X API利用ではEnterprise planへの申請または加入が必要になりうる。 | 公開有料ローンチ前にXへuse case、利用規模、保存・表示方法を提示し、適用planを確認する。 |
| More about restricted uses of the X APIs - X | https://docs.x.com/developer-terms/restricted-use-cases | spam、無断matching、surveillance、再配布などのrestricted useが明示される。 | 本人backupに限定し、第三者account export、lead抽出、bulk outreachを作らない。 |
| X's automation development rules | https://help.x.com/articles/76915-automation-rules-and-best-practices | OAuth同意だけでは自動actionへの十分な同意にならず、bulk DMやbulk follow/unfollowは禁止される。 | v0は自動DM、自動follow/unfollow、自動投稿を外し、告知文生成と手動reviewに止める。 |
| How to access and download your X data | https://help.x.com/managing-your-account/accessing-your-twitter-data | X公式archiveはprofile、posts、DM、media、followers/following等をHTML/JSONで取得できるが、requestと通知待ちが必要。 | XGuardは公式archiveの代替を名乗らず、日次差分backup、proof DTO、原価・compliance管理で差別化する。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期し、月額 `$8`。 | backup単体は低価格市場である。XGuardはproof page、停止後の再起動導線、削除追従、原価上限を価値の中心にする。 |
| Backread | https://www.backread.app/ | X bookmarksを継続同期・検索・Markdown exportする隣接サービスで、Proは月額 `$5`。 | 「自分のXデータを持ち出して検索・再利用したい」需要はあるが、bookmark機能はv0 scopeへ追加しない。 |
| SocialVault | https://socialvault.org/ | Xを含む複数SNSのcontent backupとlocal storageをcreator向けに訴求する。 | 将来のmulti-platform continuity市場はあるが、まずXのOAuth・compliance・proof DTOを深く閉じる。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Audience Ownership for Creators: Legal Realities and Risk Mitigation Strategies | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | creatorsはplatform上のaccount、distribution、audience accessを所有しておらず、停止やpolicy変更が収益を直撃する。 | XGuardの訴求を「followers所有」ではなく「活動証跡と移行導線の保全」に固定する。 |
| X says it’s reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | Xがcreator payout条件を変更し、特定運用の収益を削減した。 | creator continuity需要はBANだけでなく、収益ルール変更への備えも含む。 |
| Please be aware of X/Twitter’s automated anti-bot system | https://www.reddit.com/r/twitterhelp/comments/1tujghk/please_be_aware_of_xtwitters_automated_antibot/ | 2026-06-02の利用者投稿で、anti-bot判定や新規account活動による停止不安が共有されている。 | 市場の不安は強いが、XGuardはBAN回避支援ではなく、正当利用者の事前backupと手動再起動支援に限定する。 |
| X suspended my account, says no violation, but still won’t restore it | https://www.reddit.com/r/twitterhelp/comments/1skt7cl/x_suspended_my_account_says_no_violation_but/ | 停止通知とappeal結果が整合しないという利用者事例がある。 | 外部proof pageと時系列の活動証跡は有用だが、復旧保証はしない。 |

## 今日のPM判断

### 維持する

- v0 OAuth scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: own profile/post backup、usage/cost ledger、proof DTO、削除・非公開・取り下げ追従queue、OAuth configured mode安全化
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### 新しく確定する

- 複数顧客向けXGuardでは `Owned Reads` を原価前提にしない。
- 公開有料ローンチ前にX API Enterprise適用要否を確認する。
- X Content削除・変更追従の24時間SLAと、API access終了時の全削除runbookをrelease gateにする。

### v0に入れない

- `follows.read`, `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach
- BAN回避、新アカウント自動作成、復旧保証に見える表現
