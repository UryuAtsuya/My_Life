# エラーパターン台帳

同じ原因が2回発生した場合に追加する。症状ではなく、原因、検出方法、安全な回復手順、停止条件を残す。

## EPERM on generated output

- Category: `permission`
- Signal: `dist/` または `node_modules/.vite-temp` への書き込みが `EPERM`
- Root cause: sandbox、symlink、checkout の書き込み権限
- Detect: `test -w <path>` と対象ディレクトリの実体確認
- Recover: writable checkout または temp clone で同じ検証を1回再実行
- Stop: writable 環境でも再現した場合は `code_failure` として調査
- Do not: テスト成功として記録しない

## Git remote divergence

- Category: `code_failure`
- Signal: push が `fetch first`、または branch が ahead / behind の両方を持つ
- Root cause: local と remote に別 commit が存在
- Detect: `git fetch origin`、`git log origin/main..HEAD`、`git log HEAD..origin/main`
- Recover: force pushせず、差分確認後に `git rebase origin/main`
- Stop: conflict 時は自動解決せず、対象ファイルと競合理由を記録

## GitHub DNS failure

- Category: `network`
- Signal: `Could not resolve host: github.com`
- Root cause: DNS またはネットワーク到達性
- Detect: `git ls-remote origin` を1回だけ実行
- Recover: commit を保持し、同一 run での再試行は1回まで
- Stop: 2回失敗したら push blocker として終了

## Missing Supabase integration environment

- Category: `environment`
- Signal: DB URL、`psql`、Supabase CLI、Docker のいずれかがない
- Root cause: integration test 前提が未準備
- Detect: secretを表示せず、command availability と env presence のみ確認
- Recover: blocker owner と解除条件を記録し、unit / contract testだけ実行
- Stop: 同じ日次TODOへ複製せず、環境が変わるまでblockedを維持

## Vitest default timeout only

- Category: `environment`
- Signal: full test は5秒 timeout、同じ targeted test は延長 timeout でpass
- Root cause: CI負荷、並列実行、非同期処理の終了待ち、またはテスト自体の遅さ
- Detect: 対象testを単独で1回実行し、実測時間とopen handleを確認
- Recover: assertionを変えず、不要なwait、timer、cleanup漏れを先に調査
- Verify: 標準の `npm run check` がpassすること
- Stop: 延長 timeout でpassしても標準checkは成功扱いにしない
- Do not: 恒久対策なしに全体 timeout だけを引き上げない
