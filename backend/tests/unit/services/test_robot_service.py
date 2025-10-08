import pytest
from unittest.mock import Mock, MagicMock
from services.RobotService import RobotService
from repositories.RobotRepository import RobotRepository
from services.BoardService import BoardService
from models.Robot import Robot
from models.Board import Board
from exceptions import (
    RobotNotPlacedException,
    WallCollisionException,
    RobotOutOfBoundsException,
    InvalidDirectionException
)


class TestRobotService:
    """Tests unitarios para RobotService"""
    
    @pytest.fixture
    def mock_robot_repository(self):
        """Mock del repositorio de robot"""
        return Mock(spec=RobotRepository)
    
    @pytest.fixture
    def mock_board_service(self):
        """Mock del servicio de tablero"""
        return Mock(spec=BoardService)
    
    @pytest.fixture
    def service(self, mock_robot_repository, mock_board_service):
        """Instancia del servicio con dependencias mockeadas"""
        return RobotService(mock_robot_repository, mock_board_service)
    
    @pytest.fixture
    def sample_robot(self):
        """Robot de ejemplo colocado"""
        robot = Robot()
        robot.place(5, 5, 'NORTH')
        return robot
    
    @pytest.fixture
    def sample_board(self):
        """Mock de tablero de ejemplo"""
        board = Mock(spec=Board)
        board.width = 10
        board.height = 10
        board.has_wall_at.return_value = False
        board.is_inside.return_value = True
        return board


    # ==================== Tests de place ====================
    
    def test_place_robot_successfully_when_no_robot_exists(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe colocar un robot nuevo exitosamente"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = None
        
        # Act
        service.place(5, 5, 'NORTH')
        
        # Assert
        sample_board.has_wall_at.assert_called_once_with(5, 5)
        sample_board.is_inside.assert_called_once_with(5, 5)
        mock_robot_repository.save.assert_called_once()
        
        # Verificar que se guardó un robot correctamente colocado
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 5
        assert saved_robot.y == 5
        assert saved_robot.facing == 'NORTH'
    
    def test_place_reposition_existing_robot(
        self, service, mock_robot_repository, mock_board_service, sample_board, sample_robot
    ):
        """Debe reposicionar un robot existente"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = sample_robot
        
        # Act
        service.place(8, 3, 'EAST')
        
        # Assert
        sample_board.has_wall_at.assert_called_once_with(8, 3)
        sample_board.is_inside.assert_called_once_with(8, 3)
        mock_robot_repository.save.assert_called_once()
        
        # Verificar nueva posición
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 8
        assert saved_robot.y == 3
        assert saved_robot.facing == 'EAST'
    
    def test_place_raises_when_no_board(
        self, service, mock_robot_repository, mock_board_service
    ):
        """Debe lanzar ValueError cuando no existe tablero"""
        # Arrange
        mock_board_service.get_board.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="No existe un tablero creado"):
            service.place(5, 5, 'NORTH')
        
        mock_robot_repository.save.assert_not_called()
    
    def test_place_raises_when_wall_collision(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe lanzar WallCollisionException si hay pared en la posición"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        sample_board.has_wall_at.return_value = True
        
        # Act & Assert
        with pytest.raises(WallCollisionException, match="hay una pared"):
            service.place(5, 5, 'NORTH')
        
        mock_robot_repository.save.assert_not_called()
    
    def test_place_raises_when_out_of_bounds(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe lanzar RobotOutOfBoundsException si está fuera de límites"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        sample_board.is_inside.return_value = False
        
        # Act & Assert
        with pytest.raises(RobotOutOfBoundsException, match="fuera de los limites"):
            service.place(15, 15, 'NORTH')
        
        mock_robot_repository.save.assert_not_called()
    
    def test_place_raises_when_invalid_direction(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe propagar InvalidDirectionException si la dirección no es válida"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = None
        
        # Act & Assert
        with pytest.raises(InvalidDirectionException):
            service.place(5, 5, 'INVALID')
        
        mock_robot_repository.save.assert_not_called()


    # ==================== Tests de move ====================
    
    def test_move_robot_successfully(
        self, service, mock_robot_repository, mock_board_service, sample_board, sample_robot
    ):
        """Debe mover el robot exitosamente"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = sample_robot
        
        # Act
        service.move()
        
        sample_board.has_wall_at.assert_called_with(6, 5) 
        mock_robot_repository.save.assert_called_once()
        
        # Verificar nueva posición
        assert sample_robot.x == 6
        assert sample_robot.y == 5
    
    def test_move_raises_when_no_board(
        self, service, mock_robot_repository, mock_board_service
    ):
        """Debe lanzar ValueError cuando no existe tablero"""
        # Arrange
        mock_board_service.get_board.return_value = None
        
        # Act & Assert
        with pytest.raises(ValueError, match="No existe un tablero creado"):
            service.move()
        
        mock_robot_repository.save.assert_not_called()
    
    def test_move_raises_when_robot_not_placed(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe lanzar RobotNotPlacedException si robot no está colocado"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = None
        
        # Act & Assert
        with pytest.raises(RobotNotPlacedException, match="no ha sido colocado"):
            service.move()
        
        mock_robot_repository.save.assert_not_called()
    
    def test_move_raises_when_wall_in_next_position(
        self, service, mock_robot_repository, mock_board_service, sample_board, sample_robot
    ):
        """Debe lanzar WallCollisionException si hay pared adelante"""
        # Arrange
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = sample_robot
        sample_board.has_wall_at.return_value = True
        
        # Act & Assert
        with pytest.raises(WallCollisionException, match="hay una pared"):
            service.move()
        
        # Solo debe guardar si el movimiento fue exitoso
        mock_robot_repository.save.assert_not_called()
    
    def test_move_wrap_around_north_edge(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe hacer wrap around cuando sale por el borde norte"""
        # Arrange
        robot = Robot()
        robot.place(10, 5, 'NORTH')  # En el borde norte
        
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = robot
        sample_board.width = 10
        sample_board.height = 10
        
        # Act
        service.move()
        
        # Assert
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 1  # Wrap around: 11 -> 1
        assert saved_robot.y == 5
    
    def test_move_wrap_around_south_edge(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe hacer wrap around cuando sale por el borde sur"""
        # Arrange
        robot = Robot()
        robot.place(1, 5, 'SOUTH')  # En el borde sur
        
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = robot
        sample_board.width = 10
        sample_board.height = 10
        
        # Act
        service.move()
        
        # Assert
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 10  # Wrap around: 0 -> 10
        assert saved_robot.y == 5
    
    def test_move_wrap_around_east_edge(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe hacer wrap around cuando sale por el borde este"""
        # Arrange
        robot = Robot()
        robot.place(5, 10, 'EAST')  # En el borde este
        
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = robot
        sample_board.width = 10
        sample_board.height = 10
        
        # Act
        service.move()
        
        # Assert
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 5
        assert saved_robot.y == 1  # Wrap around: 11 -> 1
    
    def test_move_wrap_around_west_edge(
        self, service, mock_robot_repository, mock_board_service, sample_board
    ):
        """Debe hacer wrap around cuando sale por el borde oeste"""
        # Arrange
        robot = Robot()
        robot.place(5, 1, 'WEST')  # En el borde oeste
        
        mock_board_service.get_board.return_value = sample_board
        mock_robot_repository.load.return_value = robot
        sample_board.width = 10
        sample_board.height = 10
        
        # Act
        service.move()
        
        # Assert
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.x == 5
        assert saved_robot.y == 10  # Wrap around: 0 -> 10


    # ==================== Tests de left ====================
    
    def test_left_turns_robot_successfully(
        self, service, mock_robot_repository, sample_robot
    ):
        """Debe girar el robot a la izquierda exitosamente"""
        # Arrange
        mock_robot_repository.load.return_value = sample_robot
        
        # Act
        service.left()
        
        # Assert
        mock_robot_repository.save.assert_called_once()
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.facing == 'WEST'  # NORTH -> WEST
    
    def test_left_raises_when_robot_not_placed(
        self, service, mock_robot_repository
    ):
        """Debe lanzar RobotNotPlacedException si robot no está colocado"""
        # Arrange
        mock_robot_repository.load.return_value = None
        
        # Act & Assert
        with pytest.raises(RobotNotPlacedException, match="no ha sido colocado"):
            service.left()
        
        mock_robot_repository.save.assert_not_called()


    # ==================== Tests de right ====================
    
    def test_right_turns_robot_successfully(
        self, service, mock_robot_repository, sample_robot
    ):
        """Debe girar el robot a la derecha exitosamente"""
        # Arrange
        mock_robot_repository.load.return_value = sample_robot
        
        # Act
        service.right()
        
        # Assert
        mock_robot_repository.save.assert_called_once()
        saved_robot = mock_robot_repository.save.call_args[0][0]
        assert saved_robot.facing == 'EAST'  # NORTH -> EAST
    
    def test_right_raises_when_robot_not_placed(
        self, service, mock_robot_repository
    ):
        """Debe lanzar RobotNotPlacedException si robot no está colocado"""
        # Arrange
        mock_robot_repository.load.return_value = None
        
        # Act & Assert
        with pytest.raises(RobotNotPlacedException, match="no ha sido colocado"):
            service.right()
        
        mock_robot_repository.save.assert_not_called()


    # ==================== Tests de report ====================
    
    def test_report_returns_position_when_robot_placed(
        self, service, mock_robot_repository, sample_robot
    ):
        """Debe retornar la posición cuando el robot está colocado"""
        # Arrange
        mock_robot_repository.load.return_value = sample_robot
        
        # Act
        result = service.report()
        
        # Assert
        assert result == (5, 5, 'NORTH')
    
    def test_report_returns_none_when_robot_not_placed(
        self, service, mock_robot_repository
    ):
        """Debe retornar None cuando el robot no está colocado"""
        # Arrange
        mock_robot_repository.load.return_value = None
        
        # Act
        result = service.report()
        
        # Assert
        assert result is None
    
    def test_report_returns_none_when_robot_exists_but_not_placed(
        self, service, mock_robot_repository
    ):
        """Debe retornar None cuando existe robot pero no está colocado"""
        # Arrange
        unplaced_robot = Robot()  # Robot sin place()
        mock_robot_repository.load.return_value = unplaced_robot
        
        # Act
        result = service.report()
        
        # Assert
        assert result is None


    # ==================== Tests de robot_exists ====================
    
    def test_robot_exists_returns_true_when_exists(
        self, service, mock_robot_repository
    ):
        """Debe retornar True cuando el robot existe"""
        # Arrange
        mock_robot_repository.exists.return_value = True
        
        # Act
        result = service.robot_exists()
        
        # Assert
        assert result is True
        mock_robot_repository.exists.assert_called_once()
    
    def test_robot_exists_returns_false_when_not_exists(
        self, service, mock_robot_repository
    ):
        """Debe retornar False cuando el robot no existe"""
        # Arrange
        mock_robot_repository.exists.return_value = False
        
        # Act
        result = service.robot_exists()
        
        # Assert
        assert result is False
        mock_robot_repository.exists.assert_called_once()


    # ==================== Tests de delete_robot ====================
    
    def test_delete_robot_calls_repository(
        self, service, mock_robot_repository
    ):
        """Debe llamar al método delete del repositorio"""
        # Act
        service.delete_robot()
        
        # Assert
        mock_robot_repository.delete.assert_called_once()


    # ==================== Tests del método privado _wrap_coordinate ====================
    
    def test_wrap_coordinate_returns_same_when_in_bounds(self, service):
        """Debe retornar la misma coordenada si está dentro de límites"""
        assert service._wrap_coordinate(5, 10) == 5
        assert service._wrap_coordinate(1, 10) == 1
        assert service._wrap_coordinate(10, 10) == 10
    
    def test_wrap_coordinate_wraps_when_below_minimum(self, service):
        """Debe hacer wrap cuando está por debajo del mínimo"""
        assert service._wrap_coordinate(0, 10) == 10
        assert service._wrap_coordinate(-1, 10) == 10
    
    def test_wrap_coordinate_wraps_when_above_maximum(self, service):
        """Debe hacer wrap cuando está por encima del máximo"""
        assert service._wrap_coordinate(11, 10) == 1
        assert service._wrap_coordinate(15, 10) == 1