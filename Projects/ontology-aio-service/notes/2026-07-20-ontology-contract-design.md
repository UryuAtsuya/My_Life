# 2026-07-20 AIO Ontology Contract設計

- Objective: 現行のkeyword中心Ontology draftを、サイトEvidenceから説明可能な精密scoreへ接続できる正式Contractへ拡張する
- Slice: Entity / Property / Relationship / Evidence / validation / score formula / migration順を設計し、machine-readable Score Profileを作成
- Decision: `Site → Evidence → Entity / Relationship → CriterionEvaluation → Score` のEvidence-first application ontologyを採用する
- Model: 13 Entity type、15 Relationship、stable ID、candidate / confirmed / rejected状態を定義
- Score: 6 dimensions、28 criteria、`pass / partial / fail / unavailable / not_applicable`、coverage 60%未満はnumeric scoreを出さない
- OWL: `docs/aio-ontology-v1.owl.ttl` にOWL 2 ontologyをTurtle serializationで追加。Entity / Relationship / Evidence / Score Profile参照をmachine-readable化
- Compatibility: 現行7 Entity typeと `/api/ontology/extract` は維持し、新しいv1境界を段階追加する
- AIO Issue: https://github.com/UryuAtsuya/AIO/issues/4
- AIO draft PR: https://github.com/UryuAtsuya/AIO/pull/5
- Verification: OWL 957 triplesをRDFLibでparse・再serializationし、13 Entity、15 Relationship、6 dimension、28 criterion、JSONとのID・重み・文言完全一致、`git diff --check`を確認
- Blocker: Contractはproposed。実装前にowner reviewが必要
- 次の1手: PR #5の設計レビュー後、domain types・profile loader・deterministic evaluator・golden fixtureだけをbackend sliceとして実装する
