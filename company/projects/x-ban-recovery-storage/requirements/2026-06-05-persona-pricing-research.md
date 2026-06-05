---
date: "2026-06-05"
project: "xguard"
type: persona-pricing-research
status: completed
---

# 2026-06-05 XGuard ペルソナ / 需要 / 価格調査

## 結論

XGuard v0は「一般ユーザーの思い出バックアップ」ではなく、Xが売上導線・告知導線・信用導線になっている人へ絞る。初期ICPは次の3つにする。

1. X中心の個人クリエイター / 個人事業者
2. 仕事用Xアカウントを使う小規模店舗・サロン・コーチ・講座販売者
3. 凍結リスクが高い創作・成人向け・グレー領域クリエイター

価格は「単一月額3,000円」ではなく、v0検証では `Free診断 / 1,980円 Personal / 2,980円 Pro / 4,980円 Concierge検証枠` を仮説にする。保存・検索だけなら980円前後が自然だが、証明ページ、再起動チェックリスト、優先同期、手動支援まで含めると1,980-4,980円を検証できる。

ただし、XGuardはBAN回避、自動復元、自動投稿、自動DM、自動follow/unfollowを売りにしない。競合にそのような訴求があっても、XGuardは本人の事前backup、証明ページ、手動再起動支援、compliance追従に寄せる。

## 優先ペルソナ

| 優先 | ペルソナ | 痛み | 購入動機 | 拒否理由 / リスク | 価格仮説 |
|---:|---|---|---|---|---|
| 1 | X中心の個人クリエイター / ライター / インフルエンサー | 長年の投稿資産、代表投稿、フォロワー導線、本人性が消える | 旧アカ本人であることを証明し、新アカや外部導線へ早く誘導したい | 凍結経験がないと危機感が弱い。単なるbackupなら安く見える | 1,980-2,980円/月 |
| 2 | 小規模店舗 / サロン / コーチ / 講座販売者 | 予約、告知、顧客連絡、信用形成が止まる | 仕事用アカ停止時に、顧客へ見せる証明ページと再告知テンプレを持ちたい | 月額SaaSへの抵抗。SNS担当者がいない | 2,980-4,980円/月 |
| 3 | 成人向け / NSFW / グレー領域クリエイター | 凍結で新規流入、リンク導線、フォロワー把握が切れる | 凍結前に投稿、プロフィール、外部リンク、代表投稿を保存したい | データ保存への不信。再投稿や自動復元は再凍結リスクが高い | 2,980-4,980円/月 |
| 4 | 広告 / アウトリーチを使うsmall business | X Adsや告知導線が止まり、campaign再開が遅れる | 投稿・プロフィール・証明ページを再構築し、広告再開準備を早めたい | 「凍結解除サービスではない」ことに不満が出やすい | 4,980-9,800円/月 |
| 5 | コミュニティ管理者 / ファンダム / イベント運営 | 告知履歴、重要メンバー、移行リンクが消える | 公式性と移行先を証明するページが欲しい | Discord/Telegramなど外部導線で足りる場合がある | 1,980-4,980円/月 |
| 6 | 政治 / 活動家 / 社会運動アカウント | 通報、炎上、地域法対応、規約変更で可視性が不安定 | 発信履歴と本人性を残し、支援者に移行先を示したい | 監視・プロファイリング懸念が強い。X API policy riskが高い | 初期LPでは前面に出さない |
| 7 | リサーチャー / 知識収集ユーザー | bookmark、likes、参照postが削除・非公開・凍結で消える | 個人ナレッジの保全 | 収益被害が直接ではなく、支払意思は低い | 980円/月以下 |

## 需要シグナル

| Source | URL | 1行要約 | XGuardで重要な理由 |
|---|---|---|---|
| Help on your suspended X account - X Help | https://help.x.com/en/managing-your-account/suspended-x-accounts | X公式は、停止理由、本人確認、appeal、個人情報コピー請求を案内している。 | 停止後は対応がappeal中心になり、平常時の証跡保全が必要になる。 |
| About eligibility for X Ads - X Business | https://business.x.com/en/help/ads-policies/campaign-considerations/about-eligibility-for-x-ads | suspended accountはX Adsに参加できない。 | 広告利用者・小規模事業者にとって、停止は集客停止に直結する。 |
| Pricing - X | https://docs.x.com/x-api/getting-started/pricing | X APIはpay-per-usageで、read単価、Usage endpoint、spending limitがある。 | 価格設計はユーザーあたり取得量と月次原価上限を前提にする必要がある。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | offline保存・再表示には削除/変更追従、同意、再配布制約がある。 | proof pageとbackupはcompliance込みで設計し、BAN回避や第三者exportに寄せない。 |
| X automation rules | https://help.x.com/en/rules-and-policies/x-automation | 自動操作、bulk action、spam的挙動は制限される。 | 自動DM、自動follow、自動投稿、自動復元をv0から外す根拠になる。 |
| X suspends 800m accounts - The Guardian | https://www.theguardian.com/technology/2026/mar/09/x-suspends-accounts-massive-scale-manipulation-attempts-russia | Xが大規模なplatform manipulation対策として大量停止を継続している。 | 誤判定巻き込まれ不安とplatform riskの市場背景になる。 |
| X users report wave of bans - PiunikaWeb | https://piunikaweb.com/2026/03/14/x-users-report-wave-of-bans-for-inauthentic-behaviors/ | 2026年3月のban waveでは、通常利用者も停止されたという報告が集まった。 | 「何もしていないのに止まる」不安が、事前backup需要につながる。 |
| Audience Ownership for Creators - Odin Law | https://odinlaw.com/blog-platform-dependence-risks-for-creators/ | creatorはplatform上のaccount、distribution、audience accessを所有していない。 | XGuardの訴求は「フォロワー所有」ではなく「活動証跡と移行導線の保全」にする。 |
| X Backup | https://xbackup.withllm.com/ | 日本語圏で凍結前backup、復元、Pro 3,000円/月を訴求している。 | 国内に直接近い需要と価格ベンチマークがある。ただし自動復元・凍結回避色はXGuardでは採用しない。 |
| FeedMirror | https://feedmirror.app/ | ban / hack / policy change対策として複数SNSの自動backupを、Free / $9 / $29 / $99で訴求している。 | backup単体は低価格から始まるが、creator continuityなら$29帯も検証できる。 |
| Twillot Pricing | https://www.twillot.com/en/pricing | bookmarks、likes、tweets、followers/following管理をFree / $4.99 / $9.99 / $19.99で提供している。 | Xデータ保存・検索・管理の低価格アンカーになる。 |
| GrokThyself | https://grokthyself.com/ | X posts、bookmarks、likesをprivate GitHub repoへ毎日同期し、月額$8。 | backup単体の相場は1,000円台に寄る。XGuardはproofと再起動支援で差別化する。 |

