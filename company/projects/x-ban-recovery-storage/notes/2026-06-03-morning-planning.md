---
date: "2026-06-03"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-06-03 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。note、Today Board、その他webサービス改善は、XGuardのlive remote確認、実Supabase/Postgres integration test、OAuth configured mode安全化、Developer Console原価確認が進むまで後回しにする。

朝runではproduction codeを実装しない。昼runは `/Users/uryuatsuya/XGuard/xguard` を正本として扱い、書けない場合のみ `/private/tmp/xguard-midday-2026-06-03` を使う。Vaultへ実装コードは置かない。

## 朝の確認結果

- 日付確認: `2026-06-03 08:24:09 JST`
- 指定実装パス: `/Users/uryuatsuya/XGuard/xguard`
- 指定パス状態: `exists=yes`, `writable=no`, `main...origin/main`
- local `HEAD`: `95e6392`
- local `origin/main`: `95e6392`
- MyLife repo: `main...origin/main`。未追跡の `.obsidian/`, `Ideas/`, `Projects/`, `memo/` などは既存の無関係変更として触らない。

## 今日のTop 3

1. `/Users/uryuatsuya/XGuard/xguard` の `HEAD=origin/main=95e6392` をlive GitHubで再確認し、`git fetch origin main` / `git ls-remote origin refs/heads/main` のDNS・`.git/FETCH_HEAD` blockerを解消する。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`service_role` 実行、`authenticated` 拒否、ownership、同一Xアカウント整合性、存在しない `backup_run`、`x_account_id` 必須、月次上限超過、負値拒否を確認する。
3. OAuth configured modeの `state` / S256 PKCE / callback validation、token repositoryとSupabase schema契約、Developer Console原価確認を進める。

## 昼の実装スコープ

### 作業ディレクトリ

- 第一候補: `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可またはfetch不可の場合: `/private/tmp/xguard-midday-2026-06-03`
- 実装コードを置かない場所: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

### 最初のゲート

1. `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で指定パスを再確認する。
2. `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行する。失敗した場合は理由を昼メモに残し、force pushはしない。
3. working treeがdirtyなら差分を読む。無関係な変更は巻き戻さず、必要なら一時cloneへ取り込む。
4. `95e6392` がlive remoteと一致したら、残る実装gateへ進む。一致しない場合はremote正本を優先し、rebase/cherry-pickで統合する。

### 作成・変更候補

- `supabase/schema.sql`: 実DB integration testで判明したgrant / revoke / ownership / check constraint不足があれば修正。
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`: `service_role` / `authenticated` のrole別RPC、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を実DBで確認する。
- OAuth route / runtime config: `state` を署名付き一回限り値へ変更し、PKCEをS256に固定し、callbackで `state` と `code_verifier` を照合する。
- token repository / Supabase schema: `access_token`, `refresh_token`, `scope`, `expires_at`, `revoked_at` の保存契約を一本化する。
- `docs/API_COST_MODEL.md`: Developer Console実値、spending limit、Usage endpoint、Owned Reads条件の証跡を更新。
- `docs/DEPLOY.md`: 実Supabase migration testの実行手順と必要envを更新。
- `docs/API_SPEC.md`: `/api/x/oauth/status` の本番公開条件をadmin/deployment-only前提へ補足する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- targeted Vitest
- `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` 付きintegration test
- `npm run test`
- `npm run build`
- `npm run check`
- stage後 `git diff --cached --check`
- GitHub接続が復旧していれば `git fetch origin main`, `git status --short --branch`, `git push origin main`

## サブエージェント担当案

| Agent | 担当 | 成果物 |
|---|---|---|
| Implementation agent | live remote確認、実Supabase/Postgres test、OAuth state / S256 PKCE / callback validation、token schema整合 | XGuard repoのcommit候補、検証ログ |
| Review agent | service_role境界、OAuth callback、token保存契約、proof DTO削除追従、secret非表示、`/api/x/oauth/status` production制御をレビュー | P0/P1/P2 findings |
| Verification agent | `tsc`, targeted Vitest, integration test, `npm run test`, `npm run build`, `npm run check`, `git diff --check`, remote/fetch/push確認 | pass/failと失敗理由 |
| Documentation/Sync agent | XGuard docs、MyLife project notes、PM ticket、decisions、TODO、automation memory同期 | MyLife commit/push |

## 判断

- `follows.read`, DM/write/follow系scopeは今日も追加しない。
- `Owned Reads` は安いが、第三者ユーザー向けSaaS適用確認まで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線は作らない。
- `/api/x/oauth/status` はproductionでadmin-onlyまたはdeployment-onlyへ寄せるまで完了扱いにしない。
