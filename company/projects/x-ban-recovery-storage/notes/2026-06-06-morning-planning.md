---
date: "2026-06-06"
project: "xguard"
type: "morning-planning"
status: "ready-for-midday"
---

# 2026-06-06 XGuard 朝会

## 今日の方針

XGuardを事業最優先にする。OAuth `state` / S256 PKCE は `2b96993 Add OAuth state and PKCE guard` で正本に反映済みとして扱い、production release No-Goの主因を backup / proof APIの認証・所有権・visibility/revocation、実Supabase/Postgres検証、cost/compliance release gate に絞る。

## 今日のTop 3

1. backup / proof APIへ認証、user ownership、proof visibility/revocation境界を追加し、他user・private・revoked proof拒否テストを入れる。
2. 実Supabase/Postgresで `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` を実行し、role・ownership・同一Xアカウント・存在しない `backup_run`・`x_account_id` 必須・負値・月次上限超過を確認する。
3. `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` に、pay-per-usage、通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、24時間削除SLA、API access終了時全削除runbook、Enterprise確認を反映する。

## 昼の実装スコープ

- ディレクトリ: `/Users/uryuatsuya/XGuard/xguard`
- fallback: 指定パスが書き込み不可なら `/private/tmp/xguard-midday-2026-06-06`
- 起点: `2b96993 Add OAuth state and PKCE guard`
- production codeはMyLife Vaultに置かない。
- 未追跡 `output/playwright/` は触る前に生成物かレビュー成果物か確認する。

## 変更候補

- `backend/src/app.ts`: backup/proof APIで認証済みuserを要求する。
- backend route tests: 他user backup/proof、private proof、revoked proof、存在しないrun idを拒否する。
- proof DTO service/repository: proof公開可否、owner、revocationをDTO境界で強制する。
- docs: `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` をrelease gateとして更新する。

## サブエージェント担当案

| 担当 | 役割 | 完了条件 |
|---|---|---|
| Implementation agent | backup/proof auth boundaryとownership checkを実装する。 | 他user/private/revoked proofがAPIで拒否される。 |
| Review agent | 認証抜け、IDOR、token漏洩、private/protected content漏洩、BAN回避表現をレビューする。 | P0/P1がなければ次へ進める。 |
| Verification agent | `tsc`、targeted Vitest、可能なら実Supabase test、`npm run check` を実行する。 | 実行結果と環境blockerを分けて記録する。 |
| Documentation/Sync agent | cost/compliance docs、PM ticket、MyLife引き継ぎを更新する。 | XGuard commit/pushとMyLife commit/pushを分けて報告する。 |

## No-Go 条件

- proof pageが他ユーザーのbackup/proofを読める。
- private/revoked proofが公開DTOとして返る。
- raw X API payloadやtoken materialがAPIレスポンスに混ざる。
- X Content削除/非公開/停止への24時間追従方針がdocsにない。
- X API利用が商用/多ユーザーへ進む前にEnterprise適用要否が未確認。

## 17:00 再実行時点の後続スコープ

同日昼の実装でTop 1のbackup / proof所有権境界は `d5aa75e Guard backup proof ownership boundaries` まで完了した。以後の実装・検証スコープは以下へ更新する。

- ディレクトリ: `/private/tmp/xguard-midday-2026-06-06-1331` の `d5aa75e` をpush候補、正本確認は `/Users/uryuatsuya/XGuard/xguard`。
- まず `git fetch origin main` または `git ls-remote origin refs/heads/main` でremote先行分を確認する。DNSや `.git/FETCH_HEAD` 権限で失敗した場合は、push不可理由を記録して止める。
- 実装残: Supabase Auth/JWT + DB ownershipでprototype user headerを置換する。prototype headerはproduction認証として扱わない。
- 検証残: `RUN_SUPABASE_SQL_INTEGRATION_TESTS=1` に必要な実DB URL / `psql` を満たしてusage ledger integration testを走らせる。
- docs残: `docs/API_COST_MODEL.md` と `docs/COMPLIANCE.md` にX API通常read単価、`Owned Reads` 非適用、Usage endpoint、spending limit、24時間削除SLA、API access終了時全削除runbookを反映する。

| 担当 | 次の役割 | 完了条件 |
|---|---|---|
| Implementation agent | `d5aa75e` のpush前remote確認、必要ならrebase/cherry-pick、Supabase Auth/JWT置換設計。 | force pushなしでremoteへ反映、またはblocker記録。 |
| Review agent | prototype header、本番auth、IDOR、private/revoked proof、raw payload/token漏洩を再レビュー。 | P0/P1なし、P2はPM ticketへ残す。 |
| Verification agent | `npm run check`、targeted Vitest、実Supabase/Postgres test、diff checkを再実行。 | pass/skip/blockerを分けて証跡化。 |
| Documentation/Sync agent | cost/compliance docs、PM ticket、MyLife TODO/decision/memoryを同期。 | XGuard push状態とMyLife push状態を分けて報告。 |
