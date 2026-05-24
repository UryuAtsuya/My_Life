---
created: "2026-05-25"
project: "xguard"
type: morning-planning
status: handoff
---

# 2026-05-25 XGuard 朝会メモ

## 今日の優先順位

XGuardを事業側の最優先にする。今日の焦点は「書ける状態の実装repoで、規約・原価・read-only境界をdocsとbuild gateへ固定する」こと。

## 朝の結論

- XGuard v0はread-onlyの事前バックアップと証明ページ生成に限定する。
- 初期scopeは `tweet.read`, `users.read`, `offline.access` に維持する。
- X API価格はPay-per-usageで、endpoint別の現行単価はDeveloper Console実画面確認を正とする。
- proof pageはraw payloadを公開しない。公開DTO、取り下げ、redaction、X Content削除追従を必須にする。
- 自動DM、自動follow/unfollow、自動投稿、bulk outreach、BAN回避に見える導線はv0から外す。
- `/Users/uryuatsuya/XGuard/xguard` は存在し、git statusはclean。ただし朝run時点のCodexサンドボックスからは `NOT_WRITABLE`。

## 昼への引き継ぎ

対象は `/Users/uryuatsuya/XGuard/xguard`。

昼run冒頭で以下を確認する。

```bash
cd /Users/uryuatsuya/XGuard/xguard
git status --short --branch
test -w .
```

書ける場合の成果物は以下。

1. `docs/ARCHITECTURE.md`: read-only OAuth、backend service境界、token repository、backup job、proof DTO、compliance events。
2. `docs/API_COST_MODEL.md`: Pay-per-usage、Developer Console確認項目、spending limit、ユーザー単位取得上限、月次停止/通知。
3. `docs/COMPLIANCE.md`: X Content削除/非公開化/withheld/ユーザー削除要求への24時間追従、raw payload非公開、proof page取り下げ。
4. `tsconfig.build.json` または同等のbuild分離: `backend/src/__tests__/**` をproduction buildから外す。
5. Supabase repository層: `TokenRepository` をservice role + encryption/secret store前提にし、token本文をfrontendへ返さない。

## 検証

```bash
git diff --check
npm run build
npm run check
npx vitest run --configLoader runner
```

同じ環境で `NOT_WRITABLE` が続く場合は、MyLife Vault内へ実装コードを迂回配置せず、権限ブロッカーとして記録する。
