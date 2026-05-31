---
date: "2026-06-01"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-06-01 XGuard 朝会

## 今日の結論

XGuardを今日の事業最優先にする。note、Today Board、その他webサービス改善は、XGuardのlive remote確認、実Supabase/Postgres migration test、Developer Console原価確認が進むまで後回しにする。

朝runではproduction codeを実装しない。昼runは `/Users/uryuatsuya/XGuard/xguard` を正本として扱い、書けない場合のみ `/private/tmp/xguard-midday-2026-06-01` を使う。Vaultへ実装コードは置かない。

## 朝の確認結果

- 日付確認: `2026-06-01 08:01:14 JST (+0900)`
- 指定実装パス: `/Users/uryuatsuya/XGuard/xguard`
- 指定パス状態: `exists=yes`, `writable=no`, `main...origin/main`
- local `HEAD`: `2655267 Filter revoked tweet snapshots from proof DTO`
- local `origin/main`: `2655267`
- `git ls-remote origin refs/heads/main`: `Could not resolve host: github.com`
- `git fetch origin main`: `.git/FETCH_HEAD: Operation not permitted`
- MyLife repo: `main...origin/main`。未追跡の `.obsidian/`, `Ideas/`, `Projects/`, `memo/` は既存の無関係変更として触らない。

## 今日のTop 3

1. GitHub DNS/権限復旧後、`2655267` が `UryuAtsuya/Xguard` live remote `origin/main` と一致するか確認する。
2. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の権限境界と拒否条件を確認する。
3. Developer Consoleでendpoint別単価、credit/spending、Usage endpoint、Owned Reads条件を確認し、XGuard docsとcompany gateへ反映する。

## 昼の実装スコープ

### 作業ディレクトリ

- 第一候補: `/Users/uryuatsuya/XGuard/xguard`
- 書き込み不可またはfetch不可の場合: `/private/tmp/xguard-midday-2026-06-01`
- 実装コードを置かない場所: `/Users/uryuatsuya/Documents/ObsidianVault/MyLife`

### 作成・変更候補

- `docs/API_COST_MODEL.md`: Developer Console実値、spending limit、Usage endpoint、Owned Reads条件の証跡を更新。
- `docs/DEPLOY.md`: 実Supabase migration testの実行手順と必要envを更新。
- `docs/API_SPEC.md`: `/api/x/oauth/status` の本番公開条件をadmin/deployment-only route前提へ補足。
- `supabase/schema.sql`: migration testで判明したgrant / rejection条件の不足があれば修正。
- `backend/src/__tests__/...`: 実Supabase/Postgres境界を直接確認する最小テストまたは検証スクリプトを追加。ただしsecret値は記録しない。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- targeted Vitest
- `npm run check`
- stage後 `git diff --cached --check`
- GitHub接続が復旧していれば `git fetch origin main`, `git status --short --branch`, `git push origin main`

## サブエージェント担当案

| Agent | 担当 | 成果物 |
|---|---|---|
| Implementation agent | 実Supabase/Postgres migration test、必要ならgrant / validation修正、`docs/API_COST_MODEL.md` 更新 | XGuard repoのcommit候補、検証ログ |
| Review agent | `/api/x/oauth/status` の公開リスク、service_role境界、proof DTO削除追従、secret非表示をレビュー | P0/P1/P2 findings |
| Verification agent | `tsc`, targeted Vitest, `npm run check`, `git diff --check`, remote/fetch/push確認 | pass/failと失敗理由 |
| Documentation/Sync agent | XGuard docs、MyLife project notes、PM ticket、decisions、TODO、automation memory同期 | MyLife commit/push |

## 判断

- `follows.read`, DM/write/follow系scopeは今日も追加しない。
- `Owned Reads` は安いが、第三者ユーザー向けSaaS適用確認まで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線は作らない。
- `09ff660 Add OAuth status endpoint` は `2655267` 系列に必要差分がなければ破棄する。
