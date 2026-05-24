---
created: "2026-05-25"
project: "xguard"
type: research
status: morning-scan
sources:
  - "https://docs.x.com/x-api/getting-started/pricing"
  - "https://docs.x.com/x-api/fundamentals/post-cap"
  - "https://docs.x.com/x-api/fundamentals/rate-limits"
  - "https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code"
  - "https://docs.x.com/developer-terms/policy"
  - "https://docs.x.com/developer-terms/restricted-use-cases"
  - "https://docs.x.com/developer-guidelines"
  - "https://help.x.com/en/rules-and-policies/authenticity"
  - "https://xportkit.com/"
  - "https://bestweet.com/"
  - "https://www.twex.tools/"
  - "https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/"
  - "https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/"
  - "https://www.reddit.com/r/twitterhelp/comments/1t7anfe/banned_x_account_how_i_got_it_back_timelineadvice/"
---

# 2026-05-25 XGuard 朝調査: 原価・規約・市場シグナル再確認

## 結論

XGuardは今日も事業側の最優先にする。v0の方向性は昨日から変えない。つまり「BANされたアカウントを復活させる」ではなく、「本人が事前に許可したXデータをread-onlyで保存し、BAN後に手動で再起動しやすくする証明ページと告知素材を出す」サービスに固定する。

今日の追加判断は、昼の実装をコード機能拡張より先に `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` とbuild設定へ寄せること。公式ドキュメントではX APIがPay-per-usageで、現行単価はDeveloper Consoleで確認する前提になっている。`Owned Reads` は自分の開発者アプリで自分のデータを読む場合の低単価枠だが、XGuardは第三者ユーザーのOAuth接続を扱うため、ここに依存した原価モデルにしない。

## 今日の判断

1. v0初期scopeは `tweet.read`, `users.read`, `offline.access` に維持する。`follows.read`, `dm.read`, `tweet.write`, `follows.write`, `dm.write` は初期同意画面に入れない。
2. 価格・使用量は、X公式docsのPay-per-usageとDeveloper Console実画面確認を正とする。昼は `docs/API_COST_MODEL.md` に「未確認値」と「Developer Console確認待ち」を分けて書く。
3. proof pageは公開DTOだけを返し、raw X API payload、token、第三者一覧、DM、protected由来の内容は公開しない。
4. X Contentの削除、非公開化、withheld、ユーザー削除要求に24時間以内で追従する運用を `docs/COMPLIANCE.md` とDBイベントに明記する。
5. 市場訴求は「BAN回避」「凍結解除」「新アカウント量産」ではなく、「Xだけに信用・収益導線を置くリスクを下げる」「事前バックアップ」「証明ページ」に寄せる。
6. 昼の最初のゲートは `/Users/uryuatsuya/XGuard/xguard` の書き込み可否確認にする。朝run時点ではディレクトリは存在するが、現在のCodexサンドボックスからは `NOT_WRITABLE`。

## X API / 規約調査

| 観点 | 確認結果 | XGuardへの反映 |
|---|---|---|
| 価格 | X APIはPay-per-usage。creditを購入し、API利用に応じて消費する。現行のendpoint別単価はDeveloper Console確認が必要。 | `api_usage_events` と `backup_runs.estimated_cost_usd` を必須にし、Console確認前の試算を確定値として扱わない。 |
| billing cap | Pay-per-usage planにはPost readsの月次capがあり、高ボリュームはEnterprise検討が必要。 | 無制限バックアップを約束しない。1日あたり取得件数、月次停止、ユーザー通知を入れる。 |
| rate limits | `GET /2/users/:id/tweets` はper-app/per-user、`GET /2/users/me` はper-user、followers/followingも別limit。DM writeやfollow writeにも厳しいlimitがある。 | backup jobはrate-limit headerを保存し、429時は失敗ではなく `rate_limited` として再実行予定にする。 |
| OAuth | OAuth 2.0 Authorization Code Flow with PKCEはfine-grained scopeを選べる。`offline.access` なしではrefresh tokenが出ない。 | token repository層はrefresh token前提。token本文は暗号化/secret storeへ寄せ、frontendへ返さない。 |
| Developer Policy | use case descriptionが実質的な拘束条件になる。目的変更やX Contentの扱いはpolicy違反になり得る。 | Developer Portal申請文とLP文言を一致させる。BAN回避・自動拡散に見える表現は避ける。 |
| Developer Guidelines | bulk DMs、unsolicited outreach、browser automation/scraping、rate limit abuseは禁止。削除要求やX側削除に24時間以内で追従する要件がある。 | v0は公式API read-onlyのみ。自動DM、自動follow/unfollow、browser automation、scrapingは実装しない。 |
| Authenticity policy | ban evasionとして、新規アカウント作成、停止アカウントの模倣、既存アカウント転用が禁止例に入る。 | 「新アカウントを自動作成する」「停止回避を支援する」UIは作らない。ユーザーの手動再起動素材に留める。 |
| restricted uses | 個人識別子を保存する分析、再配布、監視、センシティブ推論はリスクが高い。 | followers/following個別一覧の保存・公開はP1以降。P0は集計値と本人所有データのsnapshotに絞る。 |

