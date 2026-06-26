# Company Daily Automation

## Purpose

Run company operations through three daily Codex automations: morning planning, midday production, and evening closeout.

## Daily Flow

1. Morning: create/update today's TODO, choose priorities, run a business meeting, record decisions, and research the note article market/topic for midday.
2. Midday: pick the top executable TODO, with note article production/publishing as the default growth task, then actually produce, publish, measure, or prepare the concrete artifact.
3. Evening: close the day, summarize completed work and blockers, carry unfinished tasks into tomorrow, and sync changes.

## Automations

- ID: `morning-company-business-meeting`
- Name: Morning company business meeting
- Time: every day at 8:00
- Role: planning, TODO, priorities, meeting summary, decisions, note market/topic research
- Status: ACTIVE

- ID: `midday-company-production-session`
- Name: Midday company production session
- Time: every day at 12:30
- Role: implementation, production, note article writing/publishing, posting preparation, measurement setup, PM/project updates
- Status: ACTIVE

- ID: `evening-company-closeout-review`
- Name: Evening company closeout review
- Time: every day at 18:00
- Role: daily closeout, completed/unfinished work, tomorrow handoff, final commit/push
- Status: ACTIVE

## Local Automation Files

- `/Users/uryuatsuya/.codex/automations/morning-company-business-meeting/automation.toml`
- `/Users/uryuatsuya/.codex/automations/midday-company-production-session/automation.toml`
- `/Users/uryuatsuya/.codex/automations/evening-company-closeout-review/automation.toml`

## 2026-05-10 Update

The previous single morning workflow was split into a three-meeting daily cadence. Morning now avoids substantial implementation unless needed to unblock planning; midday owns the actual execution slice; evening owns the closeout and tomorrow handoff.

## 2026-05-11 Note Automation Update

The daily note workflow is now split across morning and midday:

1. Morning researches current note/AI/tool/development topics and writes `company/marketing/content-plan/note-research-YYYY-MM-DD.md`.
2. Morning updates the note backlog and makes the midday note article candidate explicit in the TODO.
3. Midday uses `/Users/uryuatsuya/.codex/skills/note-growth-editor/SKILL.md` to draft, score, improve, prepare eyecatch prompts, and publish one note article when it reaches 80/100 or higher.
4. Midday is explicitly permitted to click `投稿する` for the selected daily note article after the publish checklist passes.
5. If publishing succeeds, midday records the public URL, publish time, tags, initial reaction state, and next measurement checkpoint in the Vault.

Safety rule: the midday automation must not publish if the article score is below 80/100, note is logged out or blocks publishing, the content contains invented claims/metrics, or there is no concrete proof artifact.

## 2026-05-19 Policy Update

note記事は `company/marketing/content-plan/note/` 配下でカテゴリ別に管理する。

- `note/coffee/`: コーヒー単体記事。
- `note/AI/`: AI単体記事。
- `note/MBTI/`: `mbti-lovetype.com` の相性診断関連記事。定期更新とサイテーション強化の対象。
- `note/bridge/`: コーヒー×AIなどの例外的な橋渡し記事。

毎日のnote制作目標は3本にする。

1. coffee記事を1本作る。
2. AI記事を1本作る。
3. MBTI記事を1本作る。

公開できない場合も、各レーンで記事ファイル、出典、構成、次アクションを残す。

webサービス制作を別プロジェクトとして追加する。

1. Morning: webサービスの企画を行い、対象ユーザー、解決する痛み、最小機能、今日の実装範囲を決める。
2. Midday: `Projects/` 配下でコーディングまたは最小プロトタイプ作成を行う。
3. Evening: 動作確認、未完了、改善点、翌日の最小TODOをフィードバックとして残す。

## 2026-06-24 Codex Implementation Meeting Gate

Codex が GitHub Issue や project 実装を直接扱う場合、朝会が未実施の状態であれば、実装前に短い全体MTGを挟む。

目的は新しい会議を増やすことではなく、会社全体の優先順位、marketing / PM / engineering の影響、完了条件を1回だけ揃えてから実装することである。

実装前MTGの最小確認:

1. Issue または実装対象は、現在の Main Focus と矛盾しないか。
2. marketing / content / sales に戻すべき成果物や告知材料があるか。
3. Codex が扱う slice は1つに絞れているか。
4. 完了条件は test / lint / diff / source / human review のどれで確認するか。
5. 作業結果を `company/notes/`、`company/projects/`、`company/decisions/` のどこへ戻すか。

朝会が既に実施済みで、同じ内容が handoff note や project note に残っている場合は、追加MTGを省略してよい。
