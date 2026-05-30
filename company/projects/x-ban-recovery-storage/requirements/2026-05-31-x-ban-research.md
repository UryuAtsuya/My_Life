---
date: "2026-05-31"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-31 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定パス `/Users/uryuatsuya/XGuard/xguard` に既に未コミット変更があることを前提に、まず差分の所有者・意図・remote状態を確認し、無関係な変更を巻き戻さずに、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認を進める。

2026-05-31 08:29 JST時点で、指定パスは `exists=yes`, `writable=no`, `main...origin/main`, HEAD `d30fc48`。未コミット変更は `backend/src/__tests__/api.test.ts`, `backend/src/app.ts`, `docs/API_SPEC.md`, `docs/DEPLOY.md`。昼runの最初のgateは、これらの差分を読むこと、`test -w` と `git fetch origin main` を再確認すること、書き込み不可ならVaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-31` をremote最新から作ること。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API | https://docs.x.com/x-api | X APIはposts、users、DM、listsなどの公式API面を提供し、pay-per-usage前提の開発に移っている。 | XGuardは必要最小のread-only endpointだけを使い、backup価値と原価上限を同時に設計する。 |
| Usage and Billing | https://docs.x.com/x-api/fundamentals/post-cap | X APIはcredit / per-request pricing、monthly cap、Developer ConsoleでのUsage・spending確認が前提。 | `api_usage_events`、`monthly_api_cost_limit_usd`、Developer Console実値転記はP0。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpointごとにper-user / per-app制限があり、rate-limit headersで残数とreset時刻を扱う。 | backup workerは429 backoff、ユーザー別queue、rate-limit header記録を必須にする。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0はgranular scopeを使い、read/write/DM/follow系scopeが分かれている。 | v0 consentは `tweet.read`, `users.read`, `offline.access` のみに固定する。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X Content、privacy expectation、rate limit、第三者提供、削除・非公開追従が求められる。 | proof pageはraw payloadを公開せず、公開DTO、redaction、revocation、削除追従を実装境界にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | API利用はDeveloper Agreement、Policy、Automation Rules、Brand Guidelinesを含む契約条件に従う必要がある。 | secret、token、service-role keyをcompany文書やログに残さない。 |
| Developer Guidelines | https://docs.x.com/developer-guidelines | scrapingやbrowser automationではなくAPI利用が前提で、automationやwrite actionの制約が強い。 | XGuardはAPI経由・本人同意・手動支援に寄せ、自動DM/自動follow/自動投稿は外す。 |
| More about restricted uses of the X APIs | https://docs.x.com/developer-terms/restricted-use-cases | spammy behavior、platform manipulation、write actions、following、DM送信は制約が強い。 | 復元導線を自動拡散へ寄せない。proof pageと手動告知文までに止める。 |
| Help on your suspended X account | https://help.x.com/managing-your-account/suspended-twitter-accounts | Xはspam、security risk、fake account等でaccount suspensionを行い、誤停止時はappeal導線がある。 | BAN検知は断定せず、`suspension_candidate`, `auth_revoked`, `api_outage`, `rate_limited` を分ける。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X tweets、bookmarks、likesを毎日private GitHub repoへ同期するbackup tool。 | backup単体の需要はあるが、XGuardはproof page、compliance、原価上限を加えて差別化する。 |
| Twex | https://www.twex.tools/ | X/Twitter audienceをCSV exportし、outagesやbansに備える訴求をしている。 | social capital backup訴求は市場にある。XGuardは本人OAuth同意とpolicy境界を明確にする。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制で取得・分析・CSV exportする。 | followers/following export需要はあるが、v0で `follows.read` を入れるとscope・原価・policyリスクが増える。 |
| ArchivlyX | https://www.archivlyx.com/ | bookmarks、likes、posts、followers/followingの整理・export・bulk管理を訴求する。 | export/整理だけでは競争が強い。XGuardはBAN後の本人性証明と事前backupに絞る。 |
| Twibird Pricing | https://twibird.com/pricing | likes/bookmarks検索、CSV/Notion export、cloud tweet backupを低価格帯で提供している。 | 月額3,000円案は、単なるbackupではなくaccount continuityと証明価値を前面に出す必要がある。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X Cracks Down On Accounts That 'Game The Revenue Share Program' | https://www.forbes.com/sites/conormurray/2026/05/29/x-cracks-down-on-stolen-content-demonetizes-major-account-for-gaming-monetization-system/ | Xはcreator monetizationを悪用する大規模アカウントへのdemonetizationを強めている。 | creatorは収益・信用・活動履歴のplatform riskに敏感。証明ページと事前backupの価値が説明しやすい。 |
| X says it will suspend creators from revenue-sharing program for unlabeled AI posts of 'armed conflict' | https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/ | 未ラベルAI conflict postsはcreator revenue sharing停止対象になると報じられている。 | enforcementが収益リスクになるcreator向けに「正当な活動履歴の保全」を訴求できる。 |
| X says it's reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | clickbaitやrepost aggregatorへの支払い削減が報じられている。 | LPは「規約違反運用の保険」ではなく、正当な本人活動の保全に寄せる。 |
| Reddit: Download an archive of your data after suspension | https://www.reddit.com/r/twitterhelp/comments/1sf1nar/download_an_archive_of_your_data_after_suspension/ | 停止後にdata archiveを取ってもfollowers/following/likesが空になる体験談がある。 | 「BAN後に取得すればよい」では遅い可能性がある。平常時backupの訴求根拠になる。 |
| Reddit: The Truth Behind X Mass Suspensions April 2026 | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | mass suspension後の復旧、再ロック、human verificationの揺れが共有されている。 | BAN検知は断定せず、状態分類と手動確認を前提にする。 |

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

1. `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch可否、remote HEAD、local HEAD `d30fc48`、未コミット変更4ファイルの意図を確認する。
2. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` のservice-role実行、authenticated拒否、所有関係、同一Xアカウント整合性、月次上限超過、負値拒否を確認する。
3. real OAuth envを使い、`/api/x/oauth/start` のconfigured mode、callback URL、scopeをsecret非表示で確認する。
4. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, stage後 `git diff --cached --check` を基本にする。
