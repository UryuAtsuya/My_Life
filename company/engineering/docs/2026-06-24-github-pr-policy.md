# GitHub / PR 運用ルール

## 目的

実装作業を本人が安全に確認して merge できる状態で GitHub に出す。

## 共通ルール

- 作業開始時は原則として新しい branch を作る。
- branch 名は `feature/<topic>`、`fix/<topic>`、`docs/<topic>` のいずれかを基本にする。
- `main` への直接実装 push はしない。
- 変更が終わったら、必要な検証を1つ以上行ってから commit する。
- push 後は Pull Request を作成する。
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く。
- merge 判断は原則ユーザーが行う。agent は merge 可能な状態を作るところまでを担当する。
- 緊急時やユーザーが明示した場合を除き、agent は勝手に merge しない。

## 標準フロー

1. `git status --short --branch` で現状を確認する。
2. 未完了の無関係な差分がある場合は触らず、今回の対象を明確にする。
3. `git switch -c <branch>` で作業 branch を作る。
4. 最小 slice を実装する。
5. `test`、`lint`、`diff review`、`source check`、`human review` のいずれかで確認する。
6. 共有対象だけを `git add` する。
7. commit して push する。
8. PR を作成し、日本語で変更内容と確認結果を書く。
9. PR URL と未解決事項を `company/` または対象 project note に戻す。

## PR 本文テンプレート

```markdown
## 何をやったか

- TODO

## なぜやったか

- TODO

## 確認したこと

- [ ] TODO

## 未解決事項

- なし
```

## 例外

- docs や company note だけの軽微な更新でも、共有・レビューが必要なら PR にする。
- automation memory や緊急の同期記録など、即時反映が目的の小変更は直接 push を許可する。ただし commit message と最終報告に理由を書く。
- production branch への昇格は、検証済み branch から PR を作り、ユーザー merge を基本にする。

## 記録先

- MyLife 全体の運用判断: `company/sync-policy.md`
- 技術的な反復ルール: `company/engineering/docs/`
- プロジェクト別の状態: `Projects/README.md` または `company/projects/`
- PR 作成後の引き継ぎ: 対象 project note、handoff note、または `company/notes/`
