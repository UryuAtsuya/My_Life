---
date: "2026-05-31"
project: "xguard"
type: morning-planning
status: completed
---

# 2026-05-31 XGuard 朝計画

## 朝会結論

今日もXGuardを事業最優先にする。朝runではproduction codeを実装しない。昼runは、指定パスに未コミット変更がある状態から始まるため、まず差分を読んで所有者・意図・remote同期状態を確認する。そのうえで、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認を閉じる。

## 現状

- XGuard実装repoの想定パス: `/Users/uryuatsuya/XGuard/xguard`
- 朝run確認: `exists=yes`, `writable=no`, `main...origin/main`, HEAD `d30fc48`
- 未コミット変更:
  - `backend/src/__tests__/api.test.ts`
  - `backend/src/app.ts`
  - `docs/API_SPEC.md`
  - `docs/DEPLOY.md`
- 直近commit:
  - `d30fc48 Harden Supabase usage ledger boundary`
  - `a40d4bf Translate docs to Japanese`
  - `d6b5b17 Add Supabase ledger cost-limit function`
  - `455718c Add XGuard frontend prototype`
- 判断: 指定パスがこの実行環境では書き込み不可で、かつ未コミット変更がある。昼runは無関係な変更を巻き戻さず、変更内容を把握してから進める。

## 昼の実装スコープ

### 作業ディレクトリ

1. まず `/Users/uryuatsuya/XGuard/xguard` で `test -w`, `git fetch origin main`, `git status --short --branch`, `git rev-parse --short HEAD`, `git diff --stat`, `git diff -- backend/src/__tests__/api.test.ts backend/src/app.ts docs/API_SPEC.md docs/DEPLOY.md` を確認する。
2. 指定パスがwritableで、未コミット変更が今日の実装範囲と整合するなら、指定パスを作業場所にする。
3. 指定パスが書き込み不可、または `.git` 更新不可なら、Vaultへ実装コードを置かず `/private/tmp/xguard-midday-2026-05-31` を作り、`UryuAtsuya/Xguard` のremote最新から作業する。
4. 指定パス側の未コミット変更は、必要差分だけを読んで一時cloneへ手動反映する。巻き戻しや強制上書きはしない。

### 変更対象ファイル

- `supabase/schema.sql`: `record_api_usage_event_with_monthly_limit` の実Supabase/Postgres適用確認。必要ならmigration test用の最小修正だけ行う。
- `backend/src/__tests__/api.test.ts`: 既存未コミット差分を読んだうえで、OAuth configured modeやAPI境界testがあるなら整合させる。
- `backend/src/app.ts`: real OAuth configured modeで必要な最小修正だけ行う。secret値はログやdocsへ残さない。
- `docs/API_SPEC.md`: `/api/x/oauth/start` やledger関連の実挙動が変わる場合だけ更新する。
- `docs/API_COST_MODEL.md`: Developer Consoleのendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件、月額3,000円案の原価前提を更新する。
- `docs/DEPLOY.md` または `docs/OAUTH_SETUP.md`: secret非表示で、env名、callback URL、scope確認手順だけ記録する。
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
| Implementation agent | 指定パスまたは `/private/tmp/xguard-midday-2026-05-31` で、未コミット差分の意図確認、実Supabase/Postgres migration test、OAuth configured mode、Developer Console原価確認に必要な最小修正を行う。 | `d30fc48` 以降の変更が1本のmeaningful commitに整理され、force push不要で `origin/main` へpush可能。 |
| Review agent | OAuth scope、secret取り扱い、policy違反表現、Supabase function権限、proof pageのraw payload公開リスク、未コミット差分の混入リスクをレビューする。 | `tweet.read`, `users.read`, `offline.access` 以外が増えていないこと、secretが文書化されていないこと、service-role境界が崩れていないことを確認。 |
| Verification agent | TypeScript、targeted Vitest、`npm run check`、diff whitespace、git ahead/behind、remote push状態を確認する。 | 検証コマンド結果、XGuard commit hash、push状態を昼メモへ残す。 |
| Documentation/Sync agent | MyLife側のPM ticket、project note、decisions、active projectsへ、実Supabase/OAuth/Developer Console確認結果を同期する。 | XGuard commitとMyLife commitを分けて報告できる状態にする。 |

## 今日の上位TODO

1. 指定パスの未コミット変更4ファイルを読んで、今日のOAuth/API検証範囲に取り込むか、別作業として避けるかを決める。
2. 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の権限、所有関係、同一Xアカウント整合性、月次上限超過、負値拒否を確認する。
3. real OAuth configured modeとDeveloper Console原価実値をsecret非表示で確認し、`docs/API_COST_MODEL.md` とcompany記録へ反映する。
