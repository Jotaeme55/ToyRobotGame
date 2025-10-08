import pytest
from models.Robot import Robot
from exceptions import InvalidDirectionException


class TestRobot:
    """Tests unitarios para el modelo Robot"""
    
    @pytest.fixture
    def robot(self):
        """Robot sin colocar"""
        return Robot()
    
    @pytest.fixture
    def placed_robot(self):
        """Robot ya colocado"""
        robot = Robot()
        robot.place(5, 5, 'NORTH')
        return robot


    # ==================== Tests de __init__ ====================
    
    def test_robot_initializes_with_none_values(self, robot):
        """Debe inicializar con valores None"""
        assert robot.x is None
        assert robot.y is None
        assert robot.facing is None


    # ==================== Tests de is_placed ====================
    
    def test_is_placed_returns_false_when_not_placed(self, robot):
        """Debe retornar False cuando no está colocado"""
        assert robot.is_placed() is False
    
    def test_is_placed_returns_true_when_placed(self, placed_robot):
        """Debe retornar True cuando está colocado"""
        assert placed_robot.is_placed() is True
    
    def test_is_placed_returns_false_when_partially_placed(self, robot):
        """Debe retornar False si no están todos los valores"""
        robot.x = 5
        robot.y = 5
        # facing es None
        assert robot.is_placed() is False


    # ==================== Tests de place ====================
    
    def test_place_sets_position_correctly(self, robot):
        """Debe colocar el robot en la posición correcta"""
        # Act
        robot.place(3, 7, 'EAST')
        
        # Assert
        assert robot.x == 3
        assert robot.y == 7
        assert robot.facing == 'EAST'
    
    def test_place_accepts_all_valid_directions(self, robot):
        """Debe aceptar todas las direcciones válidas"""
        for direction in ['NORTH', 'SOUTH', 'EAST', 'WEST']:
            robot.place(0, 0, direction)
            assert robot.facing == direction
    
    def test_place_raises_invalid_direction_exception(self, robot):
        """Debe lanzar excepción con dirección inválida"""
        with pytest.raises(InvalidDirectionException, match="no válida"):
            robot.place(5, 5, 'INVALID')
    
    
    def test_place_can_reposition_robot(self, placed_robot):
        """Debe poder reposicionar un robot ya colocado"""
        # Arrange
        assert placed_robot.x == 5
        
        # Act
        placed_robot.place(8, 3, 'WEST')
        
        # Assert
        assert placed_robot.x == 8
        assert placed_robot.y == 3
        assert placed_robot.facing == 'WEST'


    # ==================== Tests de turn_left ====================
    
    def test_turn_left_from_north(self, robot):
        """Debe girar correctamente desde NORTH"""
        robot.place(5, 5, 'NORTH')
        robot.turn_left()
        assert robot.facing == 'WEST'
    
    def test_turn_left_from_west(self, robot):
        """Debe girar correctamente desde WEST"""
        robot.place(5, 5, 'WEST')
        robot.turn_left()
        assert robot.facing == 'SOUTH'
    
    def test_turn_left_from_south(self, robot):
        """Debe girar correctamente desde SOUTH"""
        robot.place(5, 5, 'SOUTH')
        robot.turn_left()
        assert robot.facing == 'EAST'
    
    def test_turn_left_from_east(self, robot):
        """Debe girar correctamente desde EAST"""
        robot.place(5, 5, 'EAST')
        robot.turn_left()
        assert robot.facing == 'NORTH'
    
    def test_turn_left_full_rotation(self, placed_robot):
        """Debe volver a la dirección original después de 4 giros"""
        original_facing = placed_robot.facing
        
        for _ in range(4):
            placed_robot.turn_left()
        
        assert placed_robot.facing == original_facing
    
    def test_turn_left_does_not_change_position(self, placed_robot):
        """Girar no debe cambiar la posición"""
        original_x = placed_robot.x
        original_y = placed_robot.y
        
        placed_robot.turn_left()
        
        assert placed_robot.x == original_x
        assert placed_robot.y == original_y


    # ==================== Tests de turn_right ====================
    
    def test_turn_right_from_north(self, robot):
        """Debe girar correctamente desde NORTH"""
        robot.place(5, 5, 'NORTH')
        robot.turn_right()
        assert robot.facing == 'EAST'
    
    def test_turn_right_from_east(self, robot):
        """Debe girar correctamente desde EAST"""
        robot.place(5, 5, 'EAST')
        robot.turn_right()
        assert robot.facing == 'SOUTH'
    
    def test_turn_right_from_south(self, robot):
        """Debe girar correctamente desde SOUTH"""
        robot.place(5, 5, 'SOUTH')
        robot.turn_right()
        assert robot.facing == 'WEST'
    
    def test_turn_right_from_west(self, robot):
        """Debe girar correctamente desde WEST"""
        robot.place(5, 5, 'WEST')
        robot.turn_right()
        assert robot.facing == 'NORTH'
    
    def test_turn_right_full_rotation(self, placed_robot):
        """Debe volver a la dirección original después de 4 giros"""
        original_facing = placed_robot.facing
        
        for _ in range(4):
            placed_robot.turn_right()
        
        assert placed_robot.facing == original_facing
    
    def test_turn_right_does_not_change_position(self, placed_robot):
        """Girar no debe cambiar la posición"""
        original_x = placed_robot.x
        original_y = placed_robot.y
        
        placed_robot.turn_right()
        
        assert placed_robot.x == original_x
        assert placed_robot.y == original_y
    
    def test_turn_left_and_right_cancel_out(self, placed_robot):
        """Girar izquierda y derecha debe cancelarse"""
        original_facing = placed_robot.facing
        
        placed_robot.turn_left()
        placed_robot.turn_right()
        
        assert placed_robot.facing == original_facing


    # ==================== Tests de get_position ====================
    
    def test_get_position_returns_correct_tuple(self, placed_robot):
        """Debe retornar una tupla con la posición correcta"""
        result = placed_robot.get_position()
        
        assert result == (5, 5, 'NORTH')
        assert isinstance(result, tuple)
        assert len(result) == 3


    # ==================== Tests de get_next_position ====================
    
    def test_get_next_position_north(self, robot):
        """Debe calcular correctamente la siguiente posición hacia NORTH"""
        robot.place(5, 5, 'NORTH')
        next_x, next_y = robot.get_next_position()
        
        assert next_x == 6  # x + 1
        assert next_y == 5  # y no cambia
    
    def test_get_next_position_south(self, robot):
        """Debe calcular correctamente la siguiente posición hacia SOUTH"""
        robot.place(5, 5, 'SOUTH')
        next_x, next_y = robot.get_next_position()
        
        assert next_x == 4  # x - 1
        assert next_y == 5  # y no cambia
    
    def test_get_next_position_east(self, robot):
        """Debe calcular correctamente la siguiente posición hacia EAST"""
        robot.place(5, 5, 'EAST')
        next_x, next_y = robot.get_next_position()
        
        assert next_x == 5  # x no cambia
        assert next_y == 6  # y + 1
    
    def test_get_next_position_west(self, robot):
        """Debe calcular correctamente la siguiente posición hacia WEST"""
        robot.place(5, 5, 'WEST')
        next_x, next_y = robot.get_next_position()
        
        assert next_x == 5  # x no cambia
        assert next_y == 4  # y - 1
    
    def test_get_next_position_does_not_move_robot(self, placed_robot):
        """Obtener siguiente posición no debe mover el robot"""
        original_x = placed_robot.x
        original_y = placed_robot.y
        
        placed_robot.get_next_position()
        
        assert placed_robot.x == original_x
        assert placed_robot.y == original_y
