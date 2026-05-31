---
created: "2026-05-31"
project: "xguard"
assignee: "codex"
priority: high
status: in_progress
---

# XGuard dirty path / Supabase / OAuth / cost verification

## 内容

指定パス `/Users/uryuatsuya/XGuard/xguard` に未コミット変更がある状態を最初に確認し、無関係な変更を巻き戻さず、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認を閉じる。

## 背景

- XGuard正本は `/Users/uryuatsuya/XGuard/xguard`。
- 最新push済みcommitは `d30fc48 Harden Supabase usage ledger boundary`。
- 2026-05-31朝run時点で `/Users/uryuatsuya/XGuard/xguard` は `exists=yes`, `writable=no`, `main...origin/main`, HEAD `d30fc48`。
- 未コミット変更は `backend/src/__tests__/api.test.ts`, `backend/src/app.ts`, `docs/API_SPEC.md`, `docs/DEPLOY.md`。
- Supabase SQL function `record_api_usage_event_with_monthly_limit` は、所有関係検証、同一Xアカウント整合性、負値拒否、`service_role` grant、Supabase numeric string mappingまで実装済み。
- 残る最重要は、実Supabase/Postgres migration test、real OAuth configured mode、Developer Console原価実値確認。

## 完了条件

- [x] `/Users/uryuatsuya/XGuard/xguard` のwrite/fetch/remote HEADを昼run冒頭で確認する。
- [x] 未コミット変更4ファイルの差分を読み、今日のOAuth/API検証に必要な変更か、別作業として避ける変更かを記録する。
- [x] 書き込み不可なら `/private/tmp/xguard-midday-2026-05-31` をremote最新から作り、Vaultへ実装コードを置かない。
- [ ] 実Supabase/Postgres migration testで `record_api_usage_event_with_monthly_limit` の `service_role` 実行可、`authenticated` 実行不可を確認する。
- [ ] 実Supabase/Postgres migration testで異user、異Xアカウント、存在しないbackup_run、負値、月次上限超過が拒否されることを確認する。
- [ ] real envを使って `/api/x/oauth/start` のconfigured modeを確認する。secret値はログやcompany文書に残さない。
- [ ] callback URLとscopeが `tweet.read`, `users.read`, `offline.access` のままか記録する。
- [ ] Developer Consoleでendpoint別単価、credit/spending設定、Usage endpoint、Owned Reads条件を確認し、`docs/API_COST_MODEL.md` へ反映する。
- [x] `git diff --check`, `npx tsc -p tsconfig.json --noEmit`, targeted Vitest、`npm run check`, `git diff --cached --check` を実行する。
- [ ] meaningfulなXGuard実装変更があれば `UryuAtsuya/Xguard` `origin/main` へcommit/pushする。
- [x] MyLife側へ昼実装メモ、夜レビュー、XGuard commit hash、MyLife sync commit hashを分けて報告する。

## 2026-05-31 昼run更新

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は `writable=no`。`git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。
- 未コミット変更4ファイルはOAuth status endpoint、test、API/DEPLOY docsで、今日のOAuth/API検証範囲に取り込んだ。
- 実装場所: `/private/tmp/xguard-midday-2026-05-31`
- XGuard local commit: `09ff660 Add OAuth status endpoint`
- push状態: `git push origin main` は再試行時にremote先行で `fetch first` 拒否。その後の `git fetch origin main` は `Could not resolve host: github.com` で失敗。force pushなし。
- 指定パス最終確認: `/Users/uryuatsuya/XGuard/xguard` はcleanで `552f2e5 Add OAuth status diagnostic endpoint`。local tracking `origin/main` も `552f2e5`。live remote再読込はDNS失敗。
- 追加API: `GET /api/x/oauth/status`。real envの実機確認は未完了。
- 返却: `mode`, `callbackUrl`, `scopes`, `clientIdConfigured`, `clientSecretConfigured`, `writesEnabled`, `missingEnv`
- 非返却: `X_CLIENT_SECRET` 値、OAuth token material、`clientId` 値、`authorizationUrl`
- 検証: `git diff --check`, targeted Vitest（1 file / 6 tests）, `tsc --noEmit`, `npm run check`（6 files / 39 tests）, `git diff --cached --check` pass。
- Review: P0/P1なし。P2としてExpress内部構造に依存するroute testの脆さあり。sandboxでHTTP listenが `EPERM` になるため今回は許容。

## 2026-05-31 夜レビュー更新

- 指定パス `/Users/uryuatsuya/XGuard/xguard` は夜run時点でclean。local `HEAD` / local `origin/main` は `552f2e5 Add OAuth status diagnostic endpoint`。
- `git fetch origin main` は `.git/FETCH_HEAD: Operation not permitted`。`git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。live remote確認は未完了。
- canonical pathの `npm run check` は `dist/` write `EPERM` で失敗。代替として `/private/tmp/xguard-evening-check-20260531-YdDOVH/repo` のローカルクローンで `npm run check` pass（6 files / 39 tests）。
- 夜レビュー主要指摘: P0なし。P1は `/api/x/oauth/status` の無認証診断公開リスクと、real OAuthがまだ静的state/mock PKCE/mock callback段階である点。P2は `missingEnv` の運用性とExpress内部構造依存test。
- 明日は `552f2e5` のGitHub live remote確認、`09ff660` の破棄/統合判断、実Supabase/Postgres migration test、Developer Console原価確認を優先する。

## 判断ルール

- v0初期scopeは `tweet.read`, `users.read`, `offline.access` のみ。
- `follows.read`, DM/write/follow系scopeはv0に入れない。
- API原価は通常read単価で保守的に見積もり、`Owned Reads` はDeveloper Consoleで適用条件を確認するまで主前提にしない。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避導線は作らない。
- 実装コードはMyLife Vaultへ迂回配置しない。
