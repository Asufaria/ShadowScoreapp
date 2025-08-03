@echo off
echo ShadowScore アプリケーション テスト実行
echo ==========================================

REM 仮想環境をアクティベート
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo 仮想環境をアクティベートしました
) else (
    echo 仮想環境が見つかりません。
    echo 以下のコマンドを実行してください：
    echo python -m venv .venv
    echo .venv\Scripts\activate.bat
    echo pip install -r requirements.txt
    pause
    exit /b 1
)

REM 必要なパッケージをインストール
echo.
echo 必要なパッケージを確認中...
pip install -r requirements.txt

REM アプリケーション実行
echo.
echo アプリケーションを起動しています...
echo アクセス URL: http://localhost:8000
echo 停止するには Ctrl+C を押してください
echo ==========================================
echo.

python startup.py

echo.
echo アプリケーションが停止しました。
pause
