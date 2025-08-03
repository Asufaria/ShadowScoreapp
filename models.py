from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field
import uuid

class Turn(BaseModel):
    """ターンデータモデル"""
    turn_number: int = Field(..., description="ターン番号")
    player: str = Field(..., description="ターンのプレイヤー")
    defeated_followers: List[int] = Field(default=[], description="倒したフォロワーの生成エーテル")
    used_spells: List[int] = Field(default=[], description="相手が使用したスペルの生成エーテル")
    used_amulets: List[int] = Field(default=[], description="相手が使用したアミュレットの生成エーテル")
    acted_amulets: List[int] = Field(default=[], description="相手がアクトしたアミュレットの生成エーテル（1/3計算対象）")

class Match(BaseModel):
    """対戦データモデル"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="対戦ID")
    date: datetime = Field(default_factory=datetime.now, description="対戦日時")
    players: List[str] = Field(..., description="プレイヤー名リスト [playerA, playerB]")
    first_player: str = Field(..., description="先行プレイヤー名")
    turns: List[Turn] = Field(default=[], description="ターンリスト")
    winner: Optional[str] = Field(default=None, description="勝者の名前")
    total_scores: Dict[str, int] = Field(default_factory=dict, description="各プレイヤーの総スコア")

class TurnInput(BaseModel):
    """ターン入力用モデル"""
    player: str = Field(..., description="ターンのプレイヤー")
    defeated_followers: List[int] = Field(default=[], description="倒したフォロワーの生成エーテル")
    used_spells: List[int] = Field(default=[], description="相手が使用したスペルの生成エーテル")
    used_amulets: List[int] = Field(default=[], description="相手が使用したアミュレットの生成エーテル")
    acted_amulets: List[int] = Field(default=[], description="相手がアクトしたアミュレットの生成エーテル")

class MatchCreate(BaseModel):
    """対戦作成用モデル"""
    player_a: str = Field(..., description="プレイヤーA名")
    player_b: str = Field(..., description="プレイヤーB名")
    first_player: str = Field(..., description="先行プレイヤー名")

class MatchFinish(BaseModel):
    """対戦終了用モデル"""
    winner: str = Field(..., description="勝者の名前")

class ScoreResponse(BaseModel):
    """スコア応答モデル"""
    current_turn: int = Field(..., description="現在のターン")
    current_player: str = Field(..., description="現在のプレイヤー")
    turn_score: int = Field(..., description="現在ターンのスコア")
    total_scores: Dict[str, int] = Field(..., description="各プレイヤーの総スコア")
    final_scores: Optional[Dict[str, int]] = Field(default=None, description="最終スコア（勝敗確定時）")

class ButtonInput(BaseModel):
    """ボタン入力用モデル"""
    player: str = Field(..., description="プレイヤー名")
    rarity: str = Field(..., description="レアリティ（bronze/silver/gold/legend）")
    card_type: str = Field(..., description="カード種類（follower/spell/amulet/act）")
    ether_value: int = Field(..., description="生成エーテル値")
