---
date: "2026-05-26"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-26 XGuard 朝調査

## 結論

XGuard v0は、引き続き「BAN復活」ではなく「本人が事前同意したXデータの読み取り専用バックアップ」と「BAN後の手動再起動を支える証明ページ」に限定する。

今日の調査で強まった判断は3つ。

1. X APIはPay-per-use前提で、Post/User/Followers readsの単価が事業性に直結する。`Owned Reads` は安いが、第三者ユーザー向けSaaSにそのまま使える前提にしない。
2. v0のOAuth scopeは `tweet.read`, `users.read`, `offline.access` のまま維持する。`follows.read` は原価と公開/削除追従設計が固まるまでP1、DM/write/follow系はv0対象外。
3. 市場には「投稿予約・分析」や「likes/bookmarks保存」はあるが、「BAN後の本人性・活動実績・移行先を手動で示すproof page」への特化はまだ余地がある。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはPay-per-usageで、Posts readは `$0.005/resource`、User readとFollowers/Following readは `$0.010/resource`、Owned Readsは `$0.001/resource` とされる。 | 月額3,000円で成立するバックアップ頻度・保存対象を、endpoint別原価から逆算する必要がある。 |
| X API Usage and Billing | https://docs.x.com/x-api/fundamentals/post-cap | API消費はapp単位で追跡され、pay-per-useには月間Post read 2M capがあり、usage endpointで消費量を追える。 | `api_usage_events` とusage同期jobを昼実装に入れる根拠。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | rate limitはendpoint別・per app/per userで管理され、例としてuser tweetsは `1,500/app/15min`・`900/user/15min`、followers/followingは `300/15min`。 | v0 backup jobはユーザー単位のキュー、429再試行、`x-rate-limit-*` 保存が必須。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | `tweet.read`, `users.read`, `offline.access`, `follows.read`, `dm.read`, `dm.write` などのscopeが明示されている。 | consent screenを最小scopeに保ち、あとから広いscopeを混ぜないための根拠。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | 利用目的説明、明示的同意、protected/blocked状態の尊重、offline保存したX Contentの削除・修正追従が求められる。 | proof pageでraw payloadや非公開/保護/削除済みcontentを出さない設計が必須。 |
| X Developer Guidelines | https://docs.x.com/developer-guidelines | browser automation scrapingは不可、AI repliesは事前承認が必要、auto-DMやbulk followは制限が強い。 | v0で自動DM・自動follow/unfollow・AI返信を作らない判断を再確認。 |
| X Authenticity Rules | https://help.x.com/en/rules-and-policies/authenticity | bulk/high-volume unsolicited replies/mentions/DM、重複投稿、リンクのみDMなどがspam行為として扱われる。 | 「新アカウントへ誘導する自動通知」はv0に入れず、manual queueとproof pageに留める。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Twibird Pricing | https://twibird.com/pricing | Twitter/X likes/bookmarksの検索・整理・CSV/Notion exportを、freeから `$8.9/month`、Team `$89/month` で提供。 | 「保存・検索・export」には支払い余地があるが、対象はlikes/bookmarks中心でBAN後proofではない。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制でexport/analyzeする。 | audience export需要はあるが、public account中心・compliance/本人同意の設計差別化が必要。 |
| SocialVault | https://socialvault.org/ | TikTok/Instagram/Reddit/Xなどの個人メディアを保存するmulti-platform backupツール。Free、Agent `$10`、Pro `$20` の価格帯。 | creator向けbackup訴求は市場に存在する。XGuardはX特化のaccount continuityとproof pageで切る。 |
| FeedMirror | https://feedmirror.app/ | social media backupを自動化し、ban/suspension/hack/policy changeからcontentを守る訴求。 | 「ban protection」訴求は直接競合になり得るため、X API complianceとproof DTOを差別化にする。 |
| Twex | https://www.twex.tools/ | X/Twitter audience exportを「account got banned today?」という痛みで訴求。 | BAN不安を直接LP訴求に使う競合シグナル。ただしXGuardは無断public scraping寄りにしない。 |
| Buffer Pricing | https://buffer.com/pricing | Xを含む複数SNS投稿予約/分析をfreeから `$5/channel/month` で提供。 | 一般投稿予約は低価格競争。XGuardは投稿予約ではなく「事前バックアップ + proof」へ寄せる。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| SWAPD: X.com suspensions report | https://swapd.co/t/x-com-suspends-thousands-of-accounts-over-inauthentic-behavior-raising-concerns-swapd-braces-for-surge-in-unban-requests/1979811 | 2026年3-4月に「inauthentic behavior」理由の突然の停止報告が増えた、というコミュニティ/業界記事。 | BAN/凍結への不安は現在進行形の需要。訴求は恐怖煽りではなく「準備」と「証拠」にする。 |
| Reddit: mass account suspensions thread | https://www.reddit.com/r/twitterhelp/comments/1sgdicr/has_there_been_mass_account_suspensions_going_on/ | 長期利用アカウントやcreatorが突然停止されたという投稿が複数並ぶ。 | ユーザーの言葉では「appeal状況不明」「business accountも閉じた」「main profileが事業導線」などが痛み。 |
| Reddit: banned account restored timeline | https://www.reddit.com/r/twitterhelp/comments/1t7anfe/banned_x_account_how_i_got_it_back_timelineadvice/ | appealを複数回行って復旧した体験談。復旧までの時間差と説明不足が目立つ。 | XGuardは復旧代行を約束せず、待機中に示せるproof/移行先/告知素材を作る。 |
| Metricool 2026 Social Media Study | https://metricool.com/press-release-2026-social-media-study/ | 10主要platform・約106万account・約3976万postの分析で、algorithm changeやAI配信影響が強調されている。 | creator/brandは単一platform依存を下げたい。XGuardはX依存のリスク管理ツールとして位置付ける。 |
| Sprout Social State of Social Media 2026 | https://sproutsocial.com/insights/the-state-of-social-media/ | Q1 2026 pulse surveyでsocial上の信頼・AI生成コンテンツへの不信が大きなテーマ。 | proof pageはAI生成っぽい自動主張ではなく、保存済み履歴・時刻・公開範囲を明確にする。 |
| Creator Economy Report 2026 | https://2026.creatoreconomyreports.com/ | creator economyのリスク、platform changes、creator securityなどを扱う年次レポート。 | XGuardはcreator security / owned audience準備の一部として売る余地がある。 |

## 今日のPM判断

### 維持する

- v0 scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: 自分のprofile/post backup、usage/cost ledger、proof DTO生成、削除/非公開/取り下げ追従queue
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### v0に入れない

- `follows.read` を使うfollowers/following保存
- `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、auto follow/unfollow、bulk outreach、AI auto replies
- BAN回避、新アカウント自動作成、復旧保証に見える表現

### 昼に確認・実装する

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` でremote `origin/main` をfetch/mergeできるか確認する。現在この朝runでは `exists=yes`, `writable=no`, `main...origin/main [ahead 2]`。
2. 書き込み不可なら `/private/tmp/xguard-midday-2026-05-26` の一時cloneを使い、remote `b3bd37c` とlocal `f60be3e`/`91229db` 相当の差分を整理する。
3. `backend/src/__tests__/tokenRepository.test.ts` のfetch mock型修正、`SupabaseTokenRepository.findXToken()` のscope再検査、usage/cost ledgerの最小contractを実装する。
4. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を基本にする。`dist/` emitがEPERMなら理由を明記し、`tsc --noEmit` とvitestを最低ラインにする。
