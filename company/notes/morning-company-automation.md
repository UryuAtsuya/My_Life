# Company Daily Automation

## Purpose

Run company operations through three daily Codex automations: morning planning, midday production, and evening closeout.

## Daily Flow

1. Morning: create/update today's TODO, choose priorities, run a business meeting, and record decisions.
2. Midday: pick the top executable TODO and actually produce, implement, publish, measure, or prepare the concrete artifact.
3. Evening: close the day, summarize completed work and blockers, carry unfinished tasks into tomorrow, and sync changes.

## Automations

- ID: `morning-company-business-meeting`
- Name: Morning company business meeting
- Time: every day at 8:00
- Role: planning, TODO, priorities, meeting summary, decisions
- Status: ACTIVE

- ID: `midday-company-production-session`
- Name: Midday company production session
- Time: every day at 12:30
- Role: implementation, production, posting preparation, measurement setup, PM/project updates
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
