---
date: "2026-06-15"
project: "xguard"
type: weekly-planning
status: ready
---

# 2026-06-15 週次 XGuard 計画

## 優先順位

XGuardを今週も最優先とする。production releaseはNo-Goを維持し、完了済みのruntime confirmation gateを新しいobjectiveへ複製せず、`feature/*`から`develop`への統合、staging検証、`develop`から`main`への昇格判断の順で既存release gateを閉じる。

## Branch状態

- 通常作業: `develop = origin/develop = 030a916`
- staging: `develop = origin/develop = 030a916`
- production: `main = origin/main = 030a916`
- 実装branch: `feature/runtime-confirmation-gates = origin/feature/runtime-confirmation-gates = f27ad55`
- 作業branch: `feature/proof-revocation-audit = origin/feature/proof-revocation-audit = 303bd34`。proof revocation compliance event実装はpush済み、`develop`未統合。
- `develop...origin/develop`、`main...origin/main`はいずれもahead 0 / behind 0。`f27ad55`は`develop`未統合。

## Blocker

- PR #1の`develop`統合とstaging検証が未完了。
- `feature/proof-revocation-audit`はfeature branchへpush済みのため、重複するproof監査sliceを新規に開始せずreview・`develop`統合待ちとして扱う。
- 実Supabase/Postgres検証に必要なlocal Supabase、`DATABASE_URL`、`SUPABASE_SERVICE_ROLE_KEY`が未確認。
- OAuth live token exchangeは実X credentialsとproduction callback URLが必要。
- `InMemoryOAuthStateRepository`はmulti-instance/restart境界を閉じていない。
- `output/playwright/`は未追跡の既存成果物として触らず、今週のsliceから除外する。

## 今週の実装slice

1. PR #1を`feature/runtime-confirmation-gates`から`develop`へ統合し、stagingでruntime confirmation gateを検証する。
2. staging検証がpassした場合だけ、`develop`から`main`への昇格PRを準備する。`main`への直接実装pushは行わない。
3. Supabase環境確保後、実Postgres integration testでrole、ownership、X account整合性、存在しないrun、負値、月次上限超過の拒否を確認する。
4. OAuth configured modeの実token exchange、subject/account照合、callback URL境界をlive credentialsで一度検証する。
5. `InMemoryOAuthStateRepository`をTTL付きatomic consume可能な永続repositoryへ置き換え、multi-instance/restart境界を閉じる。

各runは上記から1 sliceだけを実装・検証し、完了済み項目を別TODOとして複製しない。
