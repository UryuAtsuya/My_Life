---
date: "2026-06-06"
project: "xguard"
type: "morning-research"
status: "completed"
---

# 2026-06-06 XGuard 朝調査

## 結論

XGuardは今日も最優先。市場側の需要は「Xが止まると仕事・告知・信用が止まる人」にある一方、X API/Developer Policy上は、保存・公開・自動化をかなり保守的に設計する必要がある。

v0は引き続き `tweet.read`, `users.read`, `offline.access` のread-only backupとproof pageに限定する。自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線、第三者データの過剰保存は作らない。今日の実装優先は、backup / proof APIの認証・所有権・visibility/revocation境界を閉じること。

## 公式API / 規約ソース

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはpay-per-usage。Developer Consoleでcredit、endpoint別単価、spending limit、Usage endpointを確認する設計。 | 月額 `1,980円 / 2,980円 / 4,980円` の原価管理は、固定プランではなく実消費・上限前停止・Usage endpoint監視が前提になる。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app / per-user rate limitがあり、Usage endpointは `GET /2/usage/tweets`。 | backup jobはper-user/per-app上限と429処理を実装し、BAN検知とrate limitを混同しない必要がある。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | 表示・保存したX Contentは削除/変更/非公開/停止に追従し、必要時は24時間以内に削除または修正する。 | proof pageは永続公開ではなく、削除追従、visibility、revocation、redaction、監査ログをrelease gateにする。 |
| X Developer Guidelines | https://docs.x.com/developer-guidelines | API access終了時はX data削除、24時間削除対応、off-X matching同意、credential保護、Automation Rules遵守が必要。 | XGuardは利用停止・API access終了時の全削除runbookと、Xアカウント連携同意文を必須にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | 商用利用が初期開発・限定end-userを超える場合はEnterprise plan適用が必要になる可能性がある。 | 有料公開前にEnterprise適用要否を確認し、未確認のまま大規模LP/課金を走らせない。 |
| X Compliance Streams Introduction | https://docs.x.com/x-api/compliance/streams/introduction | 削除などのcompliance eventを近リアルタイムで受ける仕組みがある。 | v0では手動/定期再取得でも、将来は削除追従の自動化候補として評価する。 |

## API / コンプライアンス判断

- `Owned Reads` は複数顧客向けXGuardの主原価前提にしない。Developer app owner本人向けの低単価枠として扱い、一般ユーザーbackupは通常read単価で見積もる。
- backup jobは、X API 403/404、token失効、rate limit、X障害を分けて記録する。403/404だけで「BAN確定」と表示しない。
- proof pageは、public DTOだけを返す。raw X API payload、token material、private/protected content、他ユーザーが見る権限のないデータは返さない。
- `follows.read`、DM、write/follow scopeはv0から外す。通知・移行は「手動レビュー用の告知文生成」と「proof URL提示」に寄せる。
- API access終了時、ユーザー退会時、X側削除/非公開/停止検知時の削除・非公開化runbookを `docs/COMPLIANCE.md` に入れる。

## 競合 / 隣接ツール

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| Backread | https://www.backread.app/ | X bookmarksを同期・分類・Markdown exportする個人向けツール。Proは月額5ドル。 | backup単体の価格期待値は低い。XGuardはproof pageと再起動導線を価値の中心にする必要がある。 |
| FeedMirror | https://feedmirror.app/ | social media contentの自動backupを掲げ、official APIs経由を訴求。 | 「あなたのコンテンツにはbackup planが必要」という訴求はXGuardと近い。差別化はBAN後の本人証明と再起動支援。 |
| PostCapture | https://postcapture.com/ | Xなどの投稿スクリーンショット生成。credit課金や月額プランで、履歴保存期間もプラン差にしている。 | proof pageの見せ方は「保存済み投稿を外部で見せる」需要と近いが、XGuardはスクショ生成ではなく権限境界と削除追従を持つ必要がある。 |
| XWipe比較記事 | https://getxwipe.com/blog/best-tweet-deleter-tools-2026 | Tweet削除/cleanup系ツールは月額19ドル以上のプランもあるが、用途は削除・整理。 | XGuardはcleanupではなく「停止時に残す証拠・再起動導線」なので、価格比較は参考に留める。 |
| Brolly Social Media Archiving | https://brolly.io/pricing/ | social media archivingを記録件数ベースで課金し、複数SNS/公的記録寄り。 | 高単価B2B archivingとは別市場。XGuard v0は個人/小規模事業者向けに軽く始める。 |
| Tweet Archivist Pricing | https://www.tweetarchivist.com/about/pricing | Tweet保存・検索・API accessを含むアーカイブ系ツール。 | 「保存・検索」だけでは既存カテゴリに埋もれるため、proof / continuityの訴求が必要。 |

