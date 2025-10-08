import pytest
from models.Board import Board
from models.Wall import Wall
from exceptions import WallOutOfBoundsException, WallAlreadyExistsException


class TestBoard:
    """Tests unitarios para el modelo Board"""
    
    @pytest.fixture
    def board(self):
        """Tablero básico 10x10"""
        return Board(width=10, height=10)
    
    @pytest.fixture
    def small_board(self):
        """Tablero pequeño 3x3 para tests específicos"""
        return Board(width=3, height=3)
    
    @pytest.fixture
    def sample_wall(self):
        """Pared de ejemplo"""
        return Wall(x=5, y=5)
    
    @pytest.fixture
    def board_with_walls(self):
        """Tablero con algunas paredes pre-colocadas"""
        board = Board(width=10, height=10)
        board.walls.append(Wall(x=3, y=3))
        board.walls.append(Wall(x=7, y=7))
        return board


    # ==================== Tests de __init__ ====================
    
    def test_board_initializes_with_correct_dimensions(self, board):
        """Debe inicializar con las dimensiones correctas"""
        assert board.width == 10
        assert board.height == 10
    
    def test_board_initializes_with_empty_walls_list(self, board):
        """Debe inicializar con lista de paredes vacía"""
        assert board.walls == []
        assert isinstance(board.walls, list)
    
    def test_board_can_initialize_with_different_dimensions(self):
        """Debe poder crear tableros de diferentes tamaños"""
        board = Board(width=5, height=8)
        
        assert board.width == 5
        assert board.height == 8


    # ==================== Tests de is_inside ====================
    
    def test_is_inside_returns_true_for_valid_position(self, board):
        """Debe retornar True para posición válida dentro del tablero"""
        assert board.is_inside(5, 5) is True
        assert board.is_inside(1, 1) is True
        assert board.is_inside(10, 10) is True
    
    def test_is_inside_returns_true_for_all_corners(self, small_board):
        """Debe retornar True para todas las esquinas válidas"""
        assert small_board.is_inside(1, 1) is True  # Esquina inferior-izquierda
        assert small_board.is_inside(1, 3) is True  # Esquina superior-izquierda
        assert small_board.is_inside(3, 1) is True  # Esquina inferior-derecha
        assert small_board.is_inside(3, 3) is True  # Esquina superior-derecha
    
    def test_is_inside_returns_false_for_zero_coordinates(self, board):
        """Debe retornar False para coordenadas en cero"""
        assert board.is_inside(0, 5) is False
        assert board.is_inside(5, 0) is False
        assert board.is_inside(0, 0) is False
    
    def test_is_inside_returns_false_for_negative_coordinates(self, board):
        """Debe retornar False para coordenadas negativas"""
        assert board.is_inside(-1, 5) is False
        assert board.is_inside(5, -1) is False
        assert board.is_inside(-5, -5) is False
    
    def test_is_inside_returns_false_when_exceeds_width(self, board):
        """Debe retornar False cuando x excede el ancho"""
        assert board.is_inside(11, 5) is False
        assert board.is_inside(15, 5) is False
    
    def test_is_inside_returns_false_when_exceeds_height(self, board):
        """Debe retornar False cuando y excede la altura"""
        assert board.is_inside(5, 11) is False
        assert board.is_inside(5, 15) is False
    
    def test_is_inside_returns_false_when_both_coordinates_out_of_bounds(self, board):
        """Debe retornar False cuando ambas coordenadas están fuera"""
        assert board.is_inside(11, 11) is False
        assert board.is_inside(0, 11) is False


    # ==================== Tests de has_wall_at ====================
    
    def test_has_wall_at_returns_false_on_empty_board(self, board):
        """Debe retornar False cuando no hay paredes"""
        assert board.has_wall_at(5, 5) is False
    
    def test_has_wall_at_returns_true_when_wall_exists(self, board_with_walls):
        """Debe retornar True cuando existe una pared en la posición"""
        assert board_with_walls.has_wall_at(3, 3) is True
        assert board_with_walls.has_wall_at(7, 7) is True
    
    def test_has_wall_at_returns_false_when_wall_not_exists(self, board_with_walls):
        """Debe retornar False cuando no existe pared en la posición"""
        assert board_with_walls.has_wall_at(5, 5) is False
        assert board_with_walls.has_wall_at(1, 1) is False
    
    def test_has_wall_at_checks_exact_position(self, board_with_walls):
        """Debe verificar la posición exacta (no posiciones adyacentes)"""
        assert board_with_walls.has_wall_at(3, 3) is True
        assert board_with_walls.has_wall_at(3, 4) is False  # Adyacente
        assert board_with_walls.has_wall_at(4, 3) is False  # Adyacente


    # ==================== Tests de is_valid_position ====================
    
    def test_is_valid_position_returns_true_for_empty_valid_position(self, board):
        """Debe retornar True para posición válida sin pared"""
        assert board.is_valid_position(5, 5) is True
    
    def test_is_valid_position_returns_false_when_out_of_bounds(self, board):
        """Debe retornar False cuando está fuera del tablero"""
        assert board.is_valid_position(0, 5) is False
        assert board.is_valid_position(11, 5) is False
        assert board.is_valid_position(5, 0) is False
        assert board.is_valid_position(5, 11) is False
    
    def test_is_valid_position_returns_false_when_wall_exists(self, board_with_walls):
        """Debe retornar False cuando hay una pared en la posición"""
        assert board_with_walls.is_valid_position(3, 3) is False
        assert board_with_walls.is_valid_position(7, 7) is False
    
    def test_is_valid_position_returns_true_for_adjacent_to_wall(self, board_with_walls):
        """Debe retornar True para posiciones adyacentes a paredes"""
        assert board_with_walls.is_valid_position(3, 4) is True  # Al lado de pared
        assert board_with_walls.is_valid_position(4, 3) is True


    # ==================== Tests de add_wall ====================
    
    def test_add_wall_successfully(self, board, sample_wall):
        """Debe añadir una pared exitosamente"""
        board.add_wall(sample_wall)
        
        assert len(board.walls) == 1
        assert board.walls[0] == sample_wall
        assert board.has_wall_at(5, 5) is True
    
    def test_add_multiple_walls_successfully(self, board):
        """Debe añadir múltiples paredes exitosamente"""
        wall1 = Wall(x=2, y=2)
        wall2 = Wall(x=5, y=5)
        wall3 = Wall(x=8, y=8)
        
        board.add_wall(wall1)
        board.add_wall(wall2)
        board.add_wall(wall3)
        
        assert len(board.walls) == 3
        assert board.has_wall_at(2, 2) is True
        assert board.has_wall_at(5, 5) is True
        assert board.has_wall_at(8, 8) is True
    
    def test_add_wall_raises_when_out_of_bounds_x_too_low(self, board):
        """Debe lanzar excepción cuando x es menor que 1"""
        wall = Wall(x=0, y=5)
        
        with pytest.raises(WallOutOfBoundsException, match="fuera del tablero"):
            board.add_wall(wall)
    
    def test_add_wall_raises_when_out_of_bounds_x_too_high(self, board):
        """Debe lanzar excepción cuando x excede el ancho"""
        wall = Wall(x=11, y=5)
        
        with pytest.raises(WallOutOfBoundsException, match="fuera del tablero"):
            board.add_wall(wall)
    
    def test_add_wall_raises_when_out_of_bounds_y_too_low(self, board):
        """Debe lanzar excepción cuando y es menor que 1"""
        wall = Wall(x=5, y=0)
        
        with pytest.raises(WallOutOfBoundsException, match="fuera del tablero"):
            board.add_wall(wall)
    
    def test_add_wall_raises_when_out_of_bounds_y_too_high(self, board):
        """Debe lanzar excepción cuando y excede la altura"""
        wall = Wall(x=5, y=11)
        
        with pytest.raises(WallOutOfBoundsException, match="fuera del tablero"):
            board.add_wall(wall)
    
    def test_add_wall_raises_when_wall_already_exists(self, board):
        """Debe lanzar excepción cuando ya existe una pared en esa posición"""
        wall1 = Wall(x=5, y=5)
        wall2 = Wall(x=5, y=5)
        
        board.add_wall(wall1)
        
        with pytest.raises(WallAlreadyExistsException, match="Ya existe una pared"):
            board.add_wall(wall2)
    
    def test_add_wall_does_not_add_when_exception_raised(self, board):
        """No debe añadir la pared cuando se lanza una excepción"""
        wall = Wall(x=15, y=15)
        initial_count = len(board.walls)
        
        try:
            board.add_wall(wall)
        except WallOutOfBoundsException:
            pass
        
        assert len(board.walls) == initial_count
    
    def test_add_wall_at_boundaries(self, small_board):
        """Debe permitir añadir paredes en los límites del tablero"""
        wall1 = Wall(x=1, y=1)
        wall2 = Wall(x=1, y=3)
        wall3 = Wall(x=3, y=1)
        wall4 = Wall(x=3, y=3)
        
        small_board.add_wall(wall1)
        small_board.add_wall(wall2)
        small_board.add_wall(wall3)
        small_board.add_wall(wall4)
        
        assert len(small_board.walls) == 4
