---
date: "2026-06-05"
project: "xguard"
type: morning-research
status: completed
---

# 2026-06-05 XGuard 朝調査

## 結論

XGuardは今日も事業最優先にする。前日までに診断endpointの無認証公開は `394a3c3 Add OAuth diagnostic HTTP boundary tests` で解消済みなので、今日の昼実装はOAuth configured modeのCSRF/replay防止、backup/proof APIの認証・所有権境界、実Supabase/Postgres検証、商用compliance gateの順に進める。

調査上の重要点は変わらないが、今日の外部シグナルで優先順位をさらに明確にした。

1. X APIはpay-per-usageで、Posts/User/Followersなどread単価と24時間deduplication、spending limit、Usage endpointを前提に原価上限を実装する必要がある。
2. `Owned Reads` はdeveloper app owner本人のデータに限定されるため、複数顧客向けXGuardの主原価前提にしない。
3. X Contentをoffline保存・表示するサービスは、削除・非公開化・停止・変更への24時間追従、API access終了時の全削除runbook、Enterprise plan適用要否確認をrelease gateにする。
4. 2026年のban wave / anti-bot不安は市場需要を示す一方、XGuardが自動DM、自動follow、自動投稿、BAN回避に寄ると規約・事業リスクが跳ねる。v0は本人backup、証明ページ、手動再起動支援に固定する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはpay-per-usageで、Post readは `$0.005/resource`、User readとFollowing/Followers readは `$0.010/resource`。24時間UTC単位のdeduplication、spending limit、Usage endpointも明記されている。 | `api_usage_events` と `backup_runs` の原価ledger、月次上限前停止、Usage endpoint照合、Developer Console実値確認をrelease gateにする。 |
| X API Rate Limits - X | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app / per-user rate limitがあり、429時は `x-rate-limit-*` headerでresetを判断する。 | backup workerはユーザー別queue、reset時刻保存、backoff、retry抑制を持つ必要がある。 |
| OAuth 2.0 Authorization Code Flow with PKCE - X | https://docs.x.com/resources/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0 user-contextはfine-grained scopesとPKCEを使い、`offline.access` がrefresh token取得に必要。 | 今日のP1は固定 `state`、plain/mock PKCE、callback未照合を解消し、一回限りstateとS256 PKCEを入れること。 |
| How to connect to endpoints using OAuth 2.0 Authorization Code Flow with PKCE - X | https://docs.x.com/resources/fundamentals/authentication/oauth-2-0/user-access-token | callbackで返る `state` はアプリ側で検証し、token交換には `code_verifier` が必要。 | forged / expired / replay callbackテストを先に追加し、callback validationをHTTP境界で固定する。 |
| X Developer Policy - X | https://docs.x.com/developer-terms/policy | X Contentをoffline保存する場合、X上の削除・変更・非公開化・停止状態へ追従し、要求時は24時間以内に削除・変更する必要がある。 | proof pageはraw payload公開ではなく、redaction、revocation、compliance queue、監査ログを必須にする。 |
| Developer Guidelines - X | https://docs.x.com/developer-guidelines | X Content削除、ユーザー要求、API access終了時の全削除など、data handling / display requirementsが整理されている。 | `docs/COMPLIANCE.md` に24時間SLAと10営業日全削除runbookを明示する。 |
| X Developer Agreement - X | https://docs.x.com/developer-terms/agreement | Self-Serve planは限定ユーザー・初期開発・商用prototype向けで、範囲を超える場合はEnterprise plan申請が必要になりうる。 | 公開有料ローンチ前に、use case、保存・表示範囲、顧客数、X Content表示方法をXへ確認するP0事業gateにする。 |
| Restricted uses of the X API - X | https://docs.x.com/developer-terms/restricted-use-cases | spam、surveillance、不正なmatching、再配布などのrestricted useが明示される。 | 第三者account export、lead抽出、bulk outreach、BAN回避導線をv0から外し続ける。 |
| X's automation development rules | https://help.x.com/en/rules-and-policies/x-automation | OAuth同意だけでは自動actionへの十分な同意にならず、bulk DMやbulk follow/unfollowは禁止・制限される。 | v0では自動DM、自動follow/unfollow、自動投稿を実装しない。告知文生成と手動reviewだけにする。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期し、月額 `$8`。 | backup単体は低価格市場。XGuardはBAN後の証明ページ、再起動導線、所有権境界、compliance運用で差別化する。 |
| SocialVault | https://socialvault.org/ | Xを含む30以上のplatformの個人media backupを訴求し、Free / `$10` / `$20` のcredit制プランを提示している。 | creator向けbackup需要は広いが、XGuard v0はmulti-platform化せずX API complianceとproof DTOを深く閉じる。 |
| Postory: Twitter/X Account Suspended | https://postory.io/blog/twitter-account-suspended | 停止後のappealや事前archive取得の重要性を説明する実務記事。 | 「停止後に取り戻す」より「停止前に証跡を保全する」価値をLPとonboardingに入れる。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X suspends 800m accounts in one year amid massive scale of manipulation attempts - The Guardian | https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia | Xが2024年にplatform manipulation / spam対策として8億accountを停止したと報じられている。 | 大規模な自動判定・spam対策が継続しており、creator側のplatform risk対策需要は強い。 |
| X users say inauthentic behaviors ban wave is hitting wrongly flagged accounts - PiunikaWeb | https://piunikaweb.com/2026/03/14/x-users-report-wave-of-bans-for-inauthentic-behaviors/ | 2026年3月のban waveでは、誤検知・即時appeal rejection・復旧メール不整合への不満が報じられた。 | proof pageと時系列証跡は有用だが、XGuardは復旧保証ではなく手動appeal/移行の材料提供に限定する。 |
| X says it is reducing payments to clickbait accounts - TechCrunch | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | Xがclickbait / rapid-fire news aggregation系accountへのcreator payoutを減らす方針を示した。 | creator continuity需要はBANだけでなく、収益ルール変更とplatform依存にも広がる。 |
| Please be aware of X/Twitter's automated anti-bot system - Reddit | https://www.reddit.com/r/twitterhelp/comments/1tujghk/please_be_aware_of_xtwitters_automated_antibot/ | 2026-06-02の投稿で、通常行動がanti-bot判定に見える不安が共有されている。 | 市場不安は強いが、XGuardは自動化を増やさず、本人データ保全と安全な手動再起動支援に寄せる。 |

## 今日のPM判断

### 維持する

- v0 OAuth scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: own profile/post backup、usage/cost ledger、proof DTO、削除・非公開・取り下げ追従queue、OAuth configured mode安全化
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### 今日の実装優先

1. OAuth configured modeに一回限り `state`、S256 PKCE、callback validation、TTL、replay防止を入れる。
2. backup / proof APIへ認証、user ownership、proof visibility/revocation境界を入れる。
3. 実Supabase/Postgres検証と `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` のrelease gate反映を進める。

### v0に入れない

- `follows.read`, `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach
- BAN回避、新アカウント自動作成、復旧保証に見える表現
