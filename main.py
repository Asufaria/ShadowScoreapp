from fastapi import FastAPI, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from typing import List
import os

from models import Match, MatchCreate, MatchFinish, TurnInput, ScoreResponse, Turn, ButtonInput
from data_store import data_store
from score_calculator import calculate_turn_score, update_match_score, get_next_player
from logger_config import get_logger

# ポータブル実行対応
try:
    from startup import setup_portable_environment
    setup_portable_environment()
except ImportError:
    # 開発環境では無視
    pass

# ロガーの初期化
logger = get_logger()

app = FastAPI(
    title="ShadowScore API",
    description="Shadowverse Worlds BEYOND 特殊大会用スコア計測API",
    version="1.4.0"
)

# 静的ファイル配信設定
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(current_dir, "static")

if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    logger.info(f"静的ファイルディレクトリをマウント: {static_dir}")
else:
    logger.warning(f"静的ファイルディレクトリが見つかりません: {static_dir}")

# 静的ファイルの直接アクセス用（互換性のため）
@app.get("/style.css")
async def get_style_css():
    """CSSファイルの直接アクセス"""
    css_path = os.path.join(static_dir, "style.css")
    return FileResponse(css_path, media_type="text/css")

@app.get("/script.js")
async def get_script_js():
    """JavaScriptファイルの直接アクセス"""
    js_path = os.path.join(static_dir, "script.js")
    return FileResponse(js_path, media_type="application/javascript")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """メインページ"""
    try:
        import os
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_path = os.path.join(current_dir, "static", "index.html")
        
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        return HTMLResponse(content=content)
    except FileNotFoundError as e:
        logger.error(f"HTMLファイルが見つかりません: {e}")
        return HTMLResponse("""
        <html>
            <head><title>ShadowScore</title></head>
            <body>
                <h1>ShadowScore API</h1>
                <p>Shadowverse Worlds BEYOND 特殊大会用スコア計測API</p>
                <p><a href="/docs">API Documentation</a></p>
                <p>エラー: HTMLファイルが見つかりません</p>
            </body>
        </html>
        """)
    except Exception as e:
        logger.error(f"HTMLファイル読み込みエラー: {e}")
        return HTMLResponse(f"""
        <html>
            <head><title>ShadowScore Error</title></head>
            <body>
                <h1>ShadowScore API - エラー</h1>
                <p>エラーが発生しました: {str(e)}</p>
                <p><a href="/docs">API Documentation</a></p>
            </body>
        </html>
        """)

@app.post("/api/match/new", response_model=Match)
async def create_new_match(match_data: MatchCreate):
    """新規対戦データ作成"""
    try:
        logger.info(f"新規対戦作成開始: {match_data.player_a} vs {match_data.player_b}, 先行: {match_data.first_player}")
        
        # 先行プレイヤーが有効かチェック
        if match_data.first_player not in [match_data.player_a, match_data.player_b]:
            logger.warning(f"無効な先行プレイヤー指定: {match_data.first_player}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="先行プレイヤーは対戦者の中から選択してください"
            )
        
        match = Match(
            players=[match_data.player_a, match_data.player_b],
            first_player=match_data.first_player,
            total_scores={match_data.player_a: 0, match_data.player_b: 0}
        )
        created_match = data_store.create_match(match)
        logger.info(f"新規対戦作成完了: ID={created_match.id}")
        return created_match
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"対戦作成エラー: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"対戦作成エラー: {str(e)}"
        )

@app.post("/api/match/{match_id}/turn", response_model=ScoreResponse)
async def add_turn(match_id: str, turn_data: TurnInput):
    """対象対戦にターン情報を追加"""
    match = data_store.get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    # プレイヤーが有効かチェック
    if turn_data.player not in match.players:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効なプレイヤーです"
        )
    
    try:
        # 新しいターンを作成
        turn_number = len(match.turns) + 1
        new_turn = Turn(
            turn_number=turn_number,
            player=turn_data.player,
            defeated_followers=turn_data.defeated_followers,
            used_spells=turn_data.used_spells,
            used_amulets=turn_data.used_amulets,
            acted_amulets=turn_data.acted_amulets
        )
        
        # ターンを追加
        match.turns.append(new_turn)
        
        # スコアを更新
        match = update_match_score(match)
        data_store.update_match(match)
        
        # 現在ターンのスコアを計算
        current_turn_score = calculate_turn_score(new_turn)
        
        # 次のプレイヤーを決定
        next_player = get_next_player(match)
        
        return ScoreResponse(
            current_turn=turn_number + 1,
            current_player=next_player,
            turn_score=current_turn_score,
            total_scores=match.total_scores,
            final_scores=match.total_scores if match.winner else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ターン追加エラー: {str(e)}"
        )

@app.delete("/api/match/{match_id}/turn/last", response_model=ScoreResponse)
async def remove_last_turn(match_id: str):
    """最後のターンを削除（1ターン戻る）"""
    match = data_store.get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    if not match.turns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="削除するターンがありません"
        )
    
    try:
        # 最後のターンを削除
        removed_turn = match.turns.pop()
        
        # スコアを更新
        match = update_match_score(match)
        data_store.update_match(match)
        
        current_turn = len(match.turns) + 1
        turn_score = 0 if len(match.turns) == 0 else calculate_turn_score(match.turns[-1])
        
        # 次のプレイヤーを決定
        next_player = get_next_player(match)
        
        return ScoreResponse(
            current_turn=current_turn,
            current_player=next_player,
            turn_score=turn_score,
            total_scores=match.total_scores,
            final_scores=match.total_scores if match.winner else None
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ターン削除エラー: {str(e)}"
        )

