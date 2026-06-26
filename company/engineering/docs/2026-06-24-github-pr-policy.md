# GitHub / PR 運用ルール

## 目的

実装作業を本人が安全に確認して merge できる状態で GitHub に出す。

## 共通ルール

- 作業開始時は原則として新しい branch を作る。
- コーディングタスクは、可能な限り GitHub Issue を起点にする。
- Issue 作成前に、同じ目的の open Issue / PR がないか確認する。
- branch 名は `feature/<topic>`、`fix/<topic>`、`docs/<topic>` のいずれかを基本にする。
- `main` への直接実装 push はしない。
- 変更が終わったら、必要な検証を1つ以上行ってから commit する。
- push 後は Pull Request を作成する。
- PR 本文は日本語で「何をやったか」「なぜやったか」「確認したこと」「未解決事項」を書く。
- PR 本文には対応 Issue を `Closes #<number>` または関連リンクで明記する。
- merge 判断は原則ユーザーが行う。agent は merge 可能な状態を作るところまでを担当する。
- 緊急時やユーザーが明示した場合を除き、agent は勝手に merge しない。

## 標準フロー

1. `git status --short --branch` で現状を確認する。
2. 未完了の無関係な差分がある場合は触らず、今回の対象を明確にする。
3. GitHub Issue が未作成なら、objective、owner、success check、required artifacts を入れて起票する。
4. 同じ目的の open Issue / PR が既にある場合は、新規作成せず既存 Issue を継続する。
5. `git switch -c <branch>` で作業 branch を作る。
6. 最小 slice を実装する。
7. `test`、`lint`、`diff review`、`source check`、`human review` のいずれかで確認する。
8. 共有対象だけを `git add` する。
9. commit して push する。
10. PR を作成し、日本語で変更内容と確認結果を書く。
11. PR URL と未解決事項を `company/` または対象 project note に戻す。
12. 必要なら証拠 md を作り、Issue、PR、branch、commit、verification、unresolved を記録する。

## Issue / PR / 証拠 md の状態

- `issue_created`: GitHub Issue が作成済み。
- `implementation_started`: 対応 branch が作成済み。
- `implemented`: commit が作成済み。
- `pr_opened`: Pull Request が作成済み。
- `merged`: Pull Request が merge 済み。
- `recorded`: MyLife 側に証拠 md または project note が残っている。

証拠 md は小さく保つ。標準の保存先は、全体運用なら `company/evidence/`、プロジェクト固有なら `Projects/<project>/evidence/` または `company/projects/<project>/notes/` とする。

```markdown
# YYYY-MM-DD <作業名>

- Repo:
- Issue:
- PR:
- Branch:
- Commit:
- Status:
- Success check:
- Verification:
- Unresolved:
- Next:
```

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
- Issue / PR / commit の証拠: `company/evidence/`、`Projects/<project>/evidence/`、または対象 project note
