# アイドルポータル計画書

## プロジェクト概要
- **名前**: idol-portal
- **言語**: Python
- **目的**: アイドル情報の一元管理ポータル

## 機能一覧

### 1. データ管理
- アイドルプロフィールCRUD
- グループ管理
- イベント管理
- メンバー変更履歴

### 2. 可視化
- グループ構成図
- イベントカレンダー
- 人気ランキング
- 統計ダッシュボード

### 3. 検索・フィルタ
- 名前検索
- グループ別フィルタ
- ジャンル別絞り込み

## 技術スタック

| レイヤー | ツール | 用途 |
|---------|--------|------|
| フレームワーク | FastAPI | REST API |
| DB | SQLite | データ永続化 |
| ORM | SQLAlchemy | DB操作 |
| 可視化 | Plotly | グラフ描画 |
| フロント | Streamlit | UI表示 |

## ディレクトリ構成
```
repos/idol/
├── app/
│   ├── main.py
│   ├── models.py
│   ├── routes/
│   └── templates/
├── data/
│   └── idol.db
├── requirements.txt
└── README.md
```

## 実装ステップ

### Phase 1: 基盤構築
1. ディレクトリ作成
2. 依存関係インストール
3. DBスキーマ定義
4. モデルクラス実装

### Phase 2: API実装
1. アイドルCRUD
2. グループ管理
3. イベント管理

### Phase 3: UI実装
1. Streamlitダッシュボード
2. 検索・フィルタ機能
3. 可視化グラフ

## データ仕様

### アイドル
```json
{
  "id": "string",
  "name": "string",
  "group_id": "string",
  "birth_date": "date",
  "blood_type": "string",
  "hobby": "string",
  "image_url": "string"
}
```

### グループ
```json
{
  "id": "string",
  "name": "string",
  "debut_date": "date",
  "agency": "string",
  "member_count": "integer"
}
```

### イベント
```json
{
  "id": "string",
  "title": "string",
  "date": "datetime",
  "venue": "string",
  "group_id": "string",
  "type": "string"
}
```

## 次のアクション
1. 計画書確認
2. 承認後Phase 1開始
