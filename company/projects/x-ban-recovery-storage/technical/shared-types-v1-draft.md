---
created: "2026-05-24"
project: "xguard"
status: draft
target_path: "/Users/uryuatsuya/XGuard/xguard/shared/types.ts"
tags: [typescript, shared-types, proof-dto, compliance]
---

# shared/types.ts v1 ドラフト

XGuard repoが書き込み可能になったら、下記を `/Users/uryuatsuya/XGuard/xguard/shared/types.ts` の初期内容として使う。

```ts
export type SubscriptionStatus =
  | "inactive"
  | "trialing"
  | "active"
  | "past_due"
  | "canceled";

export type XAccountStatus =
  | "connected"
  | "auth_expired"
  | "rate_limited"
  | "suspected_banned"
  | "banned"
  | "suspended"
  | "deleted"
  | "unknown";

export type BackupRunStatus =
  | "queued"
  | "running"
  | "completed"
  | "partial"
  | "failed"
  | "rate_limited"
  | "auth_expired";

export type ProofPageVisibility = "private" | "unlisted" | "public" | "revoked";

export type ContentComplianceEventType =
  | "tweet_deleted"
  | "tweet_protected"
  | "tweet_withheld"
  | "tweet_changed"
  | "user_deleted"
  | "user_suspended"
  | "user_request_delete"
  | "proof_page_revoked";

export type RecoverySessionStatus =
  | "draft"
  | "proof_ready"
  | "new_account_registered"
  | "completed";

export interface UserProfile {
  id: string;
  email: string;
  subscriptionStatus: SubscriptionStatus;
  stripeCustomerId?: string;
  stripeSubscriptionId?: string;
  monthlyApiCostLimitUsd: number;
  createdAt: string;
  updatedAt: string;
}

export interface XAccount {
  id: string;
  userId: string;
  xUserId: string;
  username: string;
  displayName?: string;
  avatarUrl?: string;
  status: XAccountStatus;
  connectedAt: string;
  lastBackupAt?: string;
  lastHealthCheckAt?: string;
  suspectedBannedAt?: string;
  bannedAt?: string;
}

export interface XOAuthConnection {
  id: string;
  xAccountId: string;
  provider: "x";
  scope: string[];
  expiresAt?: string;
  refreshedAt?: string;
  revokedAt?: string;
}

export interface BackupRun {
  id: string;
  xAccountId: string;
  status: BackupRunStatus;
  startedAt?: string;
  completedAt?: string;
  tweetLimit: number;
  tweetsCaptured: number;
  profilesCaptured: number;
  apiUnitsUsed: number;
  estimatedCostUsd: number;
  rateLimitRemaining?: number;
  rateLimitResetAt?: string;
  errorCode?: string;
  errorMessage?: string;
  createdAt: string;
}

export interface ApiUsageEvent {
  id: string;
  userId: string;
  xAccountId?: string;
  backupRunId?: string;
  endpoint: string;
  method: "GET" | "POST" | "PUT" | "PATCH" | "DELETE";
  resourceType: "post" | "user" | "follower" | "following" | "media" | "usage" | "unknown";
  resourceCount: number;
  ownedRead: boolean;
  estimatedCostUsd: number;
  rateLimitLimit?: number;
  rateLimitRemaining?: number;
  rateLimitResetAt?: string;
  statusCode?: number;
  occurredAt: string;
}

export interface TweetSnapshot {
  id: string;
  xAccountId: string;
  backupRunId?: string;
  tweetId: string;
  text: string;
  postedAt: string;
  likeCount?: number;
  repostCount?: number;
  replyCount?: number;
  quoteCount?: number;
  bookmarkCount?: number;
  impressionCount?: number;
  mediaUrls: string[];
  capturedAt: string;
  deletedAt?: string;
  withheldAt?: string;
  protectedAt?: string;
}

export interface ProfileSnapshot {
  id: string;
  xAccountId: string;
  backupRunId?: string;
  displayName?: string;
  bio?: string;
  avatarUrl?: string;
  bannerUrl?: string;
  followerCount?: number;
  followingCount?: number;
  tweetCount?: number;
  listedCount?: number;
  capturedAt: string;
}

export interface AccountHealthCheck {
  id: string;
  xAccountId: string;
  status: XAccountStatus;
  reason:
    | "ok"
    | "not_found"
    | "forbidden"
    | "auth_failed"
    | "rate_limited"
    | "api_error"
    | "network_error"
    | "unknown";
  httpStatus?: number;
  errorCode?: string;
  errorMessage?: string;
  checkedAt: string;
}

export interface ProofPublicPayload {
  version: "v1";
  xUserId: string;
  username: string;
  displayName?: string;
  profileSummary?: string;
  profileImageUrl?: string;
  accountCreatedAt?: string;
  backedUpFrom: string;
  backedUpUntil: string;
  snapshotCounts: {
    tweets: number;
    profileSnapshots: number;
  };
  publicMetrics?: {
    followers?: number;
    following?: number;
    tweets?: number;
    listed?: number;
  };
  representativeTweets: Array<{
    tweetId: string;
    text: string;
    postedAt: string;
    publicMetrics?: {
      likes?: number;
      reposts?: number;
      replies?: number;
      quotes?: number;
    };
  }>;
  redactionPolicyVersion: string;
}

export interface ProofPage {
  id: string;
  userId: string;
  xAccountId: string;
  slug: string;
  visibility: ProofPageVisibility;
  publicPayload: ProofPublicPayload;
  redactionPolicyVersion: string;
  publishedAt?: string;
  revokedAt?: string;
  createdAt: string;
  updatedAt: string;
}

export interface ContentComplianceEvent {
  id: string;
  xAccountId: string;
  tweetSnapshotId?: string;
  proofPageId?: string;
  eventType: ContentComplianceEventType;
  source: "x_api" | "user_request" | "admin_review";
  details: Record<string, unknown>;
  resolvedAt?: string;
  createdAt: string;
}

export interface RecoverySession {
  id: string;
  userId: string;
  oldXAccountId: string;
  proofPageId?: string;
  newAccountUrl?: string;
  announcementDraft?: string;
  pinnedPostDraft?: string;
  profileBioDraft?: string;
  status: RecoverySessionStatus;
  createdAt: string;
  proofReadyAt?: string;
  completedAt?: string;
}

export interface ManualNotificationQueueItem {
  id: string;
  recoverySessionId: string;
  targetXUserId?: string;
  targetUsername?: string;
  messageDraft: string;
  reviewStatus: "pending" | "approved" | "rejected" | "sent_manually";
  reviewedAt?: string;
  createdAt: string;
}
```

## 境界

- `XOAuthConnection` はtoken本文を型として共有しない。暗号化token列はDB/service repository内だけで扱う。
- `ProofPublicPayload` はraw X API responseではない。公開可能な集約DTOだけを持つ。
- `ManualNotificationQueueItem` は手動レビュー用。自動DM送信の実装前提にしない。
