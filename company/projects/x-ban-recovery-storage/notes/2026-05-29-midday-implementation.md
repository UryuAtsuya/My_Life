---
date: "2026-05-29"
type: project-note
project: x-ban-recovery-storage
---

# 2026-05-29 XGuard 昼実装

## 結果

`/Users/uryuatsuya/XGuard/xguard` は `XGUARD_NOT_WRITABLE` で、`.git/FETCH_HEAD` も書き込み不可だった。Vaultへ実装コードを置かず、指定パスのローカル `455718c` を元に `/private/tmp/xguard-midday-2026-05-29-localref` を作って実装した。

`9be85a1` はそのままpushせず、`c0a7dcd` との差分から未反映のproduction boundaryだけを採用した。XGuard local commitは `3120411 Harden Supabase usage ledger boundary`。

## 実装境界

- v0 OAuth scopeは `tweet.read`, `users.read`, `offline.access` のまま。
- `record_api_usage_event_with_monthly_limit` は `service_role` 専用のDB関数として追加。
- 月次原価上限は `user_profiles` を `for update` でロックしてinsert前に判定する。
- `x_account_id` / `backup_run_id` の所有者と相互整合性をDB関数内で検証する。
- 負の利用量、負のrate-limit counter、負の推定原価はDB境界でも拒否する。
- Supabase `numeric` が文字列で返る場合もdomain DTOではnumberへ変換する。

## 検証

- `npm ci`: pass
- `tsc --noEmit`: pass
- targeted Vitest: pass（4 files / 34 tests）
- `npm run check`: pass（6 files / 37 tests）
- `git diff --check`: pass
- `git diff --cached --check`: pass

## Git状態

- 作業コピー: `/private/tmp/xguard-midday-2026-05-29-localref`
- XGuard local commit: `3120411`
- push先予定: `UryuAtsuya/Xguard` `origin/main`
- push結果: 未push。`git push origin main` は `fetch first`。`git fetch origin main` / `git ls-remote origin refs/heads/main` は `Could not resolve host: github.com`。

## 次

1. remote先行分をfetchし、`3120411` をrebase/mergeしてpushする。
2. 実Supabase/PostgresでDB関数の権限、所有関係、上限超過、負値拒否を検証する。
3. OAuth configured modeとDeveloper Console原価確認を閉じる。