## 市場シグナル

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| TechCrunch: X says it will suspend creators from revenue-sharing program for unlabeled AI posts of armed conflict | https://techcrunch.com/2026/03/03/x-says-it-will-suspend-creators-from-revenue-sharing-program-for-unlabeled-ai-posts-of-armed-conflict/ | Xのcreator monetizationは、ポリシー違反時に収益プログラム停止があり得る。 | X上の信用・収益が事業資産になっている層には、アカウント/収益停止リスクの実感がある。 |
| TechCrunch: X says it’s reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | clickbaitや操作的な投稿に対して収益減額方針が出ている。 | XGuardはgrowth automationではなく、規約順守の保全ツールとして位置づけるべき。 |
| Postory: Twitter/X Account Suspended | https://postory.io/blog/twitter-account-suspended | 2026年時点の停止理由、appeal、archive downloadの案内を整理。 | ユーザー教育では「停止後にできること」より「停止前にbackupしておくこと」を強調できる。 |
| Reddit: June 2026 X/Twitter account problems thread | https://www.reddit.com/r/Twitter/comments/1ttgvgs/june_2026_rtwitter_mega_open_thread_for/ | 2026年6月にも、停止・locked・appeal待ちの不安投稿が継続している。 | 個人の不安は現在進行形。ただし匿名投稿なので、LPの主証拠ではなく需要仮説の補助に使う。 |
| Reddit: Backup tweets from x.com? | https://www.reddit.com/r/DataHoarder/comments/1txnn76/backup_tweets_from_xcom/ | 2026年6月時点で、X閲覧制限により従来のweb archive手段が使いにくいという相談。 | browser automationやスクレイピングに寄らず、official API前提のbackupで信頼を取る余地がある。 |
| Reddit: Backing up social media accounts | https://www.reddit.com/r/DataHoarder/comments/1rdesw2/backing_up_social_media_accounts/ | 友人のX停止をきっかけに、social media backup toolを探す投稿。 | 「停止してから気づく」市場なので、Free診断でリスクを可視化する導線が有効。 |
| Creator Relay on hold | https://creatorrelay.com/ | Xアカウント停止によりプロジェクト進行が止まった事例として公開されている。 | アカウント停止が、個人だけでなくプロジェクトの信頼・告知導線を止める例として参考になる。 |

## 今日のPM判断

1. 今日のTop 1は、backup / proof APIの認証・所有権・visibility/revocation境界。
2. Top 2は、実Supabase/Postgres integration testの実行条件確認と、実行できない場合のCI/writable checkout handoff。
3. Top 3は、`docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` にpay-per-usage、Usage endpoint、spending limit、24時間削除SLA、API access終了時削除runbook、Enterprise確認を反映すること。

## 昼実装への引き継ぎ

