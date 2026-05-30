---
date: "2026-05-30"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-30 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、昨日push済みの `d30fc48 Harden Supabase usage ledger boundary` を正本にして、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認を閉じる。

2026-05-30 08:09 JST時点で、指定パス `/Users/uryuatsuya/XGuard/xguard` は存在するが、この実行環境からは `XGUARD_NOT_WRITABLE`。Git状態は `main...origin/main`、HEADは `d30fc48`。昼runの最初のgateは、同じ指定パスでwrite/fetchができるかを再確認すること。書けない場合は、Vaultへ実装コードを置かず、`/private/tmp/xguard-midday-2026-05-30` をremote最新から作る。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API | https://docs.x.com/x-api | X APIはpublic conversation、posts、users、DM、listsなどへアクセスでき、pay-per-usage pricingを前提にしている。 | XGuardはread-only backupに限定し、必要以上のscopeやwrite機能を初期同意に入れない。 |
| Usage and Billing | https://docs.x.com/x-api/fundamentals/post-cap | X API v2はcredit-based / per-request pricingで、Developer Consoleのspending limitとUsage確認が前提。Pay-per-usage planにはPost readsの月次capがある。 | `api_usage_events` と `monthly_api_cost_limit_usd` は必須。Developer Console実値を確認するまで、通常read単価で保守的に見積もる。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app / per-user制限があり、rate-limit headerで残数とreset時刻を確認する。 | backup workerは429 backoff、rate-limit header保存、ユーザー単位queueを持つ必要がある。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth 2.0はgranular scopeを使い、`tweet.read`, `users.read`, `offline.access` とwrite/DM/follow系scopeが分かれている。 | v0 consentは `tweet.read`, `users.read`, `offline.access` のみ。`tweet.write`, `dm.write`, `follows.write` は入れない。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X Content、DM、privacy expectation、rate limit、第三者提供、Developer Terms遵守が求められる。 | proof pageはraw payload公開を避け、公開DTO、redaction、revocation、削除/非公開追従を実装境界にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | API利用はDeveloper Agreement、Policy、Automation Rules、Brand Guidelinesなどの遵守が契約条件。API資格情報の取り扱いも制約される。 | secretやtokenをcompany文書に残さず、OAuth設定確認はsecret非表示で記録する。 |
| Developer Guidelines | https://docs.x.com/developer-guidelines | browser automation scrapingは不可、API利用・Automation Rules・DMや自動アクションの制約が強い。 | XGuardはAPI経由、本人同意、手動支援に寄せる。自動DM、自動follow/unfollow、自動投稿、bulk outreachはv0から外す。 |
| More about restricted uses of the X APIs | https://docs.x.com/developer-terms/restricted-use-cases | spammy behavior、write actions、posting、following、DM送信はAutomation Rulesの確認が必要。 | 復元導線を「自動拡散」へ寄せるとpolicyリスクが高い。v0はproof pageと手動告知文までに止める。 |
| Help on your suspended X account | https://help.x.com/managing-your-account/suspended-twitter-accounts | Xはspam、fake account、security riskなどでaccount suspensionを行い、mistakeの場合はunsuspend対応することがある。 | BAN検知は断定せず、`suspension_candidate`, `auth_revoked`, `api_outage`, `rate_limited` を分ける。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | X tweets/bookmarks/likesを毎日private GitHub repoへ同期するbackup tool。 | 継続backup単体の支払い余地はあるが、XGuardはproof pageとcomplianceを足して差別化する必要がある。 |
| Twex | https://www.twex.tools/ | X/Twitter audienceをCSV exportし、outagesやbansに備える訴求をしている。 | 「social capital backup」は既に市場にある。XGuardは本人OAuth同意とpolicy追従を明確にする。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制で取得・分析・CSV exportする。 | followers/following exportは需要があるが、v0で `follows.read` を入れるとscope・原価・policyリスクが増える。 |
| ArchivlyX | https://www.archivlyx.com/ | bookmarks、likes、posts、followers/followingの整理・export・bulk管理を訴求するall-in-one tool。 | export/整理は競争が強い。XGuardはBAN後の本人性証明と事前backupに絞る。 |
| Twibird Pricing | https://twibird.com/pricing | likes/bookmarks検索、整理、CSV/Notion export、cloud tweet backupを低価格帯で提供している。 | likes/bookmarks管理は低価格競争。月額3,000円案はaccount continuityと証明価値を前面に出す必要がある。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X Cracks Down On Accounts That 'Game The Revenue Share Program' | https://www.forbes.com/sites/conormurray/2026/05/29/x-cracks-down-on-stolen-content-demonetizes-major-account-for-gaming-monetization-system/ | Xはcreator monetizationを悪用する大規模アカウントへのdemonetizationを強めている。 | creatorは収益・信用・活動履歴のplatform riskに敏感。証明ページと事前backupの価値が説明しやすい。 |
| X says it will suspend creators from revenue-sharing program for unlabeled AI posts of 'armed conflict' | https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/ | Xは未ラベルAI conflict postsをcreator revenue sharing停止対象にすると報じられている。 | 収益プログラム停止やaccount enforcementが事業リスクになるcreatorへ訴求できる。 |
| X says it's reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | clickbaitやrepost aggregatorへの支払い削減が報じられている。 | XGuardのLPは「規約違反運用の保険」ではなく、正当な本人活動履歴の保全に寄せる。 |
| Reddit: Download an archive of your data after suspension | https://www.reddit.com/r/twitterhelp/comments/1sf1nar/download_an_archive_of_your_data_after_suspension/ | 停止後にdata archiveを取ってもfollowers/following/likesが空になる体験談がある。 | 「BAN後に取得すればよい」では遅い可能性がある。平常時backupの訴求根拠になる。 |
| Reddit: The Truth Behind X Mass Suspensions April 2026 | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | mass suspension後の復旧、再ロック、human verificationの揺れが共有されている。 | BAN検知は断定せず、状態分類と手動確認を前提にする。 |
| Ars Technica: X blames users for Grok-generated CSAM; no fixes announced | https://arstechnica.com/tech-policy/2026/01/x-blames-users-for-grok-generated-csam-no-fixes-announced/ | X Safetyは重大違反コンテンツに対して永久停止を含む対応を示している。 | XGuardは違反回避や復旧保証ではなく、事前同意データの保全とcomplianceに限定する。 |

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

1. `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch可否、remote HEAD、local HEAD `d30fc48` の位置を確認する。
2. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` のservice-role実行、authenticated拒否、所有関係、同一Xアカウント整合性、月次上限超過、負値拒否を確認する。
3. real OAuth envを使い、`/api/x/oauth/start` のconfigured mode、callback URL、scopeをsecret非表示で確認する。
4. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, stage後 `git diff --cached --check` を基本にする。
