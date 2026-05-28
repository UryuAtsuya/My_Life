---
date: "2026-05-28"
project: "xguard"
type: morning-research
status: completed
---

# 2026-05-28 XGuard 朝調査

## 結論

XGuardは今日も事業最優先にする。朝会ではproduction codeを触らず、昼の実装を「指定パスをpush済み正本へ同期」「Developer Console実値確認」「Supabase ledger transaction repository」に絞る。

v0の約束は引き続き「BAN復活」ではなく、「本人が事前同意したXデータのread-only backup」と「BAN後に手動再起動を支えるproof page」に固定する。

今日の調査で強まった判断は3つ。

1. X APIのPay-per-useは原価設計そのもの。`api_usage_events` と `backup_runs` をSupabase transactionで更新し、ユーザー別 `monthly_api_cost_limit_usd` を超える前にjobを止める。
2. `Owned Reads` は安いが、第三者ユーザー向けSaaSにそのまま適用できるかはDeveloper Console実画面まで未確定。保守的な通常read単価で見積もる。
3. 市場にはbackup/export系の競合が増えている。XGuardは「X特化」「本人同意」「規約追従」「公開DTOによる証明ページ」「BAN後の手動再起動支援」で差別化する。

## 公式X API / Policy調査

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X APIはPay-per-useで、Post readは `$0.005/resource`、User/Followers readは `$0.010/resource`、Owned Readsは `$0.001/resource`。Developer Consoleでcreditや現行価格を確認する。 | 月額3,000円で成立するbackup頻度、対象データ、ユーザーあたり原価上限を逆算する根拠。 |
| X API Usage | https://docs.x.com/x-api/usage/introduction | `/2/usage/tweets` で日別Post消費、app_id、project capを取得でき、Pay-per-use planには月間Post read capがある。 | 外部Usage同期jobと内部 `api_usage_events` を突合し、原価暴走を早く見つける必要がある。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別にper-app/per-user制限があり、`x-rate-limit-limit`, `x-rate-limit-remaining`, `x-rate-limit-reset` で状態を確認できる。 | backup jobはユーザー単位queue、rate-limit header保存、429 backoff、過剰polling防止が必須。 |
| OAuth 2.0 Authorization Code Flow with PKCE | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | `tweet.read`, `users.read`, `offline.access`, `follows.read`, `dm.read`, `dm.write`, `follows.write` などのscopeが定義されている。 | v0 consent screenは `tweet.read`, `users.read`, `offline.access` のみ。follow/DM/write系は初期同意に入れない。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | 明示的同意、protected/private contentの尊重、offline保存したX Contentの削除/修正追従が求められる。 | proof pageはraw payload公開ではなく、公開DTO、redaction、revocation、削除/非公開/withheld追従を前提にする。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | 2026-04-27更新のDeveloper Agreementは、APIやLicensed Materialの不正利用、第三者への資格情報提供、代替サービス化などを制限する。 | token保管、API key共有禁止、X Contentの再配布境界を設計に入れる必要がある。 |
| X Automation Rules | https://help.x.com/articles/76915-automation-rules-and-best-practices | OAuth承認だけでは自動操作の同意にならず、自動DMは事前意思表示・opt-out・頻度配慮が必要。bulk/aggressive follow/unfollowは禁止対象。 | 自動DM、自動follow/unfollow、自動投稿、bulk outreachをv0から外す根拠。 |
| API Restricted Use Cases | https://docs.x.com/developer-terms/restricted-use-cases | X APIでspamやspammy behaviorを作る、または助長する利用は禁止される。 | BAN不安ユーザー向けでも、復旧保証や拡散自動化ではなく、保存・証明・手動再起動に寄せる。 |

