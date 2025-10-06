import json
import os
from typing import Optional
from models.Robot import Robot
from repositories.IRepository import IRepository


class RobotRepository(IRepository[Robot]):
    """Repositorio para persistir el robot del juego"""
    
    def __init__(self, db_path: str = "data/robot.json"):
        self.db_path = db_path
        self._ensure_db_exists()
    
    def _ensure_db_exists(self):
        """Asegura que el archivo de persistencia existe"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        if not os.path.exists(self.db_path):
            with open(self.db_path, 'w') as f:
                json.dump(None, f)
    
    def save(self, robot: Robot) -> None:
        """Persiste el robot"""
        data = {
            "x": robot.x,
            "y": robot.y,
            "facing": robot.facing
        }
        
        with open(self.db_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load(self) -> Optional[Robot]:
        """Carga el robot desde la persistencia"""
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        
        if data is None:
            return None
        
        robot = Robot()
        robot.x = data["x"]
        robot.y = data["y"]
        robot.facing = data["facing"]
        return robot
    
    def delete(self) -> None:
        """Elimina el robot persistido"""
        with open(self.db_path, 'w') as f:
            json.dump(None, f)
    
    def exists(self) -> bool:
        """Verifica si existe un robot persistido"""
        with open(self.db_path, 'r') as f:
            data = json.load(f)
        return data is not None