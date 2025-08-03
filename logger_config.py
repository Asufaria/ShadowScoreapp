"""
ログ設定モジュール
ShadowScoreアプリケーション用のログ機能を提供
"""

import logging
import logging.handlers
import os
from datetime import datetime
from pathlib import Path


def setup_logger():
    """ログシステムのセットアップ"""
    
    # ポータブル対応: 環境変数からログディレクトリを取得
    logs_dir_env = os.environ.get('SHADOWSCORE_LOGS_DIR', 'logs')
    log_dir = Path(logs_dir_env)
    log_dir.mkdir(exist_ok=True)
    
    # ログファイル名（日付付き）
    log_filename = log_dir / f"shadowscore_{datetime.now().strftime('%Y%m%d')}.log"
    
    # ルートロガーの設定
    logger = logging.getLogger("shadowscore")
    logger.setLevel(logging.INFO)
    
    # 既存のハンドラーをクリア（重複防止）
    logger.handlers.clear()
    
    # フォーマッターの設定
    formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # ファイルハンドラー（ローテーション機能付き）
    file_handler = logging.handlers.RotatingFileHandler(
        log_filename,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # コンソールハンドラー
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # アプリケーション開始ログ
    logger.info("=" * 50)
    logger.info("ShadowScore アプリケーション開始")
    logger.info(f"ログファイル: {log_filename}")
    logger.info(f"データディレクトリ: {os.environ.get('SHADOWSCORE_DATA_DIR', '.')}")
    logger.info("=" * 50)
    
    return logger


def get_logger():
    """ロガーインスタンスを取得"""
    return logging.getLogger("shadowscore")


# アプリケーション起動時にログシステムを初期化
main_logger = setup_logger()
