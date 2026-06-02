---
date: "2026-06-02"
project: "xguard"
type: evening-code-review
status: reviewed
---

# 2026-06-02 XGuard 夜レビュー

## Completed

- 日付を `2026-06-02 18:01:54 JST` と確認した。
- サブエージェントは実利用できた。Review agent、Verification agent、Documentation/Sync agentを分け、最終判断とMyLife同期はCoordinatorが担当した。Implementation agentは夜間の小修正対象がなく、起動しなかった。
- 正本は `/Users/uryuatsuya/XGuard/xguard`、計画・運用記録の正本は `/Users/uryuatsuya/Documents/ObsidianVault/MyLife/company/projects/x-ban-recovery-storage` と確認した。
- 昼runの `33cae26 Require X account for backup usage events` 相当は、夜run最終状態で指定パスの `95e6392 Merge remote-tracking branch 'origin/main'` に統合され、local `origin/main` と一致した。
- `backup_run_id` 付き usage event では `x_account_id` を必須にし、`backup_runs.x_account_id = p_x_account_id` を要求する方向性を維持した。

## Unfinished

- live GitHubの独立確認は未完了。`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`、`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- 実Supabase/Postgres integration test本体はDB credentialがなく未実行。
- OAuth configured modeの静的 `state`、plain/mock PKCE、callback未照合は未解消。
- token repositoryとSupabase schemaの保存契約一本化は未完了。
- Developer Console原価実値確認は未完了。

## Findings

- P0: なし。
- P1: `/api/x/oauth/status` が無認証で `mode`、`callbackUrl`、`clientSecretConfigured`、`missingEnv` を返す。本番構成の偵察情報になるため、production deploy前にadmin-onlyまたはdeployment-only health checkへ寄せる。
- P1: OAuth configured modeは `state` が静的で、PKCEがplain/mock、callbackで `state` / `code_verifier` を照合していない。実運用前にS256 PKCEと一回限りstateを入れる。
- P1: token repositoryは `access_token_ref` / `refresh_token_ref` 前提、Supabase schemaは `encrypted_access_token` / `encrypted_refresh_token` 前提で、保存契約がまだ一本化されていない。
- P2: 実DB integration testがcredentialなしでskipされるため、role/grant/RLS/check constraintの実証跡がない。
- P2: OAuth status route testがExpress内部構造を直接叩いている。`supertest` 経由のHTTP検証へ置き換える。
- P2: CORSが全許可のままなので、`APP_BASE_URL` またはallowlistへ寄せる。

## Fixes Applied

- 夜runではXGuard実装コードの追加修正は適用しなかった。指定パスは最終的に clean、`HEAD=origin/main=95e6392`。
- MyLife側のcloseout note、project note、TODO、decision、PM/project記録を更新した。

## Proposed Fixes

1. `/api/x/oauth/status` はproductionで404にするか、admin/internal tokenを必須にする。
2. OAuth startでS256 `code_challenge` と一回限り `state` を発行し、callbackで `state` と `code_verifier` を照合する。
3. `x_oauth_connections` の保存契約を、暗号化token列またはtoken ref列のどちらかに統一し、repository interfaceとschemaを一致させる。
4. `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` と実DB URLを使い、SQL boundaryをrole別に実証する。
5. OAuth status testを `request(createApp(config)).get("/api/x/oauth/status")` へ移す。

## Verification

- `git status --short --branch` in XGuard: `## main...origin/main`
- `git rev-parse HEAD` / `git rev-parse origin/main`: `95e63929e7ef5e3b984bdff6fe27adc4b794cd14`
- `git diff --check`: pass
- `git ls-files -u`: unmerged entryなし
- `npx tsc -p tsconfig.json --noEmit`: pass
- targeted Vitest: 3 files passed / 1 skipped、11 passed / 2 skipped
- `npm run test`: 7 files passed / 1 skipped、41 passed / 2 skipped
- `npm run build`: pass
- `npm run check`: `dist/backend/...` 上書きが `EPERM` で失敗。コード失敗ではなく権限ブロッカー。
- `git ls-remote origin refs/heads/main`: DNS失敗
- `git fetch origin main`: `.git/FETCH_HEAD` 書き込み不可で失敗

## Tomorrow Handoff

1. `HEAD=origin/main=95e6392` をlive GitHubで再確認し、fetch/ls-remote blockerを解消する。
2. 実Supabase/Postgres integration testをcredential付きで走らせる。
3. OAuth state / S256 PKCE / callback validation、token schema契約、Developer Console原価確認を進める。

## Subagent Findings

- Review agent: P0なし。P1は無認証 `/api/x/oauth/status`。P2はExpress内部構造依存test。
- Verification agent: `tsc`、build、testは通過。`npm run check` は `dist/` write `EPERM`。fetch/ls-remoteはDNSまたは権限でblocked。
- Documentation/Sync agent: closeout更新先と明日Top 3を提案。途中状態としてconflict疑いを報告したが、Coordinator最終確認では `git ls-files -u` は空、`git diff --check` もpass。
