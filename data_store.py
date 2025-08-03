import json
import os
from pathlib import Path
from typing import List, Optional
from models import Match

class DataStore:
    """データストレージクラス（JSONファイルベース）"""
    
    def __init__(self, data_file: str = None):
        # ポータブル対応: 環境変数からデータディレクトリを取得
        if data_file is None:
            data_dir = os.environ.get('SHADOWSCORE_DATA_DIR', '.')
            self.data_file = os.path.join(data_dir, "matches.json")
        else:
            self.data_file = data_file
        
        self.matches: List[Match] = []
        self.load_data()
    
    def load_data(self):
        """データファイルから対戦データを読み込む"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.matches = [Match(**match) for match in data]
                print(f"データ読み込み完了: {len(self.matches)}件の対戦データ")
            except (json.JSONDecodeError, Exception) as e:
                print(f"データ読み込みエラー: {e}")
                self.matches = []
        else:
            print(f"新規データファイル作成: {self.data_file}")
            self.matches = []
    
    def save_data(self):
        """データファイルに対戦データを保存する"""
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
            
            data = [match.model_dump() for match in self.matches]
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"データ保存エラー: {e}")
    
    def create_match(self, match: Match) -> Match:
        """新しい対戦を作成する"""
        self.matches.append(match)
        self.save_data()
        return match
    
    def get_match(self, match_id: str) -> Optional[Match]:
        """対戦IDで対戦データを取得する"""
        for match in self.matches:
            if match.id == match_id:
                return match
        return None
    
    def update_match(self, match: Match) -> Match:
        """対戦データを更新する"""
        for i, existing_match in enumerate(self.matches):
            if existing_match.id == match.id:
                self.matches[i] = match
                self.save_data()
                return match
        raise ValueError(f"対戦ID {match.id} が見つかりません")
    
    def delete_match(self, match_id: str) -> bool:
        """対戦を削除する"""
        for i, match in enumerate(self.matches):
            if match.id == match_id:
                del self.matches[i]
                self.save_data()
                return True
        return False
    
    def get_all_matches(self) -> List[Match]:
        """全ての対戦データを取得する"""
        return self.matches.copy()

# グローバルデータストアインスタンス
data_store = DataStore()
