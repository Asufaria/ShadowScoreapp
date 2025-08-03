# ShadowScore

Shadowverse Worlds BEYOND特殊大会用のスコア計測Webアプリケーションです。

![GitHub](https://img.shields.io/github/license/username/shadowscore)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)

## ✨ 特徴

- 🎮 **リアルタイムスコア計算** - エーテル値ベースの即座なポイント計算
- 📊 **ターン管理** - ターンごとの詳細な記録と管理
- 📝 **対戦履歴** - 過去の対戦データの保存と表示
- 🎯 **特殊ルール対応** - Shadowverse Worlds BEYOND大会の計算ロジック
- 📁 **ログ機能** - 全操作の詳細ログ記録
- 📦 **簡単配布** - 実行ファイル形式での配布対応

## 🚀 クイックスタート

### 📥 配布版（推奨）
1. [リリースページ](../../releases)から最新の`ShadowScore-vX.X.X.zip`をダウンロード
2. ZIPファイルを解凍
3. 解凍したフォルダ内の`ShadowScore.exe`をダブルクリックで実行
4. ブラウザで http://localhost:8000 にアクセス

### 🛠️ 開発版

#### 前提条件
- Python 3.8+
- pip

#### セットアップ
```bash
# リポジトリをクローン
git clone https://github.com/username/shadowscore.git
cd shadowscore

# 仮想環境作成
python -m venv .venv

# 仮想環境アクティベート
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 依存関係インストール
pip install -r requirements.txt

# アプリケーション起動
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 計算ルール

### 基本スコア
- **フォロワー** - 生成エーテル値そのまま
- **スペル** - 生成エーテル値そのまま  
- **アミュレット** - 生成エーテル値そのまま
- **アクトアミュレット** - 生成エーテル値の1/3（切り捨て）

### 勝利ボーナス
- 勝利プレイヤーの総ポイントを**2倍**

### レアリティ対応
| レアリティ | エーテル値 |
|-----------|-----------|
| ブロンズ   | 200       |
| シルバー   | 400       |
| ゴールド   | 800       |
| レジェンド | 3,500     |

## 🏗️ ビルド

### 実行ファイル作成
```bash
# Windows
.\build.bat

# 手動ビルド
pyinstaller shadowscore.spec
```

生成されたファイル: `dist/ShadowScore.exe`

## 📁 プロジェクト構成

```
shadowscore/
├── main.py                 # メインアプリケーション
├── models.py              # データモデル定義
├── data_store.py          # データ永続化
├── score_calculator.py    # スコア計算ロジック
├── logger_config.py       # ログ設定
├── startup.py             # ポータブル実行用
├── static/                # Webインターフェース
│   ├── index.html
│   ├── script.js
│   └── style.css
├── shadowscore.spec       # PyInstallerビルド設定
├── build.bat              # ビルドスクリプト
├── requirements.txt       # Python依存関係
└── README.md
```

## 🔧 API エンドポイント

### 対戦管理
- `POST /api/match/new` - 新規対戦作成
- `POST /api/match/{id}/finish` - 対戦終了
- `DELETE /api/match/{id}` - 対戦削除
- `GET /api/match/list` - 対戦一覧取得

### スコア管理
- `POST /api/match/{id}/button` - ボタン入力でスコア追加
- `GET /api/match/{id}/score` - 現在スコア取得
- `GET /api/match/{id}/history` - 対戦履歴取得

詳細は http://localhost:8000/docs を参照

## 📋 ログ機能

- **場所**: `logs/shadowscore_YYYYMMDD.log`
- **ローテーション**: 10MB/ファイル、最大5ファイル
- **記録内容**: 
  - アプリケーション開始/停止
  - 対戦作成/終了
  - スコア操作
  - エラー情報

## 🤝 コントリビューション

1. フォークを作成
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成

## 📄 ライセンス

## 📚 ドキュメント

- 📖 **[ユーザーガイド](docs/USER_GUIDE.md)** - 詳細な使用方法
- 🚀 **[クイックスタート](docs/QUICKSTART.html)** - 簡単セットアップガイド
- 📄 **[配布版README](README_配布版.md)** - エンドユーザー向け説明

## 📄 ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## 🐛 バグ報告・機能要求

[Issues](../../issues)ページで報告してください。以下の情報を含めてください：
- 実行環境（OS、Pythonバージョン）
- 再現手順
- エラーメッセージ
- ログファイル（該当部分）

## 📞 サポート

- 📧 Email: [your-email@example.com]
- 🐦 Twitter: [@youraccount]
- 💬 Discord: [Server Link]

---

© 2024 ShadowScore Team
