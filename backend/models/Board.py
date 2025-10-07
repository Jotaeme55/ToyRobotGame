from models.Wall import Wall
from exceptions import WallOutOfBoundsException, WallAlreadyExistsException


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls: list[Wall] = [] 

    def is_valid_position(self, x, y) -> bool:
        """Comprueba si la posicion esta dentro del tablero y si no tiene una pared"""
        if not self.is_inside(x, y):
            return False
        
        for wall in self.walls:
            if (wall.x, wall.y) == (x, y):
                return False
            
        return True
    
    def is_inside(self, x, y) -> bool:
        """Comprueba si la posicion esta dentro de los límites del tablero"""
        return 1 <= x <= self.width and 1 <= y <= self.height
    
    def has_wall_at(self, x, y) -> bool:
        """Verifica si hay una pared en la posición especificada"""

        return any(wall.x == x and wall.y == y for wall in self.walls)
    
    def add_wall(self, wall: Wall) -> None:
        """
        Añade una pared al tablero
        
        Raises:
            WallOutOfBoundsException: Si la pared está fuera del tablero
            WallAlreadyExistsException: Si ya existe una pared en esa posición
        """
        if not self.is_inside(wall.get_x(), wall.get_y()):
            raise WallOutOfBoundsException(
                f"Pared en posición ({wall.x}, {wall.y}) está fuera del tablero (1-{self.width}, 1-{self.height})"
            )
        
        if self.has_wall_at(wall.x, wall.y):
            raise WallAlreadyExistsException(
                f"Ya existe una pared en la posición ({wall.x}, {wall.y})"
            )
        
        self.walls.append(wall)