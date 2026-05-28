---
date: "2026-05-28"
type: project-note
project: x-ban-recovery-storage
---

# 2026-05-28 Midday Implementation

## Result

`/Users/uryuatsuya/XGuard/xguard` was writable today. The local branch was merged with pushed canonical `3528e26`, then the backend prototype gained runtime OAuth configuration.

XGuard push: `18676f0 Add runtime OAuth configuration` -> `UryuAtsuya/Xguard` `origin/main`.

## Product Boundary

- v0 stays read-only: `tweet.read`, `users.read`, `offline.access`.
- The current callback still stores repository refs only; real token exchange remains future work.
- `X_CLIENT_ID` is now the switch from mock OAuth metadata to configured OAuth metadata.
- `X_CALLBACK_URL` can be explicit, or falls back to `${APP_BASE_URL}/api/x/oauth/callback` / local port `4000`.

## Verification

- `git diff --check`: pass
- `git diff --cached --check`: pass
- `npm run check`: pass
- Vitest: 4 files / 30 tests pass

## Next

1. Add real X OAuth env values and confirm `/api/x/oauth/start` reports configured mode.
2. Confirm Developer Console pricing, Usage endpoint, spending controls, and Owned Reads applicability.
3. Implement the Supabase usage ledger repository transaction and monthly cost-limit guard.
