@echo off
chcp 65001 >nul 2>&1
echo ShadowScore Application Build Script
echo ===================================

REM Activate virtual environment
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
    echo Virtual environment activated
) else (
    echo Virtual environment not found. Please run: python -m venv .venv
    pause
    exit /b 1
)

REM Install required packages
echo.
echo Installing required packages...
pip install -r requirements.txt

REM Build application
echo.
echo Building application...
pyinstaller shadowscore.spec

REM Check build result
if exist "dist\ShadowScore.exe" (
    echo.
    echo ========================================
    echo Build completed!
    echo Executable: dist\ShadowScore.exe
    echo ========================================
    
    REM Create distribution package
    echo.
    echo Creating distribution package...
    
    REM Clean up old files
    if exist "ShadowScore-v1.4.0.zip" del /Q "ShadowScore-v1.4.0.zip"
    if exist "ShadowScore-v1.4.0\" rmdir /S /Q "ShadowScore-v1.4.0\"
    
    REM Create distribution directory
    mkdir "ShadowScore-v1.4.0"
    
    REM Copy files
    copy "dist\ShadowScore.exe" "ShadowScore-v1.4.0\"
    if exist "README_配布版.md" copy "README_配布版.md" "ShadowScore-v1.4.0\"
    if exist "docs\QUICKSTART.html" copy "docs\QUICKSTART.html" "ShadowScore-v1.4.0\"
    if exist "docs\USER_GUIDE.md" copy "docs\USER_GUIDE.md" "ShadowScore-v1.4.0\"
    
    REM Create directories
    mkdir "ShadowScore-v1.4.0\data"
    mkdir "ShadowScore-v1.4.0\logs"
    
    REM Create ZIP file
    echo Creating ZIP file...
    powershell -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'ShadowScore-v1.4.0\*' -DestinationPath 'ShadowScore-v1.4.0.zip' -Force"
    
    if exist "ShadowScore-v1.4.0.zip" (
        echo.
        echo ========================================
        echo Distribution package created:
        echo    - Folder: ShadowScore-v1.4.0\
        echo    - ZIP file: ShadowScore-v1.4.0.zip
        echo ========================================
    ) else (
        echo.
        echo ZIP file creation failed
    )
    
) else (
    echo.
    echo Build failed.
    echo Check error logs.
)

echo.
pause
