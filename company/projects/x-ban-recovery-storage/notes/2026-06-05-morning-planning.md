---
date: "2026-06-05"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-06-05 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。診断endpointの無認証公開は `394a3c3 Add OAuth diagnostic HTTP boundary tests` で解消済みなので、昼はOAuth configured modeのCSRF/replay防止を最初に閉じ、次にbackup / proof APIの認証・所有権境界、実Supabase/Postgres検証、cost/compliance docs反映へ進む。

市場シグナル上は、ban waveやanti-bot誤検知への不安が続いている。ただしXGuardはBAN回避、自動DM、自動follow、自動投稿へ寄せず、本人の事前backup、証明ページ、手動再起動支援に固定する。

## 朝の確認結果

- 日付確認: `2026-06-05 08:05:28 JST`
- 指定実装パス: `/Users/uryuatsuya/XGuard/xguard`
- 指定パス状態: `exists=yes`, `writable=no`, `main...origin/main`
- local `HEAD` / local `origin/main`: `394a3c3 Add OAuth diagnostic HTTP boundary tests`
- `git ls-remote origin refs/heads/main`: `Could not resolve host: github.com`
- `git fetch origin main`: `.git/FETCH_HEAD: Operation not permitted`
- MyLife repo: `main...origin/main`。既存の未追跡 `.obsidian/`, `Ideas/`, `Projects/`, `memo/` は触らない。

## 今日のTop 3

1. `394a3c3` を起点に、OAuth configured modeへ一回限り `state`、S256 PKCE、callback validation、TTL、replay防止を実装し、forged / expired / replay callbackテストを追加する。
2. backup / proof APIへ認証、user ownership、proof visibility/revocation境界を追加し、他user・非公開・revoked proofの拒否テストを入れる。
3. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、`docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` に通常read単価、spending limit、24時間削除SLA、API access終了時全削除runbookを反映する。

## 昼の実装スコープ

### 作業ディレクトリ

- 第一候補: `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可の場合: `/private/tmp/xguard-midday-2026-06-05`
- 実装コードを置かない場所: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

### 最初のゲート

1. `git status --short --branch`, `git rev-parse --short HEAD`, `git rev-parse --short origin/main` で `394a3c3` を再確認する。
2. `git ls-remote origin refs/heads/main` と `git fetch origin main` を再試行する。失敗時は理由を記録し、force pushしない。
3. working treeがdirtyなら差分を読み、無関係な変更を巻き戻さない。
4. 書き込み不可なら `/private/tmp/xguard-midday-2026-06-05` を使い、Vaultへproduction codeを置かない。

### 作成・変更候補

- `backend/src/config/runtimeConfig.ts`: OAuth state TTL、PKCE verifier長、callback URL検証に必要なruntime設定を追加する。
- `backend/src/app.ts`: `/api/x/oauth/start` とcallbackで一回限り `state` / `code_verifier` を発行・保存・照合し、expired / replay / forged callbackを拒否する。
- `backend/src/repositories/*`: OAuth state repositoryまたはsession storeを追加し、token materialをfrontendへ返さない。
- `backend/src/__tests__/api.test.ts`: OAuth start/callbackのS256 PKCE、state mismatch、expired、replay、scope維持をHTTP境界で確認する。
- `backend/src/services/*`: backup / proof APIのuser ownership、visibility、revocation境界をservice層で固定する。
- `backend/src/__tests__/*`: 他user backup/proof拒否、revoked proof拒否、private proof拒否を追加する。
- `backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts`: 実DB role / ownership / 同一Xアカウント / limit拒否条件を確認する。
- `docs/API_COST_MODEL.md`: 通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、月次原価停止を更新する。
- `docs/COMPLIANCE.md`: 24時間削除・変更追従、API access終了時の全削除runbook、Enterprise確認gateを更新する。

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
| Implementation agent | OAuth one-time state / S256 PKCE / callback validationを先に実装し、次にbackup/proof所有権境界へ進む | 小さく分離したXGuard commit候補 |
| Review agent | OAuth CSRF/replay、token保存、backup/proof所有権、proof visibility/revocation、X Content削除SLAをP0/P1/P2でレビュー | findingsとrelease gate判断 |
| Verification agent | targeted Vitest、実Supabase test、`tsc`、build、全test、diff、remote状態を確認 | pass/fail、未実施理由、再現command |
| Documentation/Sync agent | XGuard docs、MyLife research/decision/TODO/PM ticket、automation memoryを同期 | XGuardとMyLifeを分けたcommit/push記録 |

## 判断

- `follows.read`, DM/write/follow系scopeは追加しない。
- `Owned Reads` を複数顧客向け原価へ使わない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- production codeは朝runで実装しない。
