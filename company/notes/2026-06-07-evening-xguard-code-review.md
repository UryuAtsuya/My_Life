---
date: "2026-06-07"
project: "xguard"
type: evening-code-review
status: completed-with-blockers
---

# 2026-06-07 XGuard 夜コードレビュー

## completed

- システム日付を `2026-06-07 08:17:06 JST (+0900)` と確認した。
- 今日の正本を `/Users/uryuatsuya/XGuard/xguard`、GitHub反映先を `UryuAtsuya/Xguard` `origin/main` として確認した。
- サブエージェントを実利用した。Review agent、Verification agent、Documentation/Sync agentを並行起動し、Coordinatorが最終判断、commit、push、MyLife同期を担当した。
- Implementation agent相当の作業はCoordinatorが実施した。夜間に閉じられる小修正として、既存の3ファイル差分を検証し、XGuard `9ac4f2f Add proof visibility management route` を作成した。
- `9ac4f2f` は `git push origin main` で `UryuAtsuya/Xguard` へpush済み。push出力は `b03d9c8..9ac4f2f main -> main`。
- その後、Implementation agentの追加差分としてowner-only `PATCH /api/recovery/:runId/proof/visibility` まで `9ac4f2f` として反映済み。
- backup / proof APIの認証済みowner境界、proof private default、private / revoked proofの404拒否、API spec更新を確認した。

## unfinished

- 実Supabase/Postgres integration testは未完。`RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` 実行ではDB URL / `psql` 条件不足で対象テストがskipされた。
- `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` の商用release gate更新は未完。
- OAuth configured modeはまだ実X token exchangeを行わず、正しい `state` と任意 `code` でprototype sessionを発行する。production release blockerとして残す。
- proof visibility management endpoint は `9ac4f2f` に含まれ、tracked差分はない。
- `InMemoryOAuthStateRepository` はprototype用。multi-instance / restart / serverlessでは共有永続storeへ置換が必要。
- `output/playwright/` 配下の未追跡ファイルは残存。今回も触っていない。
- `git ls-remote origin refs/heads/main` は夜の再確認時にDNS失敗したため、live remote再読込は未完。ただし直前の `git push origin main` は成功した。

## findings

- P0: OAuth configured modeが実X token exchangeなしでsessionを発行する。このままproductionへ出すと、X側で発行されたcodeの検証なしに `fixtureAccount` のsessionを作れる。configured modeではtoken endpoint交換とsubject/account検証が完了するまでsession発行を禁止する。
- P1: 実Supabase/Postgresで `service_role`、ownership、同一Xアカウント、存在しない `backup_run`、`x_account_id` 必須、負値、月次上限超過を実証できていない。
- P1: cost/compliance gateが文書・運用上のNo-Goに留まり、CIまたはruntime configで機械的にreleaseを止める仕組みが未完。
- P1: OAuth state storeがin-memoryのため、複数instanceやrestartでstate consumeの一貫性が崩れる。
- P2: proof visibilityを通常APIで更新するowner-only routeは `9ac4f2f` で実装済み。残りは監査/compliance event記録。

## fixes applied

- `backend/src/app.ts`: backup作成時のproof visibilityを `"public"` から `"private"` へ変更した。
- `backend/src/__tests__/backupProofAuth.test.ts`: private default、public proof token非漏洩、private / revoked 404拒否のテストを整理した。
- `docs/API_SPEC.md`: backup / proof endpointの `Authorization: Bearer <sessionToken>` とprivate / revoked 404境界を明記した。
- 追加実装: owner-only `PATCH /api/recovery/:runId/proof/visibility`、unlisted/public/revoked更新、revoked後の再公開409、拒否テストを追加した。

## proposed fixes

1. OAuth configured modeで、X token endpointへPKCE verifier付きで交換し、取得tokenのsubject/account検証後だけsessionを発行する。mock callback/session発行はproductionで起動禁止にする。
2. OAuth state repositoryをSupabaseまたはRedisへ移し、TTL付きatomic consumeとuser intent紐付けを実装する。
3. 実Supabase/Postgres integration testをCIまたは実DB接続環境で必須化する。
4. `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` を更新し、pricing confirmed、spending limit、compliance revocation readyをCI/runtime gateにする。
5. proof visibility endpointに監査/compliance event記録を追加する。

## verification

- `date '+%Y-%m-%d %H:%M:%S %Z (%z)'` -> `2026-06-07 08:17:06 JST (+0900)`。
- `git status --short --branch` in XGuard -> 変更前は tracked 3ファイル差分、変更後は未追跡 `output/playwright/` のみ。
- `git diff --check && git diff --cached --check` -> pass。
- `npx tsc -p tsconfig.json --noEmit` -> pass。
- `CODEX_SANDBOX=1 npx vitest run --configLoader runner backend/src/__tests__/backupProofAuth.test.ts` -> 1 file passed、8 tests passed。
- Verification agent: `npm run test` -> 8 files passed / 1 skipped、62 tests passed / 4 skipped。
- `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1 npx vitest run --configLoader runner backend/src/__tests__/supabaseSqlApiUsageLedger.integration.test.ts` -> 1 file skipped、2 tests skipped。DB URL / `psql` 条件不足。
- `CODEX_SANDBOX=1 npm run check` -> `build:api` の `dist/backend/...` 書き込み `EPERM` で失敗。コード失敗ではなく権限blocker。
- `git push origin main` -> pass。`9ac4f2f` を `UryuAtsuya/Xguard` `main` へpush。
- `git ls-remote origin refs/heads/main` -> `Could not resolve host: github.com`。push後のlive再読込はDNS blocker。
- 追加差分検証: `git diff --check`, `git diff --cached --check`, `npx tsc -p tsconfig.json --noEmit`, targeted `backupProofAuth.test.ts` -> pass。targetedは1 file / 11 tests passed。

## tomorrow handoff

1. OAuth configured modeの実token exchange + subject/account検証 + production mock callback禁止を閉じる。
2. 実Supabase/Postgres integration testをDB URL / `psql` ありで実行する。
3. `docs/API_COST_MODEL.md` / `docs/COMPLIANCE.md` release gateをCI/runtime gateへ落とす。

## subagent findings

- Review agent: 実利用。P0としてconfigured OAuth callbackの実token exchange未実装を指摘。P1はin-memory state store、実DB検証skip、cost/compliance gate未機械化。P2はproof visibility管理API不足。
- Verification agent: 実利用。コード失敗なし。`npm run test` はpass。`npm run check` は `dist/backend` 書き込み `EPERM`、`git ls-remote` はDNS失敗。
- Documentation/Sync agent: 実利用。6/7 closeout記録不足、6/8 TODO新規作成、READMEの古い `d5aa75e` 表記更新、PM ticketとactive projects更新を指摘。
- Implementation agent: proof visibility management endpoint を `9ac4f2f` として反映。Coordinator最終確認で `HEAD=origin/main=9ac4f2f`、tracked差分なし。
