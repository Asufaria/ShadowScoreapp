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

# ビルド結果を確認
if exist "dist\ShadowScore.exe" (
    echo.
    echo ========================================
    echo ビルド完了！
    echo 実行ファイル: dist\ShadowScore.exe
    echo ========================================
    
    REM 配布用ZIPファイルを作成
    echo.
    echo 配布用ZIPファイルを作成中...
    
    REM 古いZIPファイルがあれば削除
    if exist "ShadowScore-v*.zip" del "ShadowScore-v*.zip"
    
    REM 現在の日付でバージョンを作成
    for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
    set "YY=%dt:~2,2%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
    set "version=v1.%YY%.%MM%%DD%"
    
    REM ZIPファイル作成（PowerShellを使用）
    powershell -command "Compress-Archive -Path 'dist\*' -DestinationPath 'ShadowScore-%version%.zip' -Force"
    
    if exist "ShadowScore-%version%.zip" (
        echo ✅ 配布用ZIPファイルを作成しました: ShadowScore-%version%.zip
        echo.
        echo 📋 配布手順:
        echo 1. ShadowScore-%version%.zip をGitHub Releasesにアップロード
        echo 2. または直接配布してください
    ) else (
        echo ❌ ZIPファイルの作成に失敗しました
    )
    
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
