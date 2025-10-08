# tests/unit/controllers/test_robot_controller.py
import pytest
from unittest.mock import Mock
from flask import Flask
from werkzeug.exceptions import BadRequest
from controllers.RobotController import RobotController


@pytest.fixture
def app():
    """Crea una app Flask mínima para el contexto"""
    app = Flask(__name__)
    return app


@pytest.fixture
def mock_robot_service():
    return Mock()


@pytest.fixture
def robot_controller(mock_robot_service):
    return RobotController(mock_robot_service)


class TestRobotControllerPlace:
    """Tests para POST /api/robot/place"""
    
    def test_place_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe colocar el robot exitosamente"""
        # Act
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'x': 2, 'y': 3, 'facing': 'north'},
            content_type='application/json'
        ):
            response, status_code = robot_controller.place()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot colocado en (2, 3) mirando NORTH'
        mock_robot_service.place.assert_called_once_with(2, 3, 'NORTH')
    
    def test_place_robot_uppercase_facing(self, app, robot_controller, mock_robot_service):
        """Debe convertir facing a mayúsculas"""
        # Act
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'x': 0, 'y': 0, 'facing': 'south'},
            content_type='application/json'
        ):
            response, status_code = robot_controller.place()
        
        # Assert
        mock_robot_service.place.assert_called_once_with(0, 0, 'SOUTH')
    
    def test_place_robot_without_body(self, app, robot_controller, mock_robot_service):
        """Debe lanzar BadRequest si el body es inválido"""
        # Act & Assert
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            data='',
            content_type='application/json'
        ):
            with pytest.raises(BadRequest):
                robot_controller.place()
        
        mock_robot_service.place.assert_not_called()
    
    def test_place_robot_with_empty_json(self, app, robot_controller, mock_robot_service):
        """Debe lanzar ValueError si el JSON está vacío"""
        # Act & Assert
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='Body JSON requerido'):
                robot_controller.place()
        
        mock_robot_service.place.assert_not_called()
    
    def test_place_robot_without_x(self, app, robot_controller, mock_robot_service):
        """Debe lanzar ValueError si falta x"""
        # Act & Assert
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'y': 3, 'facing': 'north'},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='x, y y facing son requeridos'):
                robot_controller.place()
        
        mock_robot_service.place.assert_not_called()
    
    def test_place_robot_without_y(self, app, robot_controller, mock_robot_service):
        """Debe lanzar ValueError si falta y"""
        # Act & Assert
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'x': 2, 'facing': 'north'},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='x, y y facing son requeridos'):
                robot_controller.place()
        
        mock_robot_service.place.assert_not_called()
    
    def test_place_robot_without_facing(self, app, robot_controller, mock_robot_service):
        """Debe lanzar ValueError si falta facing"""
        # Act & Assert
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'x': 2, 'y': 3},
            content_type='application/json'
        ):
            with pytest.raises(ValueError, match='x, y y facing son requeridos'):
                robot_controller.place()
        
        mock_robot_service.place.assert_not_called()
    
    def test_place_robot_with_zero_coordinates(self, app, robot_controller, mock_robot_service):
        """Debe aceptar coordenadas cero (son válidas)"""
        # Act
        with app.test_request_context(
            '/api/robot/place',
            method='POST',
            json={'x': 0, 'y': 0, 'facing': 'east'},
            content_type='application/json'
        ):
            response, status_code = robot_controller.place()
        
        # Assert
        assert status_code == 200
        mock_robot_service.place.assert_called_once_with(0, 0, 'EAST')


class TestRobotControllerMove:
    """Tests para POST /api/robot/move"""
    
    def test_move_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe mover el robot exitosamente"""
        # Arrange
        mock_robot_service.report.return_value = (3, 4, 'NORTH')
        
        # Act
        with app.test_request_context('/api/robot/move', method='POST'):
            response, status_code = robot_controller.move()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot movido a (3, 4)'
        assert data['position']['x'] == 3
        assert data['position']['y'] == 4
        assert data['position']['facing'] == 'NORTH'
        mock_robot_service.move.assert_called_once()
        mock_robot_service.report.assert_called_once()


class TestRobotControllerLeft:
    """Tests para POST /api/robot/left"""
    
    def test_left_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe girar el robot a la izquierda exitosamente"""
        # Arrange
        mock_robot_service.report.return_value = (2, 3, 'WEST')
        
        # Act
        with app.test_request_context('/api/robot/left', method='POST'):
            response, status_code = robot_controller.left()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot girado a la izquierda, ahora mira WEST'
        assert data['position']['x'] == 2
        assert data['position']['y'] == 3
        assert data['position']['facing'] == 'WEST'
        mock_robot_service.left.assert_called_once()
        mock_robot_service.report.assert_called_once()


class TestRobotControllerRight:
    """Tests para POST /api/robot/right"""
    
    def test_right_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe girar el robot a la derecha exitosamente"""
        # Arrange
        mock_robot_service.report.return_value = (1, 2, 'EAST')
        
        # Act
        with app.test_request_context('/api/robot/right', method='POST'):
            response, status_code = robot_controller.right()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot girado a la derecha, ahora mira EAST'
        assert data['position']['x'] == 1
        assert data['position']['y'] == 2
        assert data['position']['facing'] == 'EAST'
        mock_robot_service.right.assert_called_once()
        mock_robot_service.report.assert_called_once()


class TestRobotControllerReport:
    """Tests para GET /api/robot/report"""
    
    def test_report_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe obtener la posición del robot exitosamente"""
        # Arrange
        mock_robot_service.report.return_value = (5, 5, 'SOUTH')
        
        # Act
        with app.test_request_context('/api/robot/report', method='GET'):
            response, status_code = robot_controller.report()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot en (5, 5) mirando SOUTH'
        assert data['position']['x'] == 5
        assert data['position']['y'] == 5
        assert data['position']['facing'] == 'SOUTH'
        mock_robot_service.report.assert_called_once()
    
    def test_report_robot_not_placed(self, app, robot_controller, mock_robot_service):
        """Debe devolver 404 si el robot no está colocado"""
        # Arrange
        mock_robot_service.report.return_value = None
        
        # Act
        with app.test_request_context('/api/robot/report', method='GET'):
            response, status_code = robot_controller.report()
        
        # Assert
        assert status_code == 404
        data = response.get_json()
        assert data['success'] is False
        assert data['message'] == 'El robot no ha sido colocado en el tablero'
        mock_robot_service.report.assert_called_once()


class TestRobotControllerDelete:
    """Tests para DELETE /api/robot"""
    
    def test_delete_robot_success(self, app, robot_controller, mock_robot_service):
        """Debe eliminar el robot exitosamente"""
        # Act
        with app.test_request_context('/api/robot', method='DELETE'):
            response, status_code = robot_controller.delete()
        
        # Assert
        assert status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['message'] == 'Robot eliminado exitosamente'
        mock_robot_service.delete_robot.assert_called_once()