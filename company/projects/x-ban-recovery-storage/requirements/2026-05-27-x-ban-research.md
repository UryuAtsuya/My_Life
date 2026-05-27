---
date: "2026-05-27"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-27 XGuard 朝調査

## 結論

XGuardは今日も事業最優先にする。ただし朝会ではproduction codeを触らず、昼の実装を「指定パス同期」「API usage ledger validation」「Developer Console実値確認」に絞る。

v0の約束は引き続き「BAN復活」ではなく、「本人が事前同意したXデータのread-only backup」と「BAN後に手動再起動を支えるproof page」に固定する。

今日の調査で強まった判断は3つ。

1. X APIのPay-per-useは原価設計そのもの。Post/User/Followers reads、Usage endpoint、spending limitをコードと運用台帳で追う必要がある。
2. `Owned Reads` は安いが、第三者ユーザー向けSaaSの通常ユーザーに適用できる前提にしない。Developer Console実画面で適用条件を確認するまで、通常read単価で保守的に見る。
3. 市場にはXデータexport/backup競合があるが、XGuardは「X特化」「本人同意」「規約追従」「公開DTOによる証明ページ」で差別化する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはPay-per-useで、Post readは `$0.005/resource`、User/Followers readは `$0.010/resource`、Owned Readsは `$0.001/resource`。Developer Consoleで現行価格とspending limitを確認できる。 | 月額3,000円で成立するbackup頻度、対象データ、ユーザーあたり上限を逆算する根拠。 |
| X API Usage | https://docs.x.com/x-api/usage/introduction | `/2/usage/tweets` で日別Post消費、app_id、project capを取得でき、消費量をプログラムで追える。 | `api_usage_events` と外部Usage同期jobを分け、課金台帳と公式消費量を突合する必要がある。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app/per-user制限があり、例としてuser tweetsは `10,000/app/15min`・`900/user/15min`、followers/followingは `300/15min`。 | backup jobはユーザー単位queue、`x-rate-limit-*` 保存、429 backoff、過剰polling防止が必須。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | `tweet.read`, `users.read`, `offline.access`, `follows.read`, `dm.read`, `dm.write`, `follows.write` などのscopeが定義されている。 | v0 consent screenは `tweet.read`, `users.read`, `offline.access` のみ。follow/DM/write系は初期同意に入れない。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | 明示的同意、privacy/control、protected/blocked状態の尊重、offline保存したX Contentの削除/修正追従が求められる。 | proof pageはraw payload公開ではなく、公開DTO、redaction、revocation、削除/非公開/withheld追従を前提にする。 |
| X Automation Rules | https://help.x.com/en/rules-and-policies/x-automation | 自動化活動はX RulesとDeveloper Agreement/Policyの対象で、違反すると検索フィルタリングやaccount suspensionにつながる。 | BAN不安を扱うサービスほど、自動DM、自動follow/unfollow、自動投稿、bulk outreachをv0から外す判断が必要。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Twillot Pricing | https://www.twillot.com/en/pricing | personal tweets、bookmarks/likes、following/followersなどをbackup/exportし、Basic `$9.99/month`、Pro `$19.99/month` の価格帯を出している。 | Xデータ保存・整理の支払い余地はあるが、XGuardの月額3,000円案は「proofと再起動支援」を追加価値にしないと高く見える。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制で取得・分析・CSV exportする。 | audience export需要はある。ただしXGuardはpublic scraping寄りではなく、本人OAuth同意とpolicy追従を前面に置く。 |
| FeedMirror | https://feedmirror.app/ | social media backupを自動化し、ban/suspension/hack/policy changeからcontentを守る訴求をしている。 | 「ban protection」訴求は市場に存在する。XGuardはX特化のAPI原価管理とproof pageで差別化する。 |
| Twibird Pricing | https://twibird.com/pricing | X likes/bookmarksの検索・整理・CSV/Notion exportをfreeから `$8.9/month`、Team `$89/month` で提供する。 | 保存・検索・exportは既に低価格競争。XGuardはlikes/bookmarks管理ではなく、BAN後の本人性・活動実績証明に寄せる。 |
| X Communities shutdown coverage | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X Communitiesは2026-05-30へ移行期限が延び、管理者はXChat等へ移る必要があると報じられている。 | creator/community運営者はplatform feature終了や audience migration に敏感。XGuardの「事前準備」訴求と相性がある。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Reddit: X account suspended for inauthentic behavior | https://www.reddit.com/r/twitterhelp/comments/1sfh5x1/x_account_suspended_for_inauthentic_behavior/ | 2026年4月に「inauthentic behavior」で突然停止、appeal即拒否、説明不足を訴える投稿と同様コメントが並ぶ。 | ユーザーの痛みは「復旧保証」ではなく、説明不足・時間差・事業導線喪失への備え。 |
| Reddit: April 2026 mass suspensions discussion | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | mass suspension後に復旧・再ロック・human verificationなどが揺れた体験談が続く。 | BAN検知は断定せず、`suspension_candidate`, `auth_revoked`, `api_outage`, `rate_limited` を分ける必要がある。 |
| TechCrunch: X Communities shutdown | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X上のコミュニティ機能終了で、管理者が別導線へ移行する話題が出ている。 | 「単一platformの機能に依存しすぎない」市場教育が進んでいる。XGuardはowned proof/audience routeの準備として売れる。 |

## 今日のPM判断

### 維持する

- v0 scope: `tweet.read`, `users.read`, `offline.access`
- v0機能: own profile/post backup、usage/cost ledger、proof DTO、削除/非公開/取り下げ追従queue
- LP表現: 「BAN後の再起動支援」「証明ページ」「事前バックアップ」

### v0に入れない

- `follows.read` を使うfollowers/following保存
- `dm.read`, `dm.write`, `tweet.write`, `follows.write`
- 自動DM、auto follow/unfollow、bulk outreach、AI auto replies
- BAN回避、新アカウント自動作成、復旧保証に見える表現

### 昼に確認・実装する

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` のwrite権限とGit履歴を確認し、可能なら `origin/main` の `c7a315c` 以降へ同期する。
2. 指定パスが引き続き書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-27` に一時cloneして作業する。
3. `ApiUsageLedgerService` に非負整数validationと失敗テストを追加する。
4. Developer Consoleでendpoint別単価、spending limit、Usage endpoint、Owned Reads適用条件を実画面確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を基本にする。
