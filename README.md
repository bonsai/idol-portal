# idol-portal（アイドル民俗学プロジェクト 統合ポータル）

3つのリポジトリ（idol-quiz / idol-lab / idol-oshare）を横断する統合ポータル。加えて、共有オントロジーから派生した可視化成果物をまとめる。

## 構成
- `index.html` — 統合ポータル（クイズ・論文・MEETing・オントロジー可視化の入り口）
- `ontology.ttl` — ローカル TTL（再生成用コピー）
- `build_ontology_artifacts.py` — TTL から以下を生成するスクリプト
- `ontology.sqlite` — RDF トリプル格納（168トリプル）
- `ontology.graph.html` — 概念グラフ（vis-network）
- `ontology.graph.json` — グラフ JSON（nodes/edges, 38/42）
- `ontology.dot` — Graphviz DOT

## 関連リポジトリ（姉妹）
- クイズ: [bonsai/idol-quiz](https://github.com/bonsai/idol-quiz)
- 論文／概念ラボ: [bonsai/idol-lab](https://github.com/bonsai/idol-lab)
- ミーティングボード（オントロジー正源）: [bonsai/idol-oshare](https://github.com/bonsai/idol-oshare)

> オントロジー `ontology.ttl` の正源は idol-oshare。本リポジトリの TTL は再生成・閲覧用のコピー。
