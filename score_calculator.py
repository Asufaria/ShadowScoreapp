from typing import List, Dict
from models import Turn, Match

def calculate_turn_score(turn: Turn) -> int:
    """
    ターンのスコアを計算する
    
    Args:
        turn: ターンデータ
        
    Returns:
        ターンスコア
    """
    followers_score = sum(turn.defeated_followers)
    spells_score = sum(turn.used_spells)
    amulets_score = sum(turn.used_amulets)
    # アクトしたアミュレットは1/3計算（切り捨て）
    acts_score = sum(turn.acted_amulets) // 3
    
    return followers_score + spells_score + amulets_score + acts_score

def calculate_player_score(turns: List[Turn], player: str, is_winner: bool = False) -> int:
    """
    指定プレイヤーの総スコアを計算する
    
    Args:
        turns: ターンリスト
        player: プレイヤー名
        is_winner: 勝敗フラグ
        
    Returns:
        プレイヤーの総スコア
    """
    player_turns = [turn for turn in turns if turn.player == player]
    total = sum(calculate_turn_score(turn) for turn in player_turns)
    return total * 2 if is_winner else total

def calculate_total_scores(turns: List[Turn], players: List[str], winner: str = None) -> Dict[str, int]:
    """
    各プレイヤーの総スコアを計算する
    
    Args:
        turns: ターンリスト
        players: プレイヤーリスト
        winner: 勝者名（None の場合は通常計算）
        
    Returns:
        各プレイヤーの総スコア辞書
    """
    scores = {}
    for player in players:
        is_winner = winner == player if winner else False
        scores[player] = calculate_player_score(turns, player, is_winner)
    return scores

def update_match_score(match: Match) -> Match:
    """
    対戦の総スコアを更新する
    
    Args:
        match: 対戦データ
        
    Returns:
        更新された対戦データ
    """
    match.total_scores = calculate_total_scores(match.turns, match.players, match.winner)
    return match

def get_next_player(match: Match) -> str:
    """
    次のターンのプレイヤーを取得する
    
    Args:
        match: 対戦データ
        
    Returns:
        次のプレイヤー名
    """
    if not match.turns:
        return match.first_player
    
    # 最後のターンとは異なるプレイヤーを返す
    last_player = match.turns[-1].player
    return match.players[1] if last_player == match.players[0] else match.players[0]
