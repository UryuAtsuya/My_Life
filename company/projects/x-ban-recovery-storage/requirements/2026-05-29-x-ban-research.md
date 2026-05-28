---
date: "2026-05-29"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-29 XGuard 朝調査

## 結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、XGuard実装repoの現在地を安全に確定し、未push/重複の可能性があるledger実装を比較したうえで、real OAuth設定確認とDeveloper Console原価確認へ進める。

昨日からの差分で重要なのは、指定パス `/Users/uryuatsuya/XGuard/xguard` が今朝も `writable=no` だが、Git状態は `main...origin/main` でclean、HEADは `455718c Add XGuard frontend prototype` になっていること。一方、昨日の一時clone `/private/tmp/xguard-midday-2026-05-28` は `9be85a1 Add Supabase API usage ledger repository` で `origin/main [ahead 1]` のまま。昼runは `9be85a1` をそのままpushせず、指定パスの `c0a7dcd Add Supabase usage ledger repository boundary` と差分比較して、未反映分だけ取り込む。

v0の約束は維持する。「BAN復活」ではなく、本人が事前同意したXデータのread-only backup、原価上限付きbackup job、BAN後の手動再起動を支えるproof pageに限定する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはPay-per-useで、credit購入、endpoint別課金、Developer Consoleでの価格確認、spending limit、Usage endpointが前提。Owned Readsは「自分のdeveloper appで自分のdata」を読む条件付きで低単価。 | 月額3,000円案は、通常read単価を保守的な主前提にして、ユーザー別 `monthly_api_cost_limit_usd` で止める必要がある。 |
| X API Usage | https://docs.x.com/x-api/usage/introduction | `/2/usage/tweets` はPost消費を日別・app別・project cap付きで返し、Pay-per-use planには月次Post read capがある。 | 内部 `api_usage_events` と外部Usage APIを突合する監査jobを作る根拠。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app/per-user制限があり、rate-limit headerで残数とreset時刻を確認できる。Usage endpoint自体にも制限がある。 | backup workerはrate-limit header保存、429 backoff、ユーザー単位queue、過剰polling防止が必須。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | scopeは granular permission。`tweet.read`, `users.read`, `offline.access` と、write/DM/follow/bookmark/list系scopeが分離されている。 | v0 consentは `tweet.read`, `users.read`, `offline.access` のみ。follow/DM/write系は初期画面に出さない。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X ContentとX APIの利用はprivacy expectation、protected/private content、DM、利用目的開示、ポリシー変更追従が求められる。 | proof pageはraw payload公開を避け、公開DTO、redaction、revocation、削除/非公開/withheld追従queueを実装境界にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | 2026-04-27更新のDeveloper Agreementは、Licensed Material、API資格情報、Developer Terms、Automation Rules遵守を契約条件にしている。 | token/secret管理、API key共有禁止、use case変更時の説明更新、実装repoのcompliance docs更新が必要。 |
| X Developer Guidelines | https://docs.x.com/developer-guidelines | browser automation scrapingは不可、AI/ML training用途や過剰再配布は禁止寄り。DMは相手起点・opt-out、like/follow等はユーザー起点が基本。 | XGuardはAPI経由・本人同意・手動支援に寄せ、自動DM、自動follow/unfollow、自動投稿、bulk outreachをv0から除外する。 |
| Honoring user intent on Twitter | https://developer.x.com/en/docs/x-api/compliance/streams/integrate/honoring-user-intent | delete、protect、suspend、withhold、geo scrubなど、X上の状態変化に応じて保存・表示側も追従する必要がある。 | backupは「永久公開」ではなく、状態変化を反映するcompliance jobとproof page visibility制御を持つ必要がある。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | tweets/bookmarks/likesを毎日private GitHub repoへ同期し、月額 `$8` で自動backupを訴求している。 | 継続backup単体の支払い余地はあるが、XGuardの月額3,000円案はproof/recovery支援を明確に足す必要がある。 |
| ArchivlyX | https://www.archivlyx.com/ | Twitter/Xのbookmark、likes、posts、followers/followingを整理・export・bulk管理するall-in-one tool。 | export/整理は競争が強い。XGuardはBAN後の本人性証明と原価管理付き事前backupに絞る。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制で取得・分析・CSV exportする。 | audience export需要はあるが、XGuardはpublic scraping寄りにせず、本人OAuth同意とX policy追従を差別化軸にする。 |
| Twex | https://www.twex.tools/ | X/Twitter audienceをCSV exportし、outagesやbansに備える訴求をしている。 | 「social capital backup」は市場にある。XGuardは自動拡散ではなく、事前保存とproof pageの安全な再起動支援に寄せる。 |
| Bestweet | https://bestweet.com/ | X archiveから独立したbackup accountを作る訴求をしている。 | 「backup account」方向はban evasionに見えやすい。XGuardは新アカウント自動作成や復旧保証を避ける。 |
| Twibird Pricing | https://twibird.com/pricing | likes/bookmarks検索、整理、CSV/Notion export、cloud tweet backupを低価格帯で提供している。 | likes/bookmarks管理は低価格競争。XGuardはaccount continuity、compliance、proof DTOに集中する。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| The Guardian: X suspends 800m accounts in one year amid massive scale of manipulation attempts | https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia | Xはplatform manipulation/spam対策で大規模なアカウント停止を行っていると報じられている。 | 誤検知・巻き添え不安を持つcreatorに、事前backupと証明ページの価値を説明しやすい。 |
| PetaPixel: X is Cracking Down on Accounts That Rip Off the Work of Photographers and Other Creators | https://petapixel.com/2026/05/26/x-is-cracking-down-on-accounts-that-rip-off-the-work-of-photographers-and-other-creators/ | Xがcreator contentの無断再投稿・収益分配悪用への取り締まりを強めている。 | creatorは収益・信用・作品履歴のplatform riskに敏感。活動実績の保存と本人性証明の需要がある。 |
| TechCrunch: X is shutting down Communities because of low usage and lots of spam | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X Communitiesは低利用とspamを理由に終了し、community運営者は移行を迫られた。 | platform機能終了もリスク。XGuardは投稿履歴だけでなく移行先案内・proof pageの導線が重要。 |
| Reddit: Download an archive of your data after suspension | https://www.reddit.com/r/twitterhelp/comments/1sf1nar/download_an_archive_of_your_data_after_suspension/ | 停止後にdata archiveを取得してもfollowers/following/likesが空になる体験談がある。 | 「BAN後に取ればよい」では遅い可能性がある。平常時backupを訴求する根拠。 |
| Reddit: The Truth Behind X Mass Suspensions April 2026 | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | mass suspension後に復旧、再ロック、human verificationが揺れた体験談が集まっている。 | BAN検知は断定せず、`suspension_candidate`, `auth_revoked`, `api_outage`, `rate_limited` を分ける必要がある。 |
| Creator Relay on hold | https://creatorrelay.com/ | 新規Xアカウントが作成直後に停止され、creator charity projectが保留になった経緯を公開している。 | 新アカウント再起動も摩擦がある。XGuardは自動作成ではなく、本人が手動で使う証明・告知・代替導線に限定する。 |

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

1. `/Users/uryuatsuya/XGuard/xguard` のwrite権限、`git fetch` 可否、remote HEAD、local HEAD `455718c` の位置を確認する。
2. `/private/tmp/xguard-midday-2026-05-28` の `9be85a1` と指定パスの `c0a7dcd` を比較し、未反映のledger transaction実装があるか判断する。
3. 未反映分があれば、指定パスがwritableなら取り込み、writableでなければ新しい `/private/tmp/xguard-midday-2026-05-29` でremote最新から作業する。
4. real OAuth env (`X_CLIENT_ID`, `X_CALLBACK_URL`, 必要なら `APP_BASE_URL`) を入れたconfigured mode確認を行う。secret値はcompany文書に書かない。
5. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
6. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check`, stage後 `git diff --cached --check` を基本にする。
