---
created: "2026-05-23"
project: "xguard"
type: research
status: initial-scan
sources:
  - "https://docs.x.com/x-api/getting-started/pricing"
  - "https://docs.x.com/x-api/fundamentals/rate-limits"
  - "https://docs.x.com/fundamentals/authentication/oauth-2-0/authorization-code"
  - "https://docs.x.com/fundamentals/authentication/guides/v2-authentication-mapping"
  - "https://docs.x.com/x-api/fundamentals/fields"
  - "https://docs.x.com/x-api/fundamentals/metrics"
  - "https://docs.x.com/developer-terms/policy"
  - "https://docs.x.com/developer-terms/agreement"
---

# 2026-05-23 XGuard 開発要素探索

## 結論

明日の開発は、いきなりNext.js/Expressを組むより先に、`X API接続 -> 自分の投稿/プロフィールを1回取得 -> DBへ保存 -> proof用DTOを生成` までを最小スパイクにする。

X APIは従量課金・endpoint別rate limit・利用規約の影響が強い。XGuard v0は「BAN復活」ではなく「本人が事前連携した自分の公開/許可済みデータを保管し、BAN後の再起動に使う証明ページを作る」に固定する。

## 公式docsから確認したこと

### 価格・課金

- X APIはPay-per-use前提。endpointごとの現在価格はDeveloper Consoleで確認する形。
- 契約・サブスク・最低利用料なしで、API creditsを購入して使う。
- Auto-rechargeとspending limitがあるため、XGuard側でもユーザーごとの月次API消費見積もりと停止条件が必要。
- Usage endpointで日次Post消費数を取得できる。

### rate limit

- rate limitはbillingとは別。rate limit内でも従量課金は発生する。
- `GET /2/users/:id/tweets` はタイムライン取得に使える。
- `GET /2/users/:id/followers` と `GET /2/users/:id/following` はfollowers/following候補取得に使える。
- `POST /2/users/:id/following` は可能だが、XGuard v0では自動followをしない。
- DM endpointは存在するが、XGuard v0では自動DMをしない。

### 認証・scope

- OAuth 2.0 Authorization Code Flow with PKCEが使える。
- refresh tokenがサポートされているため、日次バックアップにはrefresh tokenの安全な保管と更新処理が必要。
- v0で必要なscope候補:
  - `tweet.read`
  - `users.read`
  - `follows.read`
  - `offline.access`
- v0で意図的に避けるscope:
  - `tweet.write`
  - `follows.write`
  - DM write系scope

### 取得できるデータ候補

| データ | endpoint / field | v0判断 | 注意 |
|---|---|---|---|
| 自分の投稿一覧 | `GET /2/users/:id/tweets` | P0 | 初回は直近100件程度に制限する |
| 投稿本文・日時・ID | `tweet.fields=created_at,author_id,public_metrics,attachments` | P0 | defaultは最小fieldのみなのでfields指定が必要 |
| 投稿public metrics | `public_metrics` | P0 | like/reply/repost/quote/bookmark/impressionを保存候補にする |
| 自分のプロフィール | `GET /2/users/:id` / `GET /2/users/me` | P0 | `user.fields=created_at,description,public_metrics,verified` |
| follower/following数 | `user.public_metrics` | P0 | 証明ページには集計値中心 |
| follower/following個別リスト | `GET /2/users/:id/followers`, `following` | P1 | 個別ユーザー一覧の保存・公開は規約/プライバシー確認後 |
| メディアURL | `expansions=attachments.media_keys`, `media.fields=url,preview_image_url,alt_text,public_metrics` | P1 | 再配布/保存期間/削除対応が必要 |
| non-public / organic metrics | user context for owned posts | P2 | 取得できても証明ページ公開には使わない |
| DM | DM endpoints | out | v0では保存・送信しない |

### 規約・ポリシー上の重要点

- X Contentの第三者再配布は制限される。証明ページは「保存したraw payloadをそのまま公開」しない。
- 投稿・プロフィール・ユーザー情報を公開する場合でも、X Terms、Privacy Policy、Developer Agreement、Developer Policyへの準拠が必要。
- 削除、protected化、suspended、withheld、modifiedなどが起きたX Contentは、要求後24時間以内を目安に削除または修正する必要がある。
- write action、follow/unfollow、DM、投稿は、明示的同意・表示・Automation Rules対応が必要。v0では避ける。
- commercial useが限定的なself-serve範囲を超える場合、Enterprise planが必要になる可能性がある。

## v0の開発要素

### 最初に作る

1. OAuth接続スパイク
   - PKCE callback
   - `x_oauth_connections`
   - encrypted token保管
   - refresh token更新
   - revoked/expired時の状態遷移
2. read-only backup job
   - `GET /2/users/me`
   - `GET /2/users/:id/tweets`
   - `tweet.fields` と `user.fields` を明示
   - rate limit header保存
3. proof DTO生成
   - raw payloadではなく公開用DTOだけを生成
   - 投稿本文は件数制限
   - follower/following個別名は初期公開しない
4. compliance delete queue
   - 削除要求、protected化、BAN/認証失敗の再確認をキューとして扱う

### まだ作らない

- 自動DM
- 自動follow/unfollow
- follower個別一覧の公開
- raw payloadの公開
- iframe埋め込み
- AIによる大量の告知文自動投稿

## DB設計に足すもの

| 追加対象 | 理由 |
|---|---|
| `x_oauth_connections` | access token / refresh token / scope / expires_at / revoked_atを管理する |
| `api_usage_events` | X API従量課金とrate limit監視のため |
| `proof_pages` | 公開/非公開、取り下げ、slug再生成、redaction方針を分離する |
| `content_compliance_events` | 削除・protected化・withheld・ユーザー要求に追従する |
| `stripe_events` | webhook冪等性のため |
| `backup_runs` | job単位の成功/失敗、取得件数、rate limit、コスト見積もりを保存する |

## 明日の最小スパイク

1. `/Users/uryuatsuya/XGuard/xguard` をgit repoとして初期化する。
2. `docs/X_API_SCOPE.md` にこの調査結果からv0 scopeを移す。
3. DBスキーマに `x_oauth_connections`, `api_usage_events`, `proof_pages`, `content_compliance_events`, `stripe_events`, `backup_runs` を追加する。
4. 実コードはOAuth callbackの雛形と、mock tokenでのread-only backup service interfaceまでに絞る。

## 未確認

- Developer Console上の実際のendpoint別単価。
- X API app審査時に「BAN後の再起動支援」がどのuse caseとして承認されるか。
- メディアファイルのローカル保存可否と保存期間。
- follower/following個別リストをユーザー本人の復旧用途でどこまで保存・表示できるか。
- Supabase Vaultを使うか、別KMSを使うか。
