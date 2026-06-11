---
date: "2026-06-11"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-11 週次 XGuard 計画

## 優先順位

XGuardを今週も最優先とする。production releaseはNo-Goを維持し、新しいobjectiveは作らず、既存のrelease gateを閉じる。

## Blocker

- 実Supabase/Postgres検証に必要なDB URL、`psql`、Supabase CLI環境が未確認。
- OAuth live token exchangeは実X credentialsと本番callback URLが必要。
- MyLifeの`git fetch origin`はDNS解決失敗、XGuardの`git fetch origin`は`.git/FETCH_HEAD`書き込み権限で失敗。XGuard localでは`HEAD = origin/main = 9a7a783`だが、live remoteは未確認。
- XGuardの`output/playwright/`は未追跡のため、今週の実装sliceから除外する。

## 今週の実装slice

1. 実Supabase/Postgresでusage ledger integration testを実行し、role、ownership、X account整合性、負値、存在しないrun、月次上限超過の拒否を確認する。
2. `PRICING_CONFIRMED` / `COMPLIANCE_CONFIRMED` production gateの実装有無を現HEADで確認し、未実装ならruntimeConfigとtargeted testに限定して追加する。
3. OAuth configured modeの実token exchange、subject/account照合、callback URL境界をlive credentialsで一度検証する。
4. `InMemoryOAuthStateRepository`をTTL付きatomic consume可能な永続repositoryへ置き換え、multi-instance/restart境界を閉じる。
5. proof visibility変更とrevocationに監査/compliance eventを記録し、所有者以外の操作拒否をtargeted testで固定する。

各runは上記から1 sliceだけを実装・検証し、完了済み項目を別TODOとして複製しない。
