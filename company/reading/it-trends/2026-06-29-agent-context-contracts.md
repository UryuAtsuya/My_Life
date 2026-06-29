---
date: "2026-06-29"
category: it-trends
---

# agent context contracts

今週の開発ツール周りで面白いのは、AI coding agentの競争軸が「賢い返答」から「長い作業をどこで継続し、どう承認するか」へ移っていること。OpenAIのCodex changelogでは、6月25日にCodex RemoteがGAになり、mobileからconnected host上の作業を開始・継続し、進捗確認や承認をできるようになった。GitHub Copilot CLIも6月23日に新しいterminal interfaceをGA化し、repository内のIssues / Pull requestsをtabで見ながら、対象をpromptへ差し込めるようにしている。さらにOpenAIは、Codex利用が長時間タスクに広がっており、30分超・1時間超・8時間超の仕事見積もりに相当するrequestが増えていると報告した。

ここから見える実務上の変化は、agentへ毎回長いpromptを貼るより、repo内の`AGENTS.md`、automation memory、handoff noteを短く保ち、最新状態だけを読ませる設計の価値が上がっている点だ。remote hostやterminal tabで作業が続くほど、「今どのbranchで、何をmergeし、何を承認するか」がprompt外の契約として残っていないと迷いやすい。XGuardでも、`develop`をstaging、`main`をproductionとして扱うbranch contractや、`feature/*`から`develop`へ統合するhandoffを文書化しておけば、review agentと実装agentの判断が揃いやすい。

次に試すことは、XGuardの次sliceで「agentが読むべき3点」を固定すること。`AGENTS.md`、最新weekly planning、automation memoryだけを入口にし、読み物や過去TODOは参照扱いに落とす。これで毎回のtokenを抑えつつ、branch・blocker・昇格順序の誤読を減らせる。

出典:
- [OpenAI: How agents are transforming work](https://openai.com/index/how-agents-are-transforming-work/)
- [OpenAI Developers: Codex changelog](https://developers.openai.com/codex/changelog)
- [GitHub Changelog: Copilot CLI new terminal interface](https://github.blog/changelog/2026-06-23-copilot-cli-new-terminal-interface-is-generally-available/)
