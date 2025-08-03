"""
ポータブル実行用スタートアップスクリプト
設定とデータを実行ファイルと同じディレクトリに保存
"""

import os
import sys
from pathlib import Path


def setup_portable_environment():
    """ポータブル実行環境のセットアップ"""
    
    # 実行ファイルのディレクトリを取得
    if getattr(sys, 'frozen', False):
        # PyInstallerでビルドされた場合
        app_dir = Path(sys.executable).parent
    else:
        # 開発環境の場合
        app_dir = Path(__file__).parent
    
    # データディレクトリの設定
    data_dir = app_dir / "data"
    logs_dir = app_dir / "logs"
    
    # ディレクトリ作成
    data_dir.mkdir(exist_ok=True)
    logs_dir.mkdir(exist_ok=True)
    
    # 環境変数で設定
    os.environ['SHADOWSCORE_DATA_DIR'] = str(data_dir)
    os.environ['SHADOWSCORE_LOGS_DIR'] = str(logs_dir)
    
    return app_dir, data_dir, logs_dir


def main():
    """メイン実行関数"""
    
    # ポータブル環境のセットアップ
    app_dir, data_dir, logs_dir = setup_portable_environment()
    
    print("ShadowScore アプリケーション")
    print("=" * 40)
    print(f"アプリケーションディレクトリ: {app_dir}")
    print(f"データディレクトリ: {data_dir}")
    print(f"ログディレクトリ: {logs_dir}")
    print("=" * 40)
    
    # メインアプリケーションをインポートして実行
    try:
        import uvicorn
        from main import app
        
        print("サーバーを起動しています...")
        print("アクセス URL: http://localhost:8000")
        print("停止するには Ctrl+C を押してください")
        print("=" * 40)
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\nアプリケーションを停止しました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        input("何かキーを押してください...")


if __name__ == "__main__":
    main()
