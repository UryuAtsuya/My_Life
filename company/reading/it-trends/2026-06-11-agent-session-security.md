# AIエージェントは「生成」より引き継ぎと検証の時代へ

## 今週なにが起きたか

GitHubは6月9日、第三者のcoding agentが作ったコードにも、CodeQL、依存関係の脆弱性照合、secret scanningを自動適用した。翌10日にはCopilot Chatからagent sessionの進行確認、完了ログや過去sessionの検索が可能になった。Copilot CLIにはlocal差分を調べる`/security-review`も加わった。

## 何が面白いか

焦点が「AIにコードを書かせる」から「同じ検証を通し、理由を追える」へ移っている。sessionごとに前提が失われれば運用コストは下がらない。変更差分・検証結果・session logを一つの流れで扱うことが品質の中心になる。

認証境界を変更するPRなら、targeted test、型検査、secret scanning、変更理由を同じsessionに残す。次の担当者は未確認事項から再開できる。

## 次に試すこと

XGuard実装で、1 sliceごとに「目的、変更ファイル、検証、未確認条件」を4行でcloseoutする。security reviewは既存testやCodeQLの代替にはしない。

## 出典

- [GitHub: Security validation for third-party coding agents](https://github.blog/changelog/2026-06-09-security-validation-for-third-party-coding-agents/)
- [GitHub: Copilot Chat now sees your agent sessions](https://github.blog/changelog/2026-06-10-copilot-chat-now-sees-your-agent-sessions/)
- [GitHub: Dedicated security review command](https://github.blog/changelog/2026-06-10-dedicated-security-review-command-now-available-in-copilot-cli/)
