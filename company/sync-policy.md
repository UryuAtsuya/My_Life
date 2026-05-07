# Company Sync Policy

## 方針

ローカルの `.company/` は日々の運用場所、`My_Life/company/` はGitHub上で見返す整理場所として扱う。

## 同期ルール

- `.company/` 配下のTODO、意思決定、メモ、プロジェクト情報を更新したら、必要な内容を `My_Life/company/` にも反映する
- My_Life側に反映した変更は、作業完了時に `git commit` して `git push` する
- 公開・共有に向く要約を優先し、ローカル専用の詳細ログは必要に応じて整理してから載せる

## 同期先

- GitHub: `https://github.com/UryuAtsuya/My_Life`
- Local: `/Users/uryuatsuya/Documents/ObsidianVault/My_Life`

## 基本フロー

1. `.company/` を更新する
2. GitHubに残すべき内容を `My_Life/company/` へ反映する
3. `git status` で差分を確認する
4. `git commit` する
5. `git push` する

