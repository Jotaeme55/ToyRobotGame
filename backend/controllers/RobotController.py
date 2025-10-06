from flask import request, jsonify
from services.RobotService import RobotService
from services.BoardService import BoardService
from repositories.RobotRepository import RobotRepository
from repositories.BoardRepository import BoardRepository


class RobotController:
    """Controlador HTTP para gestionar el robot"""
    
    def __init__(self):
        board_service = BoardService(BoardRepository())
        self._robot_service = RobotService(RobotRepository(), board_service)
    
    def place(self):
        """Maneja POST /api/robot/place"""
        data = request.get_json()
        
        if not data:
            raise ValueError('Body JSON requerido')
        
        x = data.get('x')
        y = data.get('y')
        facing = data.get('facing')
        
        if x is None or y is None or not facing:
            raise ValueError('x, y y facing son requeridos')
        
        # Flask captura InvalidDirectionException y WallCollisionException automáticamente
        self._robot_service.place(int(x), int(y), facing.upper())
        
        return jsonify({
            'success': True,
            'message': f'Robot colocado en ({x}, {y}) mirando {facing.upper()}'
        }), 200
    
    def move(self):
        """Maneja POST /api/robot/move"""
        # Flask captura RobotNotPlacedException y WallCollisionException automáticamente
        self._robot_service.move()
        position = self._robot_service.report()
        
        x, y, facing = position
        return jsonify({
            'success': True,
            'message': f'Robot movido a ({x}, {y})',
            'position': {
                'x': x,
                'y': y,
                'facing': facing
            }
        }), 200
    
    def left(self):
        """Maneja POST /api/robot/left"""
        # Flask captura RobotNotPlacedException automáticamente
        self._robot_service.left()
        position = self._robot_service.report()
        
        x, y, facing = position
        return jsonify({
            'success': True,
            'message': f'Robot girado a la izquierda, ahora mira {facing}',
            'position': {
                'x': x,
                'y': y,
                'facing': facing
            }
        }), 200
    
    def right(self):
        """Maneja POST /api/robot/right"""
        # Flask captura RobotNotPlacedException automáticamente
        self._robot_service.right()
        position = self._robot_service.report()
        
        x, y, facing = position
        return jsonify({
            'success': True,
            'message': f'Robot girado a la derecha, ahora mira {facing}',
            'position': {
                'x': x,
                'y': y,
                'facing': facing
            }
        }), 200
    
    def report(self):
        """Maneja GET /api/robot/report"""
        position = self._robot_service.report()
        
        if position is None:
            return jsonify({
                'success': False,
                'message': 'El robot no ha sido colocado en el tablero'
            }), 404
        
        x, y, facing = position
        return jsonify({
            'success': True,
            'message': f'Robot en ({x}, {y}) mirando {facing}',
            'position': {
                'x': x,
                'y': y,
                'facing': facing
            }
        }), 200
    
    def delete(self):
        """Maneja DELETE /api/robot"""
        self._robot_service.delete_robot()
        
        return jsonify({
            'success': True,
            'message': 'Robot eliminado exitosamente'
        }), 200