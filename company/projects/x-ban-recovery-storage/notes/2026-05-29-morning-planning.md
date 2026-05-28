---
date: "2026-05-29"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-05-29 XGuard 朝計画

## 朝会結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定パスの最新状態と昨日の一時clone未pushcommitを比較し、real OAuth設定確認とDeveloper Console原価確認へ進める。

## 現状

- XGuard実装repoの想定パス: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`, `main...origin/main`, HEAD `455718c`
- 指定パス直近commit: `455718c Add XGuard frontend prototype`, `c0a7dcd Add Supabase usage ledger repository boundary`, `9dd0449 Translate README to Japanese`, `18676f0 Add runtime OAuth configuration`
- 昨日の一時clone: `/private/tmp/xguard-midday-2026-05-28`
- 一時clone状態: `main...origin/main [ahead 1]`, HEAD `9be85a1 Add Supabase API usage ledger repository`
- 判断: `9be85a1` はそのままpushしない。指定パスにある `c0a7dcd` と実装内容が重複または派生している可能性があるため、昼runで差分比較して未反映分だけ扱う。

## 昼の実装スコープ

### 作業ディレクトリ

1. まず `/Users/uryuatsuya/XGuard/xguard` で `test -w`, `git fetch origin main`, `git status --short --branch`, `git rev-parse --short HEAD`, `git log --oneline -8` を確認する。
2. 指定パスがwritableでremote最新へ同期できるなら、指定パスを作業場所にする。
3. 指定パスが書き込み不可、または`.git`更新不可なら、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-29` を作り、`UryuAtsuya/Xguard` のremote最新から作業する。
4. `/private/tmp/xguard-midday-2026-05-28` の `9be85a1` は参考commitとして扱う。`git show --stat 9be85a1` と指定パスの `c0a7dcd` を比較してから採用判断する。

### 変更対象ファイル

- `docs/API_COST_MODEL.md`: Developer Console実値、credit/spending設定、Usage endpoint、Owned Reads適用条件を記録する。
- `backend/src/repositories/supabaseApiUsageLedgerRepository.ts`: `c0a7dcd` と `9be85a1` の差分を確認し、未反映のtransaction境界があれば取り込む。
- `supabase/schema.sql`: `record_api_usage_event_with_monthly_limit` 相当のDB関数・制約・indexがremote最新に存在するか確認し、足りなければ最小更新する。
- `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`: row mapping、rollup、月次上限超過前停止、transaction失敗時の未反映を検証する。
- `backend/src/config/runtimeConfig.ts` とOAuth route: real envを入れたconfigured mode確認で必要な最小修正だけ行う。
- `docs/OAUTH_SETUP.md` または既存docs: secretを含めず、env名と確認手順だけ記録する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- `npx vitest run --configLoader runner`
- `npm run check`
- stage後に `git diff --cached --check`
- push前に `git status --short --branch`

## サブエージェント担当案

| Agent | 担当 | 完了条件 |
|---|---|---|
| Implementation agent | 指定パスまたは `/private/tmp/xguard-midday-2026-05-29` で、remote最新へ同期し、`9be85a1` と `c0a7dcd` を比較して未反映分だけ実装する。 | 実装commitが1本に整理され、force push不要で `origin/main` へpush可能。 |
| Review agent | OAuth scope、secret取り扱い、policy違反表現、ledger transaction境界、重複commit取り込みリスクをレビューする。 | `tweet.read`, `users.read`, `offline.access` 以外が増えていないこと、secretが文書化されていないことを確認。 |
| Verification agent | TypeScript、Vitest、`npm run check`、diff whitespace、git ahead/behind、remote push状態を確認する。 | 検証コマンド結果とcommit hashを昼メモへ残す。 |
| Documentation/Sync agent | MyLife側のPM ticket、project note、decisions、active projectsへ、XGuard repo commit hashと未解決事項を同期する。 | XGuard commitとMyLife commitを分けて報告できる状態にする。 |

## 今日の上位TODO

1. `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/remote最新状態を確認し、`455718c` と `origin/main` の関係を確定する。
2. `/private/tmp/xguard-midday-2026-05-28` の `9be85a1` と指定パスの `c0a7dcd` を比較し、Supabase ledger repositoryの未反映分だけ扱う。
3. real OAuth configured modeとDeveloper Console原価確認を行い、`docs/API_COST_MODEL.md` とcompany記録へ同期する。
