# tests/unit/controllers/test_board_controllers.py
import pytest
from unittest.mock import Mock
from flask import Flask
from werkzeug.exceptions import BadRequest
from controllers.BoardController import BoardController
from models.Board import Board
from models.Wall import Wall


@pytest.fixture
def app():
    """Crea una app Flask mínima para el contexto"""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_board_service():
    return Mock()


@pytest.fixture
def board_controller(mock_board_service):
    return BoardController(mock_board_service)


class TestBoardControllerCreateUnit:
    """Tests unitarios con contexto Flask"""
    
    def test_create_board_success(self, app, board_controller, mock_board_service):
        """Debe crear un tablero exitosamente"""
        # Arrange
        mock_board = Board(10, 10)
        mock_board_service.create_or_get_board.return_value = mock_board
        
        # Act
        with app.test_request_context(
            '/api/board',
            method='POST',
            json={'width': 10, 'height': 10},
            content_type='application/json'
        ):
            response, status_code = board_controller.create()
        
        # Assert
        assert status_code == 201
        mock_board_service.create_or_get_board.assert_called_once_with(10, 10)
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Tablero 10x10 creado exitosamente'
    
    def test_create_board_without_body(self, app, board_controller, mock_board_service):
        """Debe lanzar BadRequest si el body JSON es inválido"""
        # Act & Assert - Flask lanza BadRequest antes de llegar al controlador
        with app.test_request_context(
            '/api/board',
            method='POST',
            data='',
            content_type='application/json'
        ):
            with pytest.raises(BadRequest):
                board_controller.create()
        
        mock_board_service.create_or_get_board.assert_not_called()
    
    def test_create_board_with_empty_json(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si el JSON está vacío"""
        # Act & Assert - {} evalúa a False, entonces dispara 'Body JSON requerido'
        with app.test_request_context(
            '/api/board',
            method='POST',
            json={},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='Body JSON requerido'):  # ← Cambio aquí
                board_controller.create()
        
        mock_board_service.create_or_get_board.assert_not_called()
    
    def test_create_board_without_width(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si falta width"""
        # Act & Assert
        with app.test_request_context(
            '/api/board',
            method='POST',
            json={'height': 10},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='width y height son requeridos'):
                board_controller.create()
        
        mock_board_service.create_or_get_board.assert_not_called()
    
    def test_create_board_without_height(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si falta height"""
        # Act & Assert
        with app.test_request_context(
            '/api/board',
            method='POST',
            json={'width': 10},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='width y height son requeridos'):
                board_controller.create()
        
        mock_board_service.create_or_get_board.assert_not_called()
    
    def test_create_board_with_zero_values(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError con valores cero"""
        # Act & Assert
        with app.test_request_context(
            '/api/board',
            method='POST',
            json={'width': 0, 'height': 0},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='width y height son requeridos'):
                board_controller.create()


class TestBoardControllerGetUnit:
    """Tests unitarios para GET"""
    
    def test_get_board_success(self, app, board_controller, mock_board_service):
        """Debe obtener el tablero exitosamente"""
        # Arrange
        mock_board = Board(5, 5)
        mock_board.add_wall(Wall(1, 1))
        mock_board.add_wall(Wall(2, 2))
        mock_board_service.get_board.return_value = mock_board
        
        # Act
        with app.test_request_context('/api/board', method='GET'):
            response, status_code = board_controller.get()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['width'] == 5
        assert data['height'] == 5
        assert len(data['walls']) == 2
    
    def test_get_board_not_exists(self, app, board_controller, mock_board_service):
        """Debe devolver 404 si no existe tablero"""
        # Arrange
        mock_board_service.get_board.return_value = None
        
        # Act
        with app.test_request_context('/api/board', method='GET'):
            response, status_code = board_controller.get()
        
        # Assert
        assert status_code == 404
        data = response.get_json()
        assert data['success'] is False


class TestBoardControllerDeleteUnit:
    """Tests unitarios para DELETE"""
    
    def test_delete_board_success(self, app, board_controller, mock_board_service):
        """Debe eliminar el tablero exitosamente"""
        # Act
        with app.test_request_context('/api/board', method='DELETE'):
            response, status_code = board_controller.delete()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        mock_board_service.delete_board.assert_called_once()


class TestBoardControllerAddWallUnit:
    """Tests unitarios para POST /wall"""
    
    def test_add_wall_success(self, app, board_controller, mock_board_service):
        """Debe añadir una pared exitosamente"""
        # Act
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            json={'x': 3, 'y': 4},
            content_type='application/json'
        ):
            response, status_code = board_controller.add_wall()
        
        # Assert
        assert status_code == 201
        data = response.get_json()
        assert data['success'] is True
        mock_board_service.add_wall.assert_called_once()
        wall_arg = mock_board_service.add_wall.call_args[0][0]
        assert isinstance(wall_arg, Wall)
        assert wall_arg.x == 3
        assert wall_arg.y == 4
    
    def test_add_wall_without_body(self, app, board_controller, mock_board_service):
        """Debe lanzar BadRequest si el body JSON es inválido"""
        # Act & Assert
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            data='',
            content_type='application/json'
        ):
            with pytest.raises(BadRequest):
                board_controller.add_wall()
        
        mock_board_service.add_wall.assert_not_called()
    
    def test_add_wall_with_empty_json(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si el JSON está vacío"""
        # Act & Assert - {} evalúa a False, entonces dispara 'Body JSON requerido'
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            json={},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='Body JSON requerido'):  # ← Cambio aquí
                board_controller.add_wall()
    
    def test_add_wall_without_x(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si falta x"""
        # Act & Assert
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            json={'y': 5},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='x e y son requeridos'):
                board_controller.add_wall()
    
    def test_add_wall_without_y(self, app, board_controller, mock_board_service):
        """Debe lanzar ValueError si falta y"""
        # Act & Assert
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            json={'x': 5},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='x e y son requeridos'):
                board_controller.add_wall()
    
    def test_add_wall_with_zero_coordinates(self, app, board_controller, mock_board_service):
        """Debe aceptar coordenadas cero (x=0, y=0 es válido pero None no lo es)"""
        # Act
        with app.test_request_context(
            '/api/board/wall',
            method='POST',
            json={'x': 0, 'y': 0},
            content_type='application/json'
        ):
            response, status_code = board_controller.add_wall()
        
        # Assert
        assert status_code == 201
        mock_board_service.add_wall.assert_called_once()