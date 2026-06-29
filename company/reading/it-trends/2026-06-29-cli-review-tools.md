---
date: "2026-06-29"
type: weekly-reading
category: it-trends
---

# AI codingは、CLIとreviewの作業面に寄ってきた

## 今週なにが起きたか

GitHubは6月23日、Copilot CLIの新しいterminal interfaceを一般提供にした。tabでissue、PR、gistを扱い、tool設定もterminal側で済ませやすくする更新だ。6月25日にはCopilot code reviewが`grep`、`rg`、`glob`、`view`を使ってrepositoryを探索するようになった。さらに同日、Jira上でcoding agentの進行状況をstreaming表示できるCopilot for Jiraも一般提供になった。

## 何が面白いか

AI codingの焦点が「chatで答える」から「開発者が普段いる作業面に入り、根拠を探し、進行を見せる」へ寄っている。CLIはterminalで作業単位を切り替え、reviewは`rg`相当の探索で差分だけでなく周辺コードを読む。Jira連携は、agentが何をしているかをPM側の画面にも戻す。これはXGuardのように、branch、検証、blockerを小さく管理するworkflowと相性がよい。

## 自分の作業にどう関係するか

次に試すことは、Codex handoffを「探索command、見るfile、期待する検証、戻すstatus」の4点で始めること。reviewには実装意図より先に、`rg`で確認してほしい契約、例えば`main`直接push禁止、raw X API payload非公開、token material非露出を渡す。

## 出典

- [GitHub Changelog: Copilot CLI: New terminal interface is generally available](https://github.blog/changelog/2026-06-23-copilot-cli-new-terminal-interface-is-generally-available/) - 確認日: 2026-06-29
- [GitHub Changelog: Copilot code review: Analysis depth and efficiency updates](https://github.blog/changelog/2026-06-25-copilot-code-review-analysis-depth-and-efficiency-updates/) - 確認日: 2026-06-29
- [GitHub Changelog: GitHub Copilot for Jira is now generally available](https://github.blog/changelog/2026-06-25-github-copilot-for-jira-is-now-generally-available/) - 確認日: 2026-06-29
