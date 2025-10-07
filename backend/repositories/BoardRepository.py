import json
import os
from typing import Optional, Dict
from models.Board import Board
from models.Wall import Wall
from repositories.IRepository import IRepository


class BoardRepository(IRepository):
    """Repositorio para persistir el tablero del juego"""
    
    def __init__(self, db_path: str = "data/board.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Asegura que el archivo de persistencia existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump(None, f)
    
    def save(self, board: Board) -> None:
        data = {
            "width": board.width,
            "height": board.height,
            "walls": [{"x": wall.x, "y": wall.y} for wall in board.walls]  # ✅
        }
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> Optional[Board]:
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        
        if data is None:
            return None
        
        board = Board(data["width"], data["height"])
        
        for wall_data in data.get("walls", []):
            wall = Wall(wall_data["x"], wall_data["y"])
            board.walls.append(wall)
        
        return board
    
    def delete(self) -> None:
        """Elimina el tablero persistido"""
        with open(self.db_path, 'w') as f:
            json.dump(None, f)
    
    def exists(self) -> bool:
        """Verifica si existe un tablero persistido"""
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        return data is not None