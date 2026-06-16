---
date: "2026-06-16"
type: weekly-reading
category: it-trends
---

# AIエージェントは「使えるか」から「測れるか」へ

## 今週なにが起きたか

GitHubは6月11日、AI usage reportでGitHub AI Creditsの使用量と金額を標準フィールドに反映した。6月のChangelogでは、Copilot cloud agentのsessionをChatから検索・参照できる更新や、Agent tasks REST APIでcloud agent taskを開始・追跡する更新も並んでいる。OpenAIもOna買収計画を発表し、Codexを長時間動くagent向けの安全なcloud環境へ広げる方向を示した。

## 何が面白いか

AI開発ツールの差は、モデル性能だけでは見えにくくなっている。実務では「誰が、どのtaskで、いくら使い、どの成果に結びついたか」を追えないと、便利でも運用に乗らない。たとえばcode review agentを毎PRで走らせるなら、指摘数だけでなく、blocker検出、修正commit、再実行回数、credit消費を同じ単位で見る必要がある。session検索やusage reportは地味だが、agentをチームの作業台帳に入れるための基礎になる。

## 自分の作業にどう関係するか

XGuardでも、Codex handoffを「feature branch」「閉じるgate」「検証command」「staging昇格可否」「重い検証の要否」の5項目で記録する。次に試すことは、各sliceのcloseoutに「追加で回す価値がある検証」と「今は回さない検証」を1行ずつ書くこと。

## 出典

- [GitHub Changelog: AI usage report updates](https://github.blog/changelog/2026-06-11-ai-usage-report-updates/) - 確認日: 2026-06-16
- [GitHub Changelog: 06/2026](https://github.blog/changelog/month/06-2026/) - 確認日: 2026-06-16
- [OpenAI: OpenAI to acquire Ona](https://openai.com/index/openai-to-acquire-ona/) - 確認日: 2026-06-16
