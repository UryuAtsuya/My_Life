---
date: "2026-08-31"
project: "xguard"
type: midday-implementation
status: pr-ready
---

# 2026-08-31 XGuard 昼実装

- branch: `feature/frontend-source-boundary`（`cc98804`）
- objective: 顧客画面と管理画面の別entrypoint、別認証、別API権限を維持する
- slice: customerとadminのsource import境界gateを追加する
- 変更: customer sourceからadmin sourceと`shared/admin`へのimportを拒否し、admin sourceからcustomer sourceへのimportを拒否する検査を追加
- review findings: 拡張子付きの`shared/admin.ts` importで検査を回避できる問題を修正。追加の修正必須事項なし
- verification: Node.js 22で`npm run build:web`、`npm run check:bundle-separation`、`git diff --check`がpass
- PR / push: commit `cc98804`をpush。XGuard PR #69を`feature/frontend-source-boundary`から`develop`へ作成
- blocker: staging deployment、公開Supabase設定、admin redirect URL、staff/admin bootstrapが未準備のため、staging/productionは引き続きNo-Go
- 次の1手: PR #69をreviewして`develop`へmergeし、外部前提の準備後にcustomer/adminのtargeted E2Eを実行する
