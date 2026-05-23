---
created: "2026-05-24"
project: "xguard"
type: morning-planning
status: handoff
---

# 2026-05-24 XGuard 朝会メモ

## 今日の優先順位

XGuardを事業側の最優先にする。note、Today Board、その他webサービス改善は、XGuardのread-only境界とDB schema v1が昼に固まるまで後回しにする。

## 朝の結論

- XGuard v0はread-onlyの事前バックアップと証明ページ生成に限定する。
- X APIはPay-per-useで、Owned Readsは安いが、followers/followingやmediaまで広げると月額3,000円の原価が崩れる可能性がある。
- 自動DM、自動follow/unfollow、自動投稿は規約・spam・ban evasionの見え方が悪いため、v0から外す。
- 証明ページはraw payloadではなく、公開用DTOのみを公開する。
- 昼は実装コードの本格着手ではなく、`supabase/schema.sql`, `shared/types.ts`, `docs/ARCHITECTURE.md`, `docs/API_COST_MODEL.md`, `docs/COMPLIANCE.md` に絞る。

## 昼への引き継ぎ

対象は `/Users/uryuatsuya/XGuard/xguard`。すでに `README.md`, `docs/X_API_SCOPE.md`, `docs/IMPLEMENTATION_GATE.md` があるため、これを前提に追加する。

最初の成果物は以下。

1. `supabase/schema.sql`: OAuth token保管、API使用量、backup run、proof page公開制御、content compliance、Stripe webhook冪等性。
2. `shared/types.ts`: proof DTOとstatus enum。
3. `docs/ARCHITECTURE.md`: v0のread-only構成。
4. `docs/API_COST_MODEL.md`: X API Pay-per-use前提の原価試算。
5. `docs/COMPLIANCE.md`: X Content削除/変更追従、raw payload非公開、user deletion request。

## 注意

LP文言は「BAN復活」ではなく、「事前バックアップ」「BAN後の再起動支援」「証明ページ生成」に固定する。
