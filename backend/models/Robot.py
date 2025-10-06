from typing import Optional
from exceptions import InvalidDirectionException


class Robot:
    VALID_DIRECTIONS = ['NORTH', 'SOUTH', 'EAST', 'WEST']
    
    def __init__(self):
        self.x: Optional[int] = None
        self.y: Optional[int] = None
        self.facing: Optional[str] = None
    
    def is_placed(self) -> bool:
        """Verifica si el robot ha sido colocado en el tablero"""
        return self.x is not None and self.y is not None and self.facing is not None
    
    def place(self, x: int, y: int, facing: str) -> None:
        """
        Coloca el robot en una posición
        
        Raises:
            InvalidDirectionException: Si la dirección no es válida
        """
        if facing not in self.VALID_DIRECTIONS:
            raise InvalidDirectionException(
                f"Dirección '{facing}' no válida. Debe ser: {', '.join(self.VALID_DIRECTIONS)}"
            )
        
        self.x = x
        self.y = y
        self.facing = facing
    
    def turn_left(self) -> None:
        """Gira el robot 90 grados a la izquierda"""
        rotations = {
            'NORTH': 'WEST',
            'WEST': 'SOUTH',
            'SOUTH': 'EAST',
            'EAST': 'NORTH'
        }
        self.facing = rotations[self.facing]
    
    def turn_right(self) -> None:
        """Gira el robot 90 grados a la derecha"""
        rotations = {
            'NORTH': 'EAST',
            'EAST': 'SOUTH',
            'SOUTH': 'WEST',
            'WEST': 'NORTH'
        }
        self.facing = rotations[self.facing]
    
    def get_position(self) -> tuple[int, int, str]:
        """Retorna la posición y orientación actual"""
        return (self.x, self.y, self.facing)
    
    def get_next_position(self) -> tuple[int, int]:
        """Calcula la siguiente posición sin moverse"""
        movements = {
            'NORTH': (0, 1),
            'SOUTH': (0, -1),
            'EAST': (1, 0),
            'WEST': (-1, 0)
        }
        dx, dy = movements[self.facing]
        return (self.x + dx, self.y + dy)