@app.get("/api/match/{match_id}/score", response_model=ScoreResponse)
async def get_current_score(match_id: str):
    """現在のスコアを取得"""
    match = data_store.get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    current_turn = len(match.turns) + 1
    turn_score = 0 if len(match.turns) == 0 else calculate_turn_score(match.turns[-1])
    next_player = get_next_player(match)
    
    return ScoreResponse(
        current_turn=current_turn,
        current_player=next_player,
        turn_score=turn_score,
        total_scores=match.total_scores,
        final_scores=match.total_scores if match.winner else None
    )

@app.post("/api/match/{match_id}/finish", response_model=Match)
async def finish_match(match_id: str, finish_data: MatchFinish):
    """勝敗フラグを受け取り、2倍計算して保存"""
    logger.info(f"対戦終了処理開始: Match={match_id}, Winner={finish_data.winner}")
    
    match = data_store.get_match(match_id)
    if not match:
        logger.warning(f"対戦が見つかりません: {match_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    # 勝者が有効かチェック
    if finish_data.winner not in match.players:
        logger.warning(f"無効な勝者: {finish_data.winner}, Match={match_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効な勝者です"
        )
    
    try:
        # 対戦前のスコア記録
        original_scores = match.total_scores.copy()
        
        # 勝者を設定
        match.winner = finish_data.winner
        
        # 最終スコアを計算
        match = update_match_score(match)
        updated_match = data_store.update_match(match)
        
        logger.info(f"対戦終了完了: Match={match_id}, Winner={finish_data.winner}")
        logger.info(f"スコア変化: {original_scores} → {updated_match.total_scores}")
        
        return updated_match
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"対戦終了エラー: Match={match_id}, Error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"対戦終了エラー: {str(e)}"
        )

@app.get("/api/match/list", response_model=List[Match])
async def get_match_list():
    """対戦履歴を取得"""
    try:
        matches = data_store.get_all_matches()
        # 日時の降順でソート
        matches.sort(key=lambda x: x.date, reverse=True)
        return matches
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"履歴取得エラー: {str(e)}"
        )

@app.get("/api/match/{match_id}/history", response_model=List[Turn])
async def get_match_history(match_id: str):
    """対戦中の入力履歴を取得"""
    match = data_store.get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    return match.turns

@app.post("/api/match/{match_id}/button", response_model=ScoreResponse)
async def add_button_input(match_id: str, button_data: ButtonInput):
    """ボタン入力でポイントを追加"""
    logger.info(f"ボタン入力: Match={match_id}, Player={button_data.player}, Type={button_data.card_type}, Ether={button_data.ether_value}")
    
    match = data_store.get_match(match_id)
    if not match:
        logger.warning(f"対戦が見つかりません: {match_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    # プレイヤーが有効かチェック
    if button_data.player not in match.players:
        logger.warning(f"無効なプレイヤー: {button_data.player}, Match={match_id}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効なプレイヤーです"
        )
    
    try:
        # 現在のターンデータを取得または作成
        if not match.turns or match.turns[-1].player != button_data.player:
            # 新しいターンを作成
            turn_number = len(match.turns) + 1
            new_turn = Turn(
                turn_number=turn_number,
                player=button_data.player
            )
            match.turns.append(new_turn)
            logger.info(f"新しいターン作成: Turn={turn_number}, Player={button_data.player}")
        
        # 最後のターンを取得
        current_turn = match.turns[-1]
        
        # ボタンの種類に応じてエーテル値を追加
        if button_data.card_type == "follower":
            current_turn.defeated_followers.append(button_data.ether_value)
        elif button_data.card_type == "spell":
            current_turn.used_spells.append(button_data.ether_value)
        elif button_data.card_type == "amulet":
            current_turn.used_amulets.append(button_data.ether_value)
        elif button_data.card_type == "act":
            current_turn.acted_amulets.append(button_data.ether_value)
        else:
            logger.error(f"無効なカード種類: {button_data.card_type}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="無効なカード種類です"
            )
        
        # スコアを更新
        match = update_match_score(match)
        data_store.update_match(match)
        
        # 現在ターンのスコアを計算
        current_turn_score = calculate_turn_score(current_turn)
        
        # 次のプレイヤーを決定
        next_player = get_next_player(match)
        
        logger.info(f"ボタン入力完了: Match={match_id}, TurnScore={current_turn_score}, TotalScores={match.total_scores}")
        
        return ScoreResponse(
            current_turn=len(match.turns),
            current_player=current_turn.player,
            turn_score=current_turn_score,
            total_scores=match.total_scores,
            final_scores=match.total_scores if match.winner else None
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"ボタン入力エラー: Match={match_id}, Error={str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"ボタン入力エラー: {str(e)}"
        )

@app.delete("/api/match/{match_id}")
async def delete_match(match_id: str):
    """対戦削除"""
    success = data_store.delete_match(match_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    
    return {"message": "対戦が削除されました"}

@app.get("/api/match/{match_id}", response_model=Match)
async def get_match(match_id: str):
    """対戦詳細を取得"""
    match = data_store.get_match(match_id)
    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="対戦が見つかりません"
        )
    return match

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