## 競合 / 隣接サービス

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| GrokThyself | https://grokthyself.com/ | Xのtweets/bookmarks/likesを毎日private GitHub repoへ同期し、月額 `$8` を掲げる。 | 継続backupに支払い余地がある一方、XGuardの月額3,000円案はproof/recovery支援まで含めないと高く見える。 |
| Twillot Pricing | https://www.twillot.com/en/pricing | tweet monitoring、followers/following整理、backup/exportを価格帯別に出している。 | Xデータ保存・整理は既に競争領域。XGuardは「BAN後の手動再起動」と「規約準拠証明」で差別化する。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archivesをcredit制で取得・分析・CSV exportする。 | audience export需要はあるが、XGuardはpublic scraping寄りではなく、本人OAuth同意とpolicy追従を前面に置く。 |
| Twibird Pricing | https://twibird.com/pricing | X likes/bookmarksの検索・整理・CSV/Notion exportをfreeから有料プランで提供する。 | likes/bookmarks管理は低価格競争。XGuardはaccount continuityとproof pageに寄せる。 |
| FeedMirror | https://feedmirror.app/ | social media backupを自動化し、ban/suspension/hack/policy changeからcontentを守る訴求をしている。 | 「ban protection」訴求は市場に存在する。XGuardはX特化のAPI原価管理とproof pageで差別化する。 |

## 市場シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| PetaPixel: X is Cracking Down on Accounts That Rip Off the Work of Photographers and Other Creators | https://petapixel.com/2026/05/26/x-is-cracking-down-on-accounts-that-rip-off-the-work-of-photographers-and-other-creators/ | Xがcreator contentのprogrammatic reuploadや収益分配悪用への取り締まりを強めている。 | creator側は突然の制限・収益影響に敏感。XGuardは活動実績と本人性の証明を持つ意味がある。 |
| TechCrunch: X is shutting down Communities because of low usage and lots of spam | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X Communitiesはspam問題と低利用を理由に終了し、管理者は移行を迫られている。 | platform feature終了・audience migrationの不安が顕在化している。XGuardの事前準備訴求と相性がある。 |
| Reddit: X account suspended | https://www.reddit.com/r/twitterhelp/comments/1smgxrd/x_account_suspension/ | 2026年4月の停止相談で、backup accountを作るとban evasion扱いされる不安が語られている。 | 「新アカウント自動作成」ではなく、手動再起動支援と証明ページに絞るべき。 |
| Reddit: The Truth Behind X Mass Suspensions (April 2026) | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | mass suspension後に復旧・再ロック・human verificationなどが揺れた体験談が続く。 | BAN検知は断定せず、`suspension_candidate`, `auth_revoked`, `api_outage`, `rate_limited` を分ける必要がある。 |
| Creator Relay on hold | https://creatorrelay.com/ | 新規Xアカウントが作成直後に停止され、charity creator projectが保留になった経緯を公開している。 | 事業・企画開始直後にX導線が止まる痛みがある。proof pageと代替導線準備の価値を説明しやすい。 |
| AAAI ICWSM 2026: The Failed Migration of Academic Twitter | https://ojs.aaai.org/index.php/ICWSM/article/download/42757/50317/46858 | Twitter/Xから他SNSへの移行は単純ではなく、コミュニティ単位の移動には摩擦がある。 | XGuardは「全員を移住させる」より、本人性・実績・新導線を提示する現実的支援に絞る。 |

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

1. 指定パス `/Users/uryuatsuya/XGuard/xguard` のwrite権限とGit履歴を確認し、可能ならpush済み正本 `3528e26` へ同期する。
2. 指定パスが引き続き書き込み不可なら、Vaultに実装コードを置かず `/private/tmp/xguard-midday-2026-05-28` に一時cloneして作業する。
3. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads適用条件を実画面確認し、`docs/API_COST_MODEL.md` とcompany gateへ反映する。
4. `SupabaseApiUsageLedgerRepository` を追加し、`api_usage_events` 記録、`backup_runs` rollup、`monthly_api_cost_limit_usd` 超過前停止をtransaction境界で検証する。
5. 検証は `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, `npx vitest run --configLoader runner`, `npm run check` を基本にする。
