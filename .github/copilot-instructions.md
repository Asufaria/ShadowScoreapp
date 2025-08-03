<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# ShadowScore プロジェクト用 Copilot 指示

このプロジェクトは、Shadowverse Worlds BEYOND特殊大会用のスコア計測Webアプリケーションです。

## プロジェクト概要
- FastAPIを使用したPythonバックエンド
- エーテル値ベースのポイント計算システム
- ターン管理とリアルタイムスコア計算
- 対戦履歴の保存と管理機能

## コーディング指針
- Pydanticモデルを使用したデータバリデーション
- 適切なHTTPステータスコードの使用
- エラーハンドリングの実装
- 日本語コメントでの説明
- RESTful APIの設計原則に従う

## 計算ロジック
- フォロワー、スペル、アミュレット: 生成エーテル値そのまま
- アクトしたアミュレット: 生成エーテル値の1/3（切り捨て）
- 勝利時: 総ポイントを2倍
