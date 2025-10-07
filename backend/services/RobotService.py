from typing import Optional
from models.Robot import Robot
from repositories.RobotRepository import RobotRepository
from services.BoardService import BoardService
from exceptions import (
    RobotNotPlacedException,
    WallCollisionException,
    RobotOutOfBoundsException
)


class RobotService:
    """Servicio para gestionar el robot del juego"""
    
    def __init__(self, robot_repository: RobotRepository, board_service: BoardService):
        self._repository = robot_repository
        self._board_service = board_service
    
    def place(self, x: int, y: int, facing: str) -> None:
        """
        Coloca el robot en una posición (o lo reposiciona si ya existe)
        
        Raises:
            ValueError: Si no existe un tablero creado
            InvalidDirectionException: Si la dirección no es válida
            WallCollisionException: Si hay una pared en esa posición
        """
        board = self._board_service.get_board()
        if board is None:
            raise ValueError("No existe un tablero creado")
        
        if board.has_wall_at(x, y):
            raise WallCollisionException(
                f"No se puede colocar el robot en ({x}, {y}): hay una pared"
            )
        
        if not board.is_inside(x, y):
            raise RobotOutOfBoundsException(
                f"El robot no puede estar fuera de los limites del tablero"
            )

        # Obtener o crear robot
        robot = self._repository.load()
        if robot is None:
            robot = Robot()
        
        # El dominio valida la dirección
        robot.place(x, y, facing)
        
        # Persistir
        self._repository.save(robot)
    
    def move(self) -> None:
        """
        Mueve el robot hacia adelante según su orientación
        Con wrap around en los bordes del tablero
        
        Raises:
            ValueError: Si no existe un tablero creado
            RobotNotPlacedException: Si el robot no ha sido colocado
            WallCollisionException: Si hay una pared en la siguiente posición
        """
        board = self._board_service.get_board()
        
        if board is None:
            raise ValueError("No existe un tablero creado")
        
        robot = self._repository.load()
        if robot is None or not robot.is_placed():
            raise RobotNotPlacedException("El robot no ha sido colocado en el tablero")
        
        # Calcular siguiente posición
        next_x, next_y = robot.get_next_position()

        # print("="*20)
        # print(next_x, next_y)


        # Aplicar wrap around (teleport a través de los bordes)
        next_x = self._wrap_coordinate(next_x, board.width)
        next_y = self._wrap_coordinate(next_y, board.height)
        
        print(board.has_wall_at(next_x, next_y))

        # Validar que no hay pared
        if board.has_wall_at(next_x, next_y):
            raise WallCollisionException(
                f"No se puede mover: hay una pared en ({next_x}, {next_y})"
            )
        
        # Mover el robot
        robot.x = next_x
        robot.y = next_y
        
        # Persistir
        self._repository.save(robot)
    
    def left(self) -> None:
        """
        Gira el robot 90 grados a la izquierda

        RobotNotPlacedException: Si el robot no ha sido colocado
        """
        robot = self._repository.load()
        if robot is None or not robot.is_placed():
            raise RobotNotPlacedException("El robot no ha sido colocado en el tablero")
        
        robot.turn_left()
        self._repository.save(robot)
    
    def right(self) -> None:
        """
        Gira el robot 90 grados a la derecha
        
        RobotNotPlacedException: Si el robot no ha sido colocado
        """
        robot = self._repository.load()
        if robot is None or not robot.is_placed():
            raise RobotNotPlacedException("El robot no ha sido colocado en el tablero")
        
        robot.turn_right()
        self._repository.save(robot)
    
    def report(self) -> Optional[tuple[int, int, str]]:
        """
        Obtiene la posición y orientación actual del robot
        
        Returns:
            (x, y, facing) o None si no está colocado
        """
        robot = self._repository.load()
        if robot is None or not robot.is_placed():
            return None
        
        return robot.get_position()
    
    def robot_exists(self) -> bool:
        """Verifica si existe un robot persistido"""
        return self._repository.exists()
    
    def delete_robot(self) -> None:
        """Elimina el robot persistido"""
        self._repository.delete()
    
    def _wrap_coordinate(self, coordinate: int, max_value: int) -> int:
        """
        Aplica wrap around a una coordenada
        Si sale por un borde, aparece por el opuesto
        
        Ejemplo: si coordinate = 0 y max_value = 5 → retorna 5
                 si coordinate = 6 y max_value = 5 → retorna 1
        """
        if coordinate < 1:
            return max_value
        elif coordinate > max_value:
            return 1
        return coordinate