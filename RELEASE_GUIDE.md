# 📦 ShadowScore リリースガイド

## GitHub Releasesでの配布方法

### 1. リリースの作成
1. GitHubリポジトリページで「Releases」タブをクリック
2. 「Create a new release」をクリック
3. タグを作成（例：v1.2.0）
4. リリースタイトルを入力（例：ShadowScore v1.2.0）

### 2. 配布ファイルのアップロード
1. 「Attach binaries by dropping them here or selecting them」で
2. `ShadowScore-v1.2.0.zip` をドラッグ&ドロップ
3. リリースノートを記入

### 3. 公開設定
- ✅ **「Set as the latest release」** をチェック
- ⚠️ プライベートリポジトリの場合、Releaseも制限される場合があります

## 📋 リリースノート例

```markdown
## 🎉 ShadowScore v1.2.0

### ✨ 新機能
- ファイル構成の整理
- 文字化け問題の修正
- ZIP配布形式での提供

### 📦 ダウンロード
1. `ShadowScore-v1.2.0.zip` をダウンロード
2. 任意の場所に解凍
3. `ShadowScore.exe` を実行

### 📊 動作環境
- Windows 10/11
- .NET Framework不要（スタンドアロン実行）

### 🐛 修正内容
- ビルドプロセスの改善
- ドキュメント構成の整理
```

## 🌐 一般公開の選択肢

### Option A: パブリックリポジトリに変更
```
Settings → General → Danger Zone → Change repository visibility
```

### Option B: 別配布方法
- Google Drive / OneDrive での共有
- Discord / Slack での直接配布
- 個人サイト / ブログでの配布

## 🎯 推奨アプローチ

最も簡単で安全な方法：
1. リポジトリをパブリックに変更
2. GitHub Releasesで配布
3. README_配布版.mdのリンクを更新
