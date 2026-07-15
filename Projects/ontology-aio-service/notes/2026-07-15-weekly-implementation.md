# 2026-07-15 AIO水曜実装

- Objective: prototypeのURL取得・ページシグナル抽出を本番FastAPIへ段階的に統合する
- Slice: 公開HTTP(S) URLを安全に検証し、単一HTMLからPageSignalを返すbackend境界を追加
- Verification: `backend/.venv/bin/pytest tests/test_page_signals.py tests/test_api.py` — 5 passed
- AIO PR: https://github.com/UryuAtsuya/AIO/pull/1
- Blocker: なし
- 次の1手: PR #1のレビュー後、取得したPageSignalを既存Ontology診断へ直結する最小API境界を実装する
