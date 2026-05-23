-- XGuard Supabase v0 schema
-- Created: 2026-05-23
-- Purpose: v0のバックアップ、BAN候補検知、証明ページ生成に必要な最小DB構造。
-- Note: 自動DM送信、一括フォロー、BAN回避に見える操作は含めない。

create type public.subscription_status as enum (
  'inactive',
  'trialing',
  'active',
  'past_due',
  'canceled'
);

create type public.x_account_status as enum (
  'connected',
  'auth_expired',
  'rate_limited',
  'suspected_banned',
  'banned',
  'unknown'
);

create type public.recovery_session_status as enum (
  'draft',
  'proof_ready',
  'new_account_registered',
  'completed'
);

create type public.health_check_reason as enum (
  'ok',
  'not_found',
  'forbidden',
  'auth_failed',
  'rate_limited',
  'api_error',
  'network_error',
  'unknown'
);

create table public.user_profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  email text not null,
  subscription_status public.subscription_status not null default 'inactive',
  stripe_customer_id text,
  stripe_subscription_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.x_accounts (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.user_profiles(id) on delete cascade,
  x_user_id text not null,
  username text not null,
  display_name text,
  avatar_url text,
  status public.x_account_status not null default 'connected',
  connected_at timestamptz not null default now(),
  last_backup_at timestamptz,
  last_health_check_at timestamptz,
  suspected_banned_at timestamptz,
  banned_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, x_user_id)
);

create table public.tweet_snapshots (
  id uuid primary key default gen_random_uuid(),
  x_account_id uuid not null references public.x_accounts(id) on delete cascade,
  tweet_id text not null,
  text text not null,
  posted_at timestamptz not null,
  like_count integer,
  repost_count integer,
  reply_count integer,
  quote_count integer,
  bookmark_count integer,
  impression_count integer,
  media_urls text[] not null default '{}',
  raw_payload jsonb not null default '{}'::jsonb,
  captured_at timestamptz not null default now(),
  unique (x_account_id, tweet_id, captured_at)
);

create table public.profile_snapshots (
  id uuid primary key default gen_random_uuid(),
  x_account_id uuid not null references public.x_accounts(id) on delete cascade,
  display_name text,
  bio text,
  avatar_url text,
  banner_url text,
  follower_count integer,
  following_count integer,
  tweet_count integer,
  listed_count integer,
  raw_payload jsonb not null default '{}'::jsonb,
  captured_at timestamptz not null default now()
);

create table public.account_health_checks (
  id uuid primary key default gen_random_uuid(),
  x_account_id uuid not null references public.x_accounts(id) on delete cascade,
  status public.x_account_status not null,
  reason public.health_check_reason not null default 'unknown',
  http_status integer,
  error_code text,
  error_message text,
  checked_at timestamptz not null default now()
);

create table public.recovery_sessions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references public.user_profiles(id) on delete cascade,
  old_x_account_id uuid not null references public.x_accounts(id) on delete cascade,
  new_account_url text,
  proof_page_slug text not null unique,
  proof_payload jsonb not null default '{}'::jsonb,
  announcement_draft text,
  pinned_post_draft text,
  profile_bio_draft text,
  status public.recovery_session_status not null default 'draft',
  created_at timestamptz not null default now(),
  proof_ready_at timestamptz,
  completed_at timestamptz
);

create table public.manual_notification_queue (
  id uuid primary key default gen_random_uuid(),
  recovery_session_id uuid not null references public.recovery_sessions(id) on delete cascade,
  target_x_user_id text,
  target_username text,
  message_draft text not null,
  review_status text not null default 'pending',
  reviewed_at timestamptz,
  created_at timestamptz not null default now()
);

create index x_accounts_user_id_idx on public.x_accounts(user_id);
create index tweet_snapshots_x_account_id_captured_at_idx
  on public.tweet_snapshots(x_account_id, captured_at desc);
create index profile_snapshots_x_account_id_captured_at_idx
  on public.profile_snapshots(x_account_id, captured_at desc);
create index account_health_checks_x_account_id_checked_at_idx
  on public.account_health_checks(x_account_id, checked_at desc);
create index recovery_sessions_user_id_created_at_idx
  on public.recovery_sessions(user_id, created_at desc);

alter table public.user_profiles enable row level security;
alter table public.x_accounts enable row level security;
alter table public.tweet_snapshots enable row level security;
alter table public.profile_snapshots enable row level security;
alter table public.account_health_checks enable row level security;
alter table public.recovery_sessions enable row level security;
alter table public.manual_notification_queue enable row level security;

create policy "Users can read own profile"
  on public.user_profiles for select
  using (auth.uid() = id);

create policy "Users can read own x accounts"
  on public.x_accounts for select
  using (auth.uid() = user_id);

create policy "Users can read own tweet snapshots"
  on public.tweet_snapshots for select
  using (
    exists (
      select 1 from public.x_accounts
      where x_accounts.id = tweet_snapshots.x_account_id
        and x_accounts.user_id = auth.uid()
    )
  );

create policy "Users can read own profile snapshots"
  on public.profile_snapshots for select
  using (
    exists (
      select 1 from public.x_accounts
      where x_accounts.id = profile_snapshots.x_account_id
        and x_accounts.user_id = auth.uid()
    )
  );

create policy "Users can read own health checks"
  on public.account_health_checks for select
  using (
    exists (
      select 1 from public.x_accounts
      where x_accounts.id = account_health_checks.x_account_id
        and x_accounts.user_id = auth.uid()
    )
  );

create policy "Users can read own recovery sessions"
  on public.recovery_sessions for select
  using (auth.uid() = user_id);

create policy "Users can read own manual notification queue"
  on public.manual_notification_queue for select
  using (
    exists (
      select 1
      from public.recovery_sessions
      where recovery_sessions.id = manual_notification_queue.recovery_session_id
        and recovery_sessions.user_id = auth.uid()
    )
  );

-- Insert/update/deleteはservice role経由で行う。
-- フロントエンドからの直接書き込みはv0では許可しない。
