---
date: "2026-06-04"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-06-04 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。昼は最初に `/api/x/oauth/status` の `deployment_diagnostic` 無認証公開を閉じ、その後に実Supabase/Postgres integration test、OAuth `state` / S256 PKCE / callback validationを進める。

調査上、`Owned Reads` はdeveloper app owner本人に限定されるため、複数顧客向けXGuardの原価モデルには使わない。公開有料ローンチ前にEnterprise適用要否と、X Content削除追従の24時間SLAを閉じる。

## 朝の確認結果

- 日付確認: `2026-06-04 08:02:28 JST`
- 指定実装パス: `/Users/uryuatsuya/XGuard/xguard`
- 指定パス状態: `exists=yes`, `writable=no`, `main...origin/main`
- local `HEAD` / local `origin/main`: `6024667 Restrict production CORS origins`
- `git ls-remote origin refs/heads/main`: `Could not resolve host: github.com`
- `git fetch origin main`: `.git/FETCH_HEAD: Operation not permitted`
- MyLife repo: `main...origin/main`。既存の未追跡 `.obsidian/`, `Ideas/`, `Projects/`, `memo/` は触らない。

## 今日のTop 3

1. `6024667` を正として、`X_OAUTH_STATUS_EXPOSURE=deployment_diagnostic` 有効時の `/api/x/oauth/status` をheader secret、admin auth、またはprivate health checkへ限定し、HTTP境界テストを追加する。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role、ownership、同一Xアカウント、`x_account_id` 必須、存在しない `backup_run`、月次上限、負値拒否を確認する。
3. OAuth `state` / S256 PKCE / callback validation / token schema契約を閉じ、通常read単価、Enterprise適用要否、24時間削除SLAをdocsへ反映する。

## 昼の実装スコープ

### 作業ディレクトリ

- 第一候補: `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-04`
- 実装コードを置かない場所: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

### 最初のゲート

1. `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で `6024667` を再確認する。
2. `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行する。失敗時は理由を記録し、force pushしない。
3. working treeがdirtyなら差分を読み、無関係な変更を巻き戻さない。
4. 書き込み不可なら `/private/tmp/xguard-midday-2026-06-04` を使い、Vaultへproduction codeを置かない。

### 作成・変更候補

- `backend/src/config/runtimeConfig.ts`: 診断endpoint用secretまたはprivate-only設定を追加する。
- `backend/src/app.ts`: `deployment_diagnostic` 有効時にも認証・secret gateを要求する。次のscopeで一回限り `state` とS256 PKCEを導入する。
- `backend/src/__tests__/api.test.ts`: `/api/x/oauth/status` の404、拒否、許可をHTTP境界で確認する。
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`: 実DB role / ownership / limit拒否条件を確認する。
- `supabase/schema.sql`: 実DB testで判明した不足だけを修正する。
- `docs/API_SPEC.md`, `docs/DEPLOY.md`: 診断endpoint制限、OAuth callback、安全なenv運用を更新する。
- `docs/API_COST_MODEL.md`: 通常read単価、`Owned Reads` 非適用、Enterprise確認、Usage / spending limitを更新する。
- `docs/COMPLIANCE.md`: 24時間削除・変更追従とAPI access終了時の全削除runbookを更新する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx vitest run --configLoader runner backend/src/__tests__/api.test.ts`
- `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`
- `npm run test`
- `npm run build`
- `npm run check`
- stage後 `git diff --cached --check`
- GitHub接続復旧時は `git fetch origin main`, divergence確認、`git push origin main`

## サブエージェント担当案

| Agent | 担当 | 成果物 |
|---|---|---|
| Implementation agent | 最初に診断endpointの認証・secret gateとHTTP境界テスト。完了後にOAuth state / S256 PKCE / callback validationへ進む | 小さく分離したXGuard commit候補 |
| Review agent | 診断情報漏えい、OAuth replay/CSRF、token保存、service_role境界、削除追従SLAをP0/P1/P2でレビュー | findingsとrelease gate判断 |
| Verification agent | targeted Vitest、実Supabase test、`tsc`、build、全test、diff、remote状態を確認 | pass/fail、未実施理由、再現command |
| Documentation/Sync agent | XGuard docs、MyLife research/decision/TODO/PM ticket、automation memoryを同期 | XGuardとMyLifeを分けたcommit/push記録 |

## 判断

- `follows.read`, DM/write/follow系scopeは追加しない。
- `Owned Reads` を複数顧客向け原価へ使わない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- production codeは朝runで実装しない。