## 競合・隣接ツール

| Source title | URL | 1行要約 | なぜ重要か |
|---|---|---|---|
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIのPay-per-usage、credit、Developer Consoleでの単価確認、Owned Readsが整理されている。 | 月額3,000円モデルの原価表を「確定値」と「Console確認待ち」に分ける根拠になる。 |
| Usage and Billing - X | https://docs.x.com/x-api/fundamentals/post-cap | usage tracking、Post reads cap、Developer Consoleでのusage/cost monitoringが説明されている。 | `api_usage_events` と月次停止ルールをv0から入れる理由になる。 |
| X API Rate Limits - X | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint別のper-app/per-user limitが一覧化されている。 | backup scheduler、429再試行、rate-limit header保存が必要だと分かる。 |
| OAuth 2.0 Authorization Code Flow with PKCE - X | https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code | fine-grained scope、PKCE、`offline.access` とrefresh tokenの扱いが説明されている。 | 初期scopeをread-onlyに絞り、token repositoryを先に実装する根拠になる。 |
| X Developer Policy - X | https://docs.x.com/developer-terms/policy | 開発者のuse case、privacy/control、X Content利用、policy complianceが規定されている。 | Developer Portal申請、LP、実装機能の整合性を崩さない必要がある。 |
| Restricted uses of the X API - X | https://docs.x.com/developer-terms/restricted-use-cases | 再配布、個人データ、センシティブ推論などの制限が整理されている。 | proof pageの公開情報を最小化し、raw payload公開を避ける判断材料になる。 |
| Developer Guidelines - X | https://docs.x.com/developer-guidelines | bulk DM、unsolicited outreach、scraping、rate-limit abuse、削除追従などの禁止・要件が説明されている。 | XGuard v0からwrite automationを外し、compliance docをP0にする理由になる。 |
| Authenticity - X Help | https://help.x.com/en/rules-and-policies/authenticity | ban evasion、inauthentic behavior、bulk DM/follow churn、suspension enforcementが説明されている。 | 「BAN後の再起動支援」が規約回避に見えない表現・UIにする必要がある。 |
| Xportkit | https://xportkit.com/ | public X accountのfollowers/following/tweet archiveをcredit制でexport・分析する。 | export需要は強いが、XGuardは第三者公開アカウント分析ではなく本人保護に寄せて差別化する。 |
| Bestweet | https://bestweet.com/ | X archive fileから独立バックアップと検索可能プロフィールを作る。 | APIだけでなくX archive upload補助を将来P1に入れる余地がある。 |
| Twex | https://www.twex.tools/ | follower/following exportでsocial capital backupを訴求するX向けツール。 | 価格が安い/単機能の競合に対して、XGuardは有事のproofと運用監視で差別化する必要がある。 |
| TechCrunch: X says it is reducing payments to clickbait accounts | https://techcrunch.com/2026/04/12/x-says-its-reducing-payments-to-clickbait-accounts/ | Xがcreator monetizationでmanipulation/clickbait対策を強めていることを報じている。 | クリエイター収益がX運用ルールに左右される市場シグナルになる。 |
| TechCrunch: X is shutting down Communities | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X Communities終了とspam対策強化、移行導線の必要性が報じられている。 | audience continuityや外部導線保全の不安が増える文脈として使える。 |
| Reddit: Banned X account timeline/advice | https://www.reddit.com/r/twitterhelp/comments/1t7anfe/banned_x_account_how_i_got_it_back_timelineadvice/ | inauthentic behavior判定、appeal、復旧までの個人体験が共有されている。 | 公式ニュースでは拾いにくい「説明不足・復旧不安」の生の痛みを示す。ただし個別事例として扱う。 |

