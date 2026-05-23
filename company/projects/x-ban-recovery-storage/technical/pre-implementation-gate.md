---
created: "2026-05-23"
project: "xguard"
type: implementation-gate
status: draft
---

# XGuard 実装前ゲート

## Gate 1: X API利用範囲

- [ ] Developer Consoleでendpoint別単価を確認する。
- [ ] `GET /2/users/me` が使えるscopeを確定する。
- [ ] `GET /2/users/:id/tweets` の取得件数、pagination、fieldsを決める。
- [ ] `GET /2/users/:id/followers` と `following` を保存対象にするか、集計値だけにするか決める。
- [ ] メディアURLとファイル本体を保存するか、URL/metadataだけにするか決める。

## Gate 2: セキュリティ

- [ ] OAuth tokenは平文保存しない。
- [ ] access token / refresh token / scope / expires_at / revoked_at を `x_oauth_connections` で管理する。
- [ ] フロントエンドにservice role keyやtokenを返さない。
- [ ] token失効時は `x_accounts.status = auth_expired` にする。
- [ ] token削除とユーザーデータ削除の導線を用意する。

## Gate 3: 規約・公開制御

- [ ] 証明ページはraw payloadを直接公開しない。
- [ ] 公開用DTOを `proof_pages.public_payload` として生成する。
- [ ] `visibility`, `published_at`, `revoked_at`, `redaction_policy_version` を持たせる。
- [ ] 削除・protected化・suspended・withheld・ユーザー要求に追従する `content_compliance_events` を持たせる。
- [ ] 自動DM、自動follow/unfollow、BAN回避と見える機能はv0に入れない。

## Gate 4: 課金・コスト

- [ ] X API使用量を `api_usage_events` と `backup_runs` に残す。
- [ ] ユーザー単位の月次APIコスト見積もりを作る。
- [ ] Stripe webhookは `stripe_events.event_id` uniqueで冪等化する。
- [ ] X API spending limitに達した時の停止/通知ルールを決める。

## Gate 5: 明日の実装順

1. XGuard repo初期化。
2. `docs/X_API_SCOPE.md` を作成。
3. Supabase schema v1 draftを作成。
4. OAuth callbackとtoken repositoryのinterfaceを作成。
5. read-only backup jobのservice interfaceを作成。

## Go / No-Go

- Go: read-only接続、OAuth token安全保管、proof DTO、compliance queueまで。
- No-Go: write action、DM送信、一括follow、raw payload公開、規約未確認のLP訴求。
