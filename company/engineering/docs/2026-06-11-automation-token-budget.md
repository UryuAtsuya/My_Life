---
date: "2026-06-11"
type: engineering-policy
status: active
---

# Automation Token Budget

## 変更前

- 朝・昼・夜を毎日実行: 21 run/週
- 固定 prompt: 合計約1,700語/日
- automation memory: 合計約6,700語
- 未完了時も調査、Top 3、handoff、closeoutを複製

## 変更後

| Automation | 頻度 | Reasoning | 役割 |
|---|---:|---|---|
| Morning planning | 月曜のみ | low | 週の優先順位、既存run確認、短い読み物2本 |
| Midday implementation | 平日 | medium | 1日1 sliceの実装・検証 |
| Evening closeout | 水曜・金曜 | low | 中間監査と週次closeout |

- scheduled runs: 8回/週
- run数削減: 約62%
- promptは参照型に短縮
- memoryは履歴追記をやめ、現在状態だけに置換
- 外部調査は前回情報が古いか、実装判断に必要な場合だけ実行
- 月曜の読み物はITとコーヒーを各600〜1,000字、各3ソース以内に制限

## 週次ガード

- 1 run で複数の大きな実装 sliceを扱わない
- 同一 blocker は再調査せず、解除条件だけ確認する
- 読み物は `company/reading/` に限定し、PM/TODO文書へ展開しない
- 木曜終了時点で未完了が多い場合、金曜は新規着手せずcloseoutを優先する
- token上限接近が疑われる場合、調査系runを止めて実装・検証runを優先する

## 成功指標

- 7日間 automation が停止しない
- implementation start rate 90%以上
- 同一TODOの無変更複製 0件
- automation memory 1ファイル120行以下
- prompt 1本250語以下
