# コントリビュートガイド

ShadowScore プロジェクトへのコントリビュートありがとうございます！

## 🚀 開発環境のセットアップ

### 前提条件
- Python 3.8以上
- Git
- テキストエディタ（VS Code推奨）

### セットアップ手順
```bash
# 1. リポジトリをフォーク・クローン
git clone https://github.com/your-username/shadowscore.git
cd shadowscore

# 2. 仮想環境作成
python -m venv .venv

# 3. 仮想環境アクティベート
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 4. 依存関係インストール
pip install -r requirements.txt

# 5. 開発用サーバー起動
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 コーディング規約

### Python コード
- [PEP 8](https://pep8-ja.readthedocs.io/ja/latest/) に従う
- 日本語コメントを使用
- Pydanticモデルを使用したデータバリデーション
- 適切なHTTPステータスコードの使用
- エラーハンドリングの実装

### コミットメッセージ
```
[タイプ] 簡潔な説明

詳細な説明（必要に応じて）

例:
[feat] ログ機能を追加
[fix] スコア計算のバグを修正
[docs] READMEを更新
[refactor] コードを整理
```

### ブランチ命名規則
- `feature/機能名` - 新機能
- `fix/修正内容` - バグ修正
- `docs/更新内容` - ドキュメント更新

## 🔄 開発フロー

1. **Issue 作成**
   - バグ報告や機能要求は Issue で議論

2. **ブランチ作成**
   ```bash
   git checkout -b feature/新機能名
   ```

3. **開発・テスト**
   - コードの実装
   - ローカルでのテスト
   
4. **コミット・プッシュ**
   ```bash
   git add .
   git commit -m "[feat] 新機能を追加"
   git push origin feature/新機能名
   ```

5. **プルリクエスト作成**
   - GitHub でプルリクエストを作成
   - テンプレートに従って記載

## 🧪 テスト

### 基本テスト
```bash
# アプリケーション起動テスト
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 機能テスト
- ブラウザで http://localhost:8000 にアクセス
- 各機能が正常に動作することを確認
- ログファイルが正しく出力されることを確認

## 📁 プロジェクト構造

```
shadowscore/
├── main.py                 # FastAPI アプリケーション
├── models.py              # Pydantic データモデル
├── data_store.py          # データ永続化層
├── score_calculator.py    # ビジネスロジック
├── logger_config.py       # ログ設定
├── startup.py             # エントリーポイント
├── static/                # フロントエンド
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .github/               # GitHub設定
│   ├── workflows/
│   ├── ISSUE_TEMPLATE/
│   └── pull_request_template.md
├── requirements.txt       # 依存関係
├── shadowscore.spec       # PyInstaller設定
└── README.md
```

## 🐛 バグ報告

バグを発見した場合：

1. [既存の Issue](../../issues) を確認
2. 重複がない場合は新しい Issue を作成
3. バグ報告テンプレートに従って記載

### 必要な情報
- 実行環境（OS、Pythonバージョン）
- 再現手順
- 期待される動作
- ログファイル（`logs/` フォルダ）

## ✨ 機能要求

新機能の提案：

1. [既存の Issue](../../issues) を確認
2. 機能要求テンプレートを使用して Issue 作成
3. 必要性と実装案を明確に記載

## 📞 質問・サポート

- 💬 [Discussions](../../discussions) で質問
- 📧 メール: [your-email@example.com]
- 🐛 バグは [Issues](../../issues) で報告

## 📄 ライセンス

コントリビュートしたコードは [MIT License](LICENSE) の下で公開されます。

---

ご協力ありがとうございます！ 🙏
