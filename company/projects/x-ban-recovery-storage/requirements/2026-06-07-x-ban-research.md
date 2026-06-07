---
date: "2026-06-07"
project: "xguard"
type: "morning-research"
status: "completed"
---

# 2026-06-07 XGuard 朝調査

## 結論

XGuard は今日も事業最優先。backup / proof API の所有権境界と docs release gate は前進済みだが、実装 repo の現在状態では `7e33e9f Guard production OAuth callback boundary` が local `main` にあり、local tracking `origin/main` より `ahead 1`。まずこの OAuth production boundary commit を remote へ安全に反映する。

production release は No-Go 継続。主な残件は、実 X token exchange の live 疎通証跡、実 Supabase/Postgres integration test、cost/compliance gate の CI/runtime 化、未追跡 `output/playwright/` の扱い判断。

## XGuard 正本確認

- 正本: `/Users/uryuatsuya/XGuard/xguard`
- GitHub: `UryuAtsuya/Xguard`
- 現在の local `HEAD`: `7e33e9f Guard production OAuth callback boundary`
- local 状態: `main...origin/main [ahead 1]`
- local tracking `origin/main`: `9ac4f2f Add proof visibility management route`
- 未追跡: `output/playwright/` 配下のみ。今日の Top 3 では触らない。
- 注意: 6/7 昼 run の `c4403d8 Document XGuard release gates` は push 成功記録がある一方、現 canonical checkout の local tracking には未反映に見える。昼 run は、push前に remote を確認し、`c4403d8` が remote に存在する場合は `7e33e9f` と競合させず統合する。

## 公式API / 規約ソース

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| X API Pricing | https://docs.x.com/x-api/getting-started/pricing | X API は credit-based の pay-per-usage。Post read は `$0.005/resource`、User read は `$0.010/resource`。spending limit と Usage endpoint も案内されている。 | `1,980円 / 2,980円 / 4,980円` の価格仮説は、通常 read 単価、日次同期件数、月次上限前停止を前提に再計算する。 |
| X API Pricing - Owned Reads | https://docs.x.com/x-api/getting-started/pricing | `Owned Reads` は認証 user と `{id}` が一致し、その user が developer app owner の場合に低単価対象。 | 複数顧客 SaaS の主原価として使わない。通常 read 単価を基準にする判断を維持する。 |
| X API Usage | https://docs.x.com/x-api/usage/introduction | `GET /2/usage/tweets` で app 単位の日別 Post 消費を追跡でき、pay-per-usage plan には月間 Post read cap がある。 | XGuard の usage ledger と Developer Console 実値照合、80%停止、月次上限前停止を release gate にする。 |
| X API Rate Limits | https://docs.x.com/x-api/fundamentals/rate-limits | endpoint ごとに per-app / per-user の rate limit があり、429 と `x-rate-limit-*` header で制御する。DM / follow 系にも別制限がある。 | backup worker は 429、token失効、403/404、BAN候補を分離し、自動 DM / follow / posting を v0 へ入れない。 |
| X Developer Policy | https://docs.x.com/developer-terms/policy | X Content の表示・保存・再配布・削除追従・同意・DM/private content の扱いを制限する。削除/変更/非公開/停止への追従が必要。 | proof page は raw payload 公開ではなく public DTO 限定にし、private / revoked / deleted content を出さない。 |
| X Developer Agreement | https://docs.x.com/developer-terms/agreement | X Content が削除・非公開・停止・変更された場合、合理的に速やかに、必要時は 24 時間以内に削除または変更する義務がある。 | `docs/COMPLIANCE.md` の 24時間 SLA と API access 終了時全削除 runbook を実装 gate へ落とす。 |
| X Developer Guidelines | https://docs.x.com/developer-guidelines | content deletion、API access termination、automation、data handling の実務ガイドが整理されている。 | API access 終了時削除と off-X matching 同意を、課金開始前の必須チェックにする。 |

## 競合 / 隣接ツール

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| Circleboom Plans and Pricing | https://circleboom.com/plans-and-pricing | X/Twitter account analytics、tweet scheduler、削除・管理系機能を含む social management pricing。 | XGuard は growth/automation 管理ツールではなく、read-only 保全・proof・再起動支援として差別化する。 |
| Circleboom Help: Plans and Pricing | https://help.circleboom.com/twitter/getting-started/plans-and-pricing-circleboom-twitter | Twitter management の free / delete / pro / plus / enterprise 系の多段階価格を案内。 | XGuard の `2,980円 Pro` は管理ツール市場の下限から中間に入る。backup 単体では弱く、proof と再起動支援が必要。 |
| Twibird Pricing | https://twibird.com/pricing | X likes/bookmarks sync、CSV / Notion export、cloud tweet backup を月額サブスクで提供。 | backup / export 単体の支払期待値は低め。Personal は少量同期、Proof、restore checklist まで含める必要がある。 |
| Backread | https://www.backread.app/ | X bookmarks の同期・分類・Markdown export 系の個人向けツール。 | 「保存」だけでは安価な個人ツールと比較される。XGuard は account continuity と本人性 proof を中心にする。 |
| FeedMirror | https://feedmirror.app/ | social media content の backup を official API 前提で訴求する隣接サービス。 | XGuard も official API / compliance-first を前面に出し、スクレイピング型に見せない。 |