## 競合 / 価格ベンチマーク

| カテゴリ | ツール | 価格 | 示唆 |
|---|---|---:|---|
| X backup | GrokThyself | $8/月 | 自動backupだけなら1,000円台が自然。 |
| X data manager | Twillot | Free / $4.99 / $9.99 / $19.99 | bookmarks、likes、tweets、followers/followingの管理は低価格競争。 |
| 複数SNS backup | FeedMirror | Free / $9 / $29 / $99 | ban / hack / policy changeへのbackup価値は、creator向けなら$29帯まである。 |
| 国内凍結対策 | X Backup | Free、復元500円/回、Pro 3,000円/月 | 国内で3,000円/月の直接競合がある。XGuardは規約・compliance・proof pageの堅さで差別化する。 |
| SNS管理 / growth | Hypefury / Tweet Hunter | $29以上 | Xで稼ぐ人は運用SaaSに高単価を払うが、XGuardはgrowthではなくcontinuity保険として売る。 |
| local archive | Social Archiver系 | $3.99/月前後 | 個人ナレッジ保存だけでは980円以下に寄る。 |

## 価格仮説

| プラン | 月額 | 対象 | 含める価値 | 注意 |
|---|---:|---|---|---|
| Free診断 | 0円 | 初回接触・不安層 | 凍結リスク簡易チェック、保存対象の見積もり、proof sample | APIを使いすぎない。恐怖訴求に寄せすぎない。 |
| Personal | 1,980円 | X中心の個人クリエイター / 個人事業者 | 日次backup、基本proof page、代表post保全、再起動チェックリスト | v0本命。原価上限を必ず設定する。 |
| Pro | 2,980円 | 仕事用X / 高頻度発信者 / サロン・講座販売者 | 優先同期、限定公開proof、外部リンク導線、月次保全レポート | 当初の3,000円案をここへ寄せる。 |
| Concierge検証 | 4,980円 | X停止が売上損失に直結する人 | 手動再起動支援、告知文テンプレ、優先サポート | 自動投稿・自動DMはしない。手動支援として検証する。 |
| Team検証 | 9,800円以上 | 小規模チーム / 複数アカウント運営 | 複数アカウント、監査ログ、担当者管理 | v0では後回し。要望が出たら個別見積もり。 |

## v0で検証する質問

1. Xアカウントが1週間使えなくなった場合、売上・集客・信用にどれくらい影響するか。
2. 「過去投稿を保存できる」だけなら、月いくらまで払えるか。
3. 「停止時に見せられる証明ページ」があるなら、月いくらまで払えるか。
4. 再開用プロフィール、代表投稿、外部リンク、連絡先を1ページにまとめる機能に価値を感じるか。
5. 初回にX公式archiveをアップロードしてもよいか、OAuthだけで完結したいか。
6. 1,980円と2,980円の差がある場合、日次同期、限定公開proof、優先サポート、月次レポートのどれが決め手になるか。
7. 停止後に手動で復旧/移行文面を作る支援があるなら、単発または月額でいくらまで払えるか。
8. 支払い理由は「データ保存」「停止/凍結への保険」「ファンへの連絡導線」「仕事の信用維持」のどれが一番近いか。

## PM判断

- 初期LPでは「成人向け」「政治」などセンシティブ属性を前面に出さない。営業・ヒアリング上の高反応セグメントとして扱う。
- 表現は「凍結回避」ではなく「事前バックアップ」「本人性の証明」「再起動導線」「仕事用アカウント保険」に寄せる。
- `follows.read`、DM、write系scope、自動投稿、自動DM、自動follow/unfollowはv0から外す。
- 価格検証は1,980円を本命、2,980円をPro、4,980円を手動支援つき検証枠にする。
