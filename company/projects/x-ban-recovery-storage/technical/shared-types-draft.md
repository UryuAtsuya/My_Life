---
created: "2026-05-23"
project: "xguard"
status: draft
tags: [typescript, shared-types]
---

# shared/types.ts ドラフト

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
  | "unknown";

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
  createdAt: string;
}

export interface XAccount {
  id: string;
  userId: string;
  xUserId: string;
  username: string;
  displayName?: string;
  status: XAccountStatus;
  connectedAt: string;
  suspectedBannedAt?: string;
}

export interface TweetSnapshot {
  id: string;
  xAccountId: string;
  tweetId: string;
  text: string;
  postedAt: string;
  likeCount?: number;
  repostCount?: number;
  replyCount?: number;
  capturedAt: string;
}

export interface ProfileSnapshot {
  id: string;
  xAccountId: string;
  displayName?: string;
  bio?: string;
  avatarUrl?: string;
  followerCount?: number;
  followingCount?: number;
  capturedAt: string;
}

export interface AccountHealthCheck {
  id: string;
  xAccountId: string;
  status: XAccountStatus;
  httpStatus?: number;
  errorCode?: string;
  checkedAt: string;
}

export interface RecoverySession {
  id: string;
  userId: string;
  oldXAccountId: string;
  newAccountUrl?: string;
  proofPageSlug: string;
  status: RecoverySessionStatus;
  createdAt: string;
  completedAt?: string;
}
```
