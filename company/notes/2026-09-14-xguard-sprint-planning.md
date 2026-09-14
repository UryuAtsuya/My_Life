---
date: "2026-09-14"
project: "xguard"
type: sprint-planning
status: blocked
---

# 2026-09-14 XGuard Sprint Planning

## 今週の候補

1. **Issue #44：Supabase stagingのschemaとrepositoryを実環境で検証する**
   - owner：Codexが技術実装と検証を担当し、Supabase project、credential、owner bootstrapはユーザーが用意する。
   - ready条件：staging project、DB URL、必要な秘密値、実行許可が揃う。
   - success check：schema適用、RLSとservice-role境界、Admin Auth、repository integration testが実DBで成功する。
   - required artifacts：検証結果、環境値一覧（秘密値は除外）、Issue更新。

2. **Issue #45：X OAuth 2.0 live token exchangeを実装する**
   - owner：Codexが実装とunit testを担当し、X Developer設定とstaging credentialはユーザーが用意する。
   - ready条件：現行X OAuth仕様の確認、callback URL、client設定、token保存先の境界が確定する。
   - success check：PKCEとstate検証、read-only scope、backend-only token境界、account一致確認、mock mode維持をテストで確認する。
   - required artifacts：実装commit、verification結果、PR、Issue更新。

3. **Issue #46：customer/admin/backendをstagingへdeployしてE2E検証する**
   - owner：ユーザーがRailway、Sites、Supabaseの環境設定を担当し、Codexがdeployment後のtargeted E2Eを担当する。
   - ready条件：Issue #44と#45の完了、staging環境値、別origin、admin bootstrapが揃う。
   - success check：customer/admin認証、route、CORS、bundle、role、token境界をstaging E2Eで確認する。
   - required artifacts：deployment URL、E2E evidence、Go/No-Go記録、Issue更新。

## blocker

GitHub上のstagingとproductionにdeployment、variables、secretsの実行証跡がなく、Supabase project、X credential、admin bootstrapも未確認である。

## 次の1手

ユーザーがstagingのSupabase projectとX OAuth設定を準備し、まずIssue #44の実DB検証を開始できる状態にする。