- 実装場所: `/Users/uryuatsuya/XGuard/xguard` を第一候補にする。書き込み不可またはfetch不可なら `/private/tmp/xguard-midday-2026-06-06` を使い、MyLife Vaultへproduction codeを置かない。
- 起点: local `HEAD=2b96993 Add OAuth state and PKCE guard`。未追跡 `output/playwright/` は実装前にcommit対象か生成物か判断し、無関係なら触らない。
- 作る/変える候補: `backend/src/app.ts`、backup/proof route tests、proof DTO service/repository境界、必要ならauth helper。
- 検証: `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, backup/proof targeted Vitest, frontend影響があればtargeted Vitest, 実行可能なら `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1`, `npm run check`, `git diff --cached --check`。

## 17:00 再実行リサーチ補強

### 追加結論

同日昼の実装で backup / proof APIの所有権・visibility/revocation境界は `d5aa75e Guard backup proof ownership boundaries` として進んだ。17:00時点の最優先は、XGuard実装commitのpush、実Supabase/Postgres検証、cost/compliance docsのrelease gate化へ移る。

価格・原価面では、X公式docs上のpay-per-useと通常read単価を基準にし、`Owned Reads` はdeveloper app owner本人向け条件として扱う。複数顧客SaaSでは「毎日同期するデータ量を小さくし、Usage endpointとspending limitで止める」設計が必要。

### 追加公式ソース

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはsubscriptionではなくpay-per-usage。Post readは `$0.005/resource`、User readは `$0.010/resource`、write/actionもrequest単位課金。 | XGuardの `1,980円 / 2,980円 / 4,980円` 仮説は、backup件数・保存頻度・proof生成頻度の上限設計なしに成立しない。 |
| X API Pricing - Owned Reads | https://docs.x.com/x-api/getting-started/pricing | `Owned Reads` は `{id}` が認証userと一致し、そのuserがdeveloper app ownerのときに低単価対象。 | 一般顧客の「自分のXデータbackup」をこの低単価で見積もるのは危険。通常read単価で原価モデルを作る。 |
| X API Usage endpoint | https://docs.x.com/x-api/usage/introduction | `GET /2/usage/tweets` でPost消費量を日別・app単位で追跡できる。pay-per-usage planには月間2M Post read capがある。 | 月次上限前停止、ユーザー別cost ledger、Developer Console実値との照合をrelease gateにする。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | rate limitはendpointごとのper-app/per-user制限で、`x-rate-limit-*` headerに残数とresetが返る。`GET /2/users/:id/tweets` はper-user 900/15min。 | backup workerは429とBAN候補を分離し、retry/backoffとuser別停止を実装する必要がある。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | OAuth2のauthorize URLには `state`、`code_challenge`、`code_challenge_method` が必要。callback URLはexact match。 | `2b96993` のOAuth state/S256 PKCE実装は方向性が正しい。次はproof/backup authをSupabase Auth/JWTへ寄せる。 |

### 追加競合 / 隣接ツール

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| Twibird Pricing | https://twibird.com/pricing | X likes/bookmarksのsync、CSV/Notion export、cloud tweet backupを月額 `$8.9` で提供。 | backup/search/export単体の支払期待は低め。XGuardは「証明ページ」「仕事用アカウント保険」「再起動支援」を有料価値にする。 |
| Circleboom Plans and Pricing | https://help.circleboom.com/twitter/getting-started/plans-and-pricing-circleboom-twitter | Twitter managementはfree、delete、Pro、Plus、Premiumの多段階。削除・analytics・account managementが中心。 | XGuardはgrowth/cleanup領域へ寄せず、read-only保全とcomplianceを差別化軸にする。 |
| Circleboom Pricing 2026 analysis | https://curiousblogger.com/circleboom-pricing/ | 個人向けProは年払い換算で約 `$23.99/month`、上位は複数account/大規模follower向け。 | `2,980円 Pro` はX管理ツール市場の下限から中間に入る。proof/restart支援がなければ比較で弱い。 |
| Twibird Standard plan | https://twibird.com/pricing | `10k sync`、cloud tweet backup、Notion exportをStandardで提供。 | XGuardのPersonal上限は、少量sync + proof page + restore checklistに絞るのが現実的。 |

### 追加市場シグナル

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| Audience Ownership for Creators | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | creatorはplatform上のaccount、distribution、accessを直接所有していないという法的・事業リスクを整理。 | XGuardの訴求は「フォロワーを所有する」ではなく「依存リスクを下げ、証跡と移行導線を持つ」にする。 |
| Platform Loyalty Is Dead | https://spotlightjournal.com/platform-loyalty-is-dead-creators-in-2026-are-building-audience-assets-not-follower-counts/ | 2026年のcreatorはfollower数よりaudience asset化を重視するという市場文脈。 | XGuardのLPでは「Xだけに家を建てない」「仕事用Xの保険」という表現が刺さる可能性がある。 |
| Reddit: any twitter backup tools out there? | https://www.reddit.com/r/Twitter/comments/1rgr5ey/any_twitter_backup_tools_out_there/ | 2026年にもtweets、replies、media、followers、followingを保存したい相談が出ている。 | 需要はあるが、公式backupとの比較が必ず出る。XGuardは「公式archive前提 + 継続sync + proof」を分けて説明する。 |

### 17:00時点のPM判断

1. 今日の残Top 1は `d5aa75e` のpush。DNS復旧後にremote先行分を確認し、force pushしない。
2. Top 2は実Supabase/Postgres integration test。実DB URL / `psql` がない場合は、CIまたはwritable checkoutでの実行条件を明記する。
3. Top 3は `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` の更新。価格、Usage endpoint、spending limit、24時間削除SLA、API access終了時削除runbookをproduction No-Go条件へ入れる。