## 市場シグナル

| ソース | URL | 要約 | XGuardで重要な理由 |
|---|---|---|---|
| TechCrunch: X creator revenue-sharing backlash | https://techcrunch.com/2026/03/25/elon-musk-pauses-changes-to-xs-creator-revenue-sharing-program-after-backlash/ | X の creator monetization ルール変更が反発を受け、一時停止された。 | X 依存 creator は platform ルール変更に左右される。XGuard の「仕事用Xの保険」訴求と相性がある。 |
| TechCrunch: X Communities shutdown | https://techcrunch.com/2026/04/23/x-is-shutting-down-communities-because-of-low-usage-and-lots-of-spam/ | X Communities が低利用・spam 問題で終了方向になった。 | platform 内の機能や community 導線は永続前提にできない。外部 proof / migration 導線の価値がある。 |
| Forbes: X cracks down on revenue share gaming | https://www.forbes.com/sites/conormurray/2026/05/29/x-cracks-down-on-stolen-content-demonetizes-major-account-for-gaming-monetization-system/ | X が monetization system を悪用する大規模アカウントを取り締まった事例。 | XGuard は growth automation や収益操作ではなく、規約順守の保全・証跡サービスとして表現する。 |
| Reddit: X account suspended for inauthentic behavior | https://www.reddit.com/r/twitterhelp/comments/1sfh5x1/x_account_suspended_for_inauthentic_behavior/ | 2026年にも `inauthentic behavior` 停止への不安・appeal 体験が投稿されている。 | 匿名投稿なので補助証拠扱い。ただし停止不安の現在性は高く、Free 診断の需要仮説になる。 |
| Reddit: mass account suspensions April 2026 | https://www.reddit.com/r/twitterhelp/comments/1slz3ej/the_truth_behind_x_mass_suspensions_april_2026/ | 2026年4月の mass suspension 体験談・復旧/未復旧報告がまとまっている。 | LP の主証拠にはしないが、初期ヒアリング対象の不安パターン抽出に使える。 |

## API / コンプライアンス判断

- v0 scope は `tweet.read`, `users.read`, `offline.access` のまま維持する。
- 自動 DM、自動 follow/unfollow、自動投稿、bulk outreach、BAN 回避導線は作らない。
- proof page は private default、owner-only visibility update、revoked / private / deleted content 404 を維持する。
- `Owned Reads` は複数顧客 SaaS の原価前提にしない。
- Usage endpoint、Developer Console、内部 usage ledger の差分を照合し、80%時点で停止または手動承認へ切り替える。
- OAuth configured mode は、実 token exchange と subject/account 検証が通るまでは production session を発行しない。
- 実 Supabase/Postgres integration test は、DB URL / `psql` 条件が揃う環境で必ず実行する。

## 今日のPM判断

1. Top 1 は `7e33e9f Guard production OAuth callback boundary` の remote 反映と、`c4403d8` との remote 整合確認。
2. Top 2 は実 X token exchange の疎通証跡、または live credentials がない場合の production mock callback 禁止 gate の明文化。
3. Top 3 は実 Supabase/Postgres integration test の実行環境確保と、cost/compliance gate の CI/runtime 化設計。

## 昼実装への引き継ぎ

- 実装場所: `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-07` または新しい `/private/tmp/xguard-midday-2026-06-07-*`
- 最初に確認すること:
  - `git status --short --branch`
  - `git log --oneline --decorate -5`
  - `git ls-remote origin refs/heads/main`
  - `git fetch origin main`
  - `origin/main..HEAD` と `HEAD..origin/main`
- 変更候補:
  - `backend/src/app.ts`
  - `backend/src/config/runtimeConfig.ts`
  - `backend/src/__tests__/api.test.ts`
  - `docs/API_SPEC.md`
  - `docs/DEPLOY.md`
  - `docs/API_COST_MODEL.md`
  - `docs/COMPLIANCE.md`
- 検証:
  - `git diff --check`
  - `npx tsc -p tsconfig.json --noEmit`
  - OAuth callback targeted Vitest
  - `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`
  - 可能なら `npm run check`
- サブエージェント分担:
  - Implementation agent: remote 整合確認後、`7e33e9f` の push / merge / cherry-pick 判断と OAuth boundary の不足修正。
  - Review agent: OAuth configured mode、session発行条件、mock callback production 禁止、proof visibility、raw payload漏洩を P0/P1/P2 で確認。
  - Verification agent: diff check、tsc、targeted Vitest、Supabase integration test、push後の remote hash 確認。
  - Documentation/Sync agent: MyLife の TODO、PM ticket、project README、active projects、decision を更新し、XGuard と MyLife commit hash を分けて記録。
