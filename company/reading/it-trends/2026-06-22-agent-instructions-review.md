---
date: "2026-06-22"
type: weekly-reading
category: it-trends
---

# AIレビューは、repoの作法を読む段階に入った

## 今週なにが起きたか

GitHubは6月18日、Copilot code reviewがrepository rootの`AGENTS.md`を参照するようになったと発表した。同じ週には、Copilot cloud agentが作ったPRを`author:@me`検索に含める更新も出た。6月19日には、Copilot usage metrics APIにuser別AI credits消費が追加された。

## 何が面白いか

AI coding agentの課題は「コードを書けるか」から「チームの作法、責任、コストに接続できるか」へ移っている。`AGENTS.md`対応は小さく見えるが、review観点をchatの記憶ではなくrepo内の契約に寄せる変化だ。XGuardなら、`main`直接push禁止、raw X API payload非公開、token materialをfrontendに出さない、といった制約をレビューが拾いやすくなる。agent作成PRの検索とusage APIが揃うと、「誰の依頼で、どのbranchに、いくら使ったか」も追える。

## 自分の作業にどう関係するか

次に試すことは、XGuardのhandoffを`AGENTS.md`の制約に合わせて「禁止事項、branch遷移、検証command、未確認blocker」の4点で始めること。レビューagentには実装説明より先に、repo契約違反を見せる。

## 出典

- [GitHub Changelog: Copilot code review: AGENTS.md support and UI improvements](https://github.blog/changelog/2026-06-18-copilot-code-review-agents-md-support-and-ui-improvements/) - 確認日: 2026-06-22
- [GitHub Changelog: Copilot-authored pull requests now included in author searches](https://github.blog/changelog/2026-06-18-copilot-authored-pull-requests-now-included-in-author-searches/) - 確認日: 2026-06-22
- [GitHub Changelog: AI credits consumed per user now in the Copilot usage metrics API](https://github.blog/changelog/2026-06-19-ai-credits-consumed-per-user-now-in-the-copilot-usage-metrics-api/) - 確認日: 2026-06-22