## 競合から見たポジショニング

既存ツールは主に、public account export、archive search、follower/following CSV、bookmark/thread保存、ローカル/拡張機能型backupに寄っている。XGuardは以下の位置に置く。

- 第三者アカウントの大量exportではなく、本人OAuth許可済みアカウントの保護に限定する。
- 単なるCSV exportではなく、証明ページ、公開/非公開制御、削除追従、月次API原価管理をセットにする。
- BAN回避や自動拡散ではなく、手動で使える告知文・固定投稿案・プロフィール文案に留める。
- X archive upload補助はP1候補。P0はAPI read-only backupとproof DTOの品質を優先する。

## 市場シグナル

- Xはspam、clickbait、manipulationへの取り締まりや仕様変更を継続している。
- クリエイターは収益化ルール、コミュニティ閉鎖、アカウント停止、appeal不透明性に影響を受ける。
- Reddit等の個別報告は検証済み統計ではないが、「理由が分からず停止された」「appealが機械的」「フォロワー資産を失う」という痛みは繰り返し出ている。
- LPでは恐怖訴求を強めすぎず、「X依存の事業リスクを下げる」「いつでも説明できる活動実績を持つ」に寄せる。

## 昼の実装スコープ

### 対象ディレクトリ

- `/Users/uryuatsuya/XGuard/xguard`

### 事前ゲート

```bash
cd /Users/uryuatsuya/XGuard/xguard
pwd
git status --short --branch
test -w .
test -f docs/X_API_SCOPE.md
test -f docs/API_SPEC.md
test -f docs/IMPLEMENTATION_GATE.md
test -f supabase/schema.sql
test -f shared/types.ts
```

朝run時点で `/Users/uryuatsuya/XGuard/xguard` は存在し、`main...origin/main` はclean。ただし現在のCodexサンドボックスからは `test -w /Users/uryuatsuya/XGuard/xguard` が `NOT_WRITABLE`。昼runで同じなら、production codeへ進まず、権限解決をブロッカーとして記録する。

### 昼に作る/変更するもの

1. `docs/ARCHITECTURE.md`
   - frontend/backend/shared/supabase/stripe/X APIの境界。
   - read-only scope、token repository、backup job、proof DTO、compliance eventsを明記する。
2. `docs/API_COST_MODEL.md`
   - Pay-per-usage前提。
   - Developer Consoleで確認するendpoint別単価、spending limit、usage/cost monitoring。
   - 1ユーザーあたり日次取得上限と月次停止ルール。
3. `docs/COMPLIANCE.md`
   - X Content削除/非公開化/withheld/ユーザー削除要求への24時間追従。
   - raw payload非公開、proof page取り下げ、token削除、audit log。
4. `tsconfig.build.json` または同等のbuild分離
   - production buildから `backend/src/__tests__/**` を外す。
   - `npm run build` / `npm run check` を通常環境で通す。
5. Supabase repository層の最小実装
   - `TokenRepository` をservice role + encryption/secret store前提にする。
   - token本文をfrontendへ返さない。
   - `auth_expired` 遷移を扱う。

### 昼に実装しないもの

- LP/HP。
- 自動DM。
- 自動follow/unfollow。
- tweet.write / follows.write / dm.write scope。
- follower/following個別一覧の公開。
- 新アカウント作成自動化、停止回避、bulk outreach。

### 昼の検証

```bash
cd /Users/uryuatsuya/XGuard/xguard
git diff --check
npm run build
npm run check
npx vitest run --configLoader runner
```

`npm audit` はネットワーク制限で失敗し得るため、失敗時はDNS/registry到達性と分けて記録する。
