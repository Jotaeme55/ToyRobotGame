import pytest
from unittest.mock import Mock, MagicMock, patch
from services.BoardService import BoardService
from repositories.BoardRepository import BoardRepository
from models.Board import Board
from models.Wall import Wall
from exceptions import WallOutOfBoundsException, WallAlreadyExistsException


class TestBoardService:
    """Tests unitarios para BoardService"""
    
    @pytest.fixture
    def mock_repository(self):
        """Mock del repositorio"""
        return Mock(spec=BoardRepository)
    
    @pytest.fixture
    def service(self, mock_repository):
        """Instancia del servicio con repositorio mockeado"""
        return BoardService(mock_repository)
    
    @pytest.fixture
    def sample_board(self):
        """Tablero de ejemplo para tests"""
        return Board(width=10, height=10)
    
    @pytest.fixture
    def sample_wall(self):
        """Pared de ejemplo para tests"""
        return Wall(x=0, y=0)


    # ==================== Tests de create_or_get_board ====================
    
    def test_create_or_get_board_creates_new_when_none_exists(
        self, service, mock_repository
    ):
        """Debe crear un nuevo tablero cuando no existe ninguno"""

        mock_repository.load.return_value = None
        

        result = service.create_or_get_board(width=10, height=8)
        
        assert result is not None
        assert result.width == 10
        assert result.height == 8
        mock_repository.load.assert_called_once()
        mock_repository.save.assert_called_once_with(result)

    
    def test_create_or_get_board_returns_existing_board(
        self, service, mock_repository, sample_board
    ):
        """Debe devolver el tablero existente en memoria sin crear uno nuevo"""
        mock_repository.load.return_value = sample_board
        service._board = sample_board
        
        result = service.create_or_get_board(width=10, height=10)
        
        assert result == sample_board
        mock_repository.load.assert_not_called()
        mock_repository.save.assert_not_called()

    
    def test_create_or_get_board_loads_from_repository(
        self, service, mock_repository, sample_board
    ):
        """Debe cargar el tablero del repositorio si existe"""
     
        mock_repository.load.return_value = sample_board
        
        result = service.create_or_get_board(width=10, height=10)
        
        assert result == sample_board
        mock_repository.load.assert_called_once()
        mock_repository.save.assert_not_called()


    # # ==================== Tests de get_board ====================
    
    def test_get_board_returns_loaded_board(
        self, service, mock_repository, sample_board
    ):
        """Debe cargar y devolver el tablero del repositorio"""
     
        mock_repository.load.return_value = sample_board
        
        result = service.get_board()
        
        assert result == sample_board
        mock_repository.load.assert_called_once()
    
    def test_get_board_returns_none_when_no_board(
        self, service, mock_repository
    ):
        """Debe devolver None cuando no hay tablero"""
        mock_repository.load.return_value = None
        
        result = service.get_board()
        
        assert result is None
        mock_repository.load.assert_called_once()


    # # ==================== Tests de add_wall ====================
    
    def test_add_wall_success(
        self, service, mock_repository, sample_board, sample_wall
    ):
        """Debe añadir una pared exitosamente"""
        mock_repository.load.return_value = sample_board
        sample_board.add_wall = Mock()
        
        service.add_wall(sample_wall)
        
        sample_board.add_wall.assert_called_once_with(sample_wall)
        mock_repository.save.assert_called_once_with(sample_board)

    
    def test_add_wall_raises_when_no_board(
        self, service, mock_repository, sample_wall
    ):
        """Debe lanzar ValueError cuando no hay tablero inicializado"""
        mock_repository.load.return_value = None
        with pytest.raises(ValueError, match="No hay tablero inicializado"):
            service.add_wall(sample_wall)
        
        mock_repository.save.assert_not_called()
    
    def test_add_wall_propagates_wall_out_of_bounds_exception(
        self, service, mock_repository, sample_board, sample_wall
    ):
        """Debe propagar WallOutOfBoundsException del board"""
        mock_repository.load.return_value = sample_board
        sample_board.add_wall = Mock(
            side_effect=WallOutOfBoundsException("Pared fuera de límites")
        )
        with pytest.raises(WallOutOfBoundsException):
            service.add_wall(sample_wall)
        
        mock_repository.save.assert_not_called()
    
    def test_add_wall_propagates_wall_already_exists_exception(
        self, service, mock_repository, sample_board, sample_wall
    ):
        """Debe propagar WallAlreadyExistsException del board"""
        mock_repository.load.return_value = sample_board
        sample_board.add_wall = Mock(
            side_effect=WallAlreadyExistsException("Pared ya existe")
        )
        with pytest.raises(WallAlreadyExistsException):
            service.add_wall(sample_wall)
        
        mock_repository.save.assert_not_called()

    # # ==================== Tests de delete_board ====================
    
    def test_delete_board_success(self, service, mock_repository):
        """Debe eliminar el tablero exitosamente"""
        service._board = Mock()
        
        result = service.delete_board()
        
        assert result is True
        assert service._board is None
        mock_repository.delete.assert_called_once()
    
    def test_delete_board_when_no_board_in_memory(
        self, service, mock_repository
    ):
        """Debe funcionar incluso si no hay tablero en memoria"""
        service._board = None
        
        result = service.delete_board()
        
        assert result is True
        assert service._board is None
        mock_repository.delete.assert_called_once()