@echo off
echo ShadowScore アプリを起動しています...
echo.

REM 仮想環境の存在チェック
if not exist ".venv" (
    echo 仮想環境を作成しています...
    python -m venv .venv
)

REM 仮想環境をアクティベート
call .venv\Scripts\activate.bat

REM 依存関係をインストール
echo 依存関係をインストールしています...
pip install -r requirements.txt

REM アプリケーションを起動
echo.
echo アプリケーションを起動しています...
echo ブラウザで http://localhost:8000 にアクセスしてください
echo 終了するには Ctrl+C を押してください
echo.

python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

pause
