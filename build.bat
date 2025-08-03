@echo off
chcp 65001 >nul
echo ShadowScore アプリケーション ビルドスクリプト
echo ===============================================

REM 仮想環境をアクティベート
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo 仮想環境をアクティベートしました
) else (
    echo 仮想環境が見つかりません。python -m venv .venv を実行してください。
    pause
    exit /b 1
)

REM 必要なパッケージをインストール
echo.
echo 必要なパッケージをインストール中...
pip install -r requirements.txt

REM ビルド実行
echo.
echo アプリケーションをビルド中...
pyinstaller shadowscore.spec

REM ビルド結果を確認
if exist "dist\ShadowScore.exe" (
    echo.
    echo ========================================
    echo ビルド完了！
    echo 実行ファイル: dist\ShadowScore.exe
    echo ========================================
    echo.
    echo distフォルダを配布用にコピーしてください。
    echo アプリケーションを起動するには ShadowScore.exe を実行してください。
) else (
    echo.
    echo ビルドに失敗しました。
    echo エラーログを確認してください。
)

echo.
pause
