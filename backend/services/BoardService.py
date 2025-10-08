from repositories.BoardRepository import BoardRepository
from models.Board import Board
from models.Wall import Wall
from typing import Optional, Dict
from exceptions import (
    WallOutOfBoundsException,
    WallAlreadyExistsException,
)

class BoardService:
    def __init__(self, repository: BoardRepository):
        self._repository = repository
        self._board = None
    
    def create_or_get_board(self, width: int, height: int) -> Board:
        """Crea un nuevo tablero o devuelve el existente"""
        if self._board is None:
            self._board = self._repository.load()
        
        if self._board is None:
            self._board = Board(width, height)
            self._repository.save(self._board)
        
        return self._board
    
    def get_board(self) -> Optional[Board]:
        """Obtiene el tablero actual"""
       
        self._board = self._repository.load()
        return self._board
    
    def add_wall(self, wall: Wall) -> None:
        """Añade una pared al tablero. Lanza excepciones si falla."""
        board = self.get_board()
        if board is None:
            raise ValueError("No hay tablero inicializado")
        
        # ⬅️ Ya NO hay try-except, las excepciones suben automáticamente
        board.add_wall(wall)  # Si falla aquí, la excepción sube hasta el error handler
        self._repository.save(board)

    
    def delete_board(self) -> bool:
        """Elimina el tablero"""
        self._board = None
        self._repository.delete()
        return True