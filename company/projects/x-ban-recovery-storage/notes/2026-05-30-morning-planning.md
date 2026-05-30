---
date: "2026-05-30"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-05-30 XGuard 朝計画

## 朝会結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、昨日push済みの `d30fc48 Harden Supabase usage ledger boundary` を前提に、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認を閉じる。

## 現状

- XGuard実装repoの想定パス: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`, `main...origin/main`, HEAD `d30fc48`
- 直近commit:
  - `d30fc48 Harden Supabase usage ledger boundary`
  - `a40d4bf Translate docs to Japanese`
  - `d6b5b17 Add Supabase ledger cost-limit function`
  - `455718c Add XGuard frontend prototype`
- 判断: 指定パスがこの実行環境では書き込み不可だが、Git状態はremote追従済み。昼runは指定パスのwrite/fetchを再確認し、書けなければ `/private/tmp/xguard-midday-2026-05-30` をremote最新から作る。

## 昼の実装スコープ

### 作業ディレクトリ

1. まず `/Users/uryuatsuya/XGuard/xguard` で `test -w`, `git fetch origin main`, `git status --short --branch`, `git rev-parse --short HEAD`, `git log --oneline -8` を確認する。
2. 指定パスがwritableでremote最新へ同期できるなら、指定パスを作業場所にする。
3. 指定パスが書き込み不可、または `.git` 更新不可なら、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-30` を作り、`UryuAtsuya/Xguard` のremote最新から作業する。

### 変更対象ファイル

- `supabase/schema.sql`: `record_api_usage_event_with_monthly_limit` の実Supabase/Postgres適用確認。必要ならmigration test用の最小修正だけ行う。
- `backend/src/__tests__/supabaseApiUsageLedgerRepository.test.ts`: 実DB境界で確認できない項目をrepository testへ補完する。
- `docs/API_COST_MODEL.md`: Developer Consoleのendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件、月額3,000円案の原価前提を更新する。
- `backend/src/config/runtimeConfig.ts` とOAuth route: real env configured mode確認で必要な最小修正だけ行う。secret値はログやdocsへ残さない。
- `docs/OAUTH_SETUP.md` または既存docs: secret非表示で、env名、callback URL、scope確認手順だけ記録する。
- `docs/COMPLIANCE.md`: 実Supabase/OAuth/Developer Console確認でpolicy境界に変化があれば追記する。

### 検証

- `git diff --check`
- `npx tsc -p tsconfig.json --noEmit`
- targeted Vitest: ledger repository / OAuth config周辺
- `npm run check`
- stage後に `git diff --cached --check`
- push前に `git status --short --branch`

## サブエージェント担当案

| Agent | 担当 | 完了条件 |
|---|---|---|
| Implementation agent | 指定パスまたは `/private/tmp/xguard-midday-2026-05-30` で、実Supabase/Postgres migration test、OAuth configured mode、Developer Console原価確認に必要な最小修正を行う。 | `d30fc48` 以降の変更が1本のmeaningful commitに整理され、force push不要で `origin/main` へpush可能。 |
| Review agent | OAuth scope、secret取り扱い、policy違反表現、Supabase function権限、proof pageのraw payload公開リスクをレビューする。 | `tweet.read`, `users.read`, `offline.access` 以外が増えていないこと、secretが文書化されていないこと、service-role境界が崩れていないことを確認。 |
| Verification agent | TypeScript、targeted Vitest、`npm run check`、diff whitespace、git ahead/behind、remote push状態を確認する。 | 検証コマンド結果、XGuard commit hash、push状態を昼メモへ残す。 |
| Documentation/Sync agent | MyLife側のPM ticket、project note、decisions、active projectsへ、実Supabase/OAuth/Developer Console確認結果を同期する。 | XGuard commitとMyLife commitを分けて報告できる状態にする。 |

## 今日の上位TODO

1. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の権限、所有関係、同一Xアカウント整合性、月次上限超過、負値拒否を確認する。
2. real OAuth configured modeをsecret非表示で確認し、callback URLとscopeが `tweet.read`, `users.read`, `offline.access` のままか記録する。
3. Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md`、PM ticket、project noteへ反映する。
