---
created: "2026-05-11"
project: "note-article-flow"
assignee: "codex"
priority: high
status: done
---

# 朝リサーチ・昼note投稿 automation 役割分担

## 内容

毎日の会社automationを、note編集部OSに合わせて役割分担する。

## 決定

- 朝: note市場・AI活用事例・急上昇トピック・既存記事を調査し、昼に書く1本を決める。
- 昼: 朝の調査を使い、記事作成、採点、アイキャッチプロンプト、noteブラウザ投稿、公開URL記録まで行う。

## 完了条件

- [x] `morning-company-business-meeting` のpromptへnoteリサーチ役割を反映
- [x] `midday-company-production-session` のpromptへnote記事作成/投稿役割を反映
- [x] Vaultの運用文書へ役割分担を記録
- [x] 昼automationが `投稿する` まで実行してよい条件を明記

## 公開条件

昼automationは、選定された当日note記事について以下を満たす場合だけ `投稿する` まで実行してよい。

- 記事採点80点以上
- 具体的な証拠素材がある
- 根拠のない数値・実績を含まない
- noteにログイン済みで公開設定へ進める
- 公開後にURL、公開時刻、タグ、初動状態をVaultへ記録できる

## 変更したローカルautomation

- `/Users/uryuatsuya/.codex/automations/morning-company-business-meeting/automation.toml`
- `/Users/uryuatsuya/.codex/automations/midday-company-production-session/automation.toml`
