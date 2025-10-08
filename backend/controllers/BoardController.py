from flask import request, jsonify
from services.BoardService import BoardService
from models.Wall import Wall


class BoardController:
    """Controlador HTTP para gestionar el tablero"""
    
    def __init__(self, board_service: BoardService):
        self._board_service = board_service
    
    def create(self):
        """Maneja POST /api/board"""
        data = request.get_json()
        
        if not data:
            raise ValueError('Body JSON requerido')
        
        width = data.get('width')
        height = data.get('height')
        
        if not width or not height:
            raise ValueError('width y height son requeridos')
        
        # Flask maneja automáticamente las excepciones
        board = self._board_service.create_or_get_board(int(width), int(height))
        
        return jsonify({
            'success': True,
            'message': f'Tablero {width}x{height} creado exitosamente',
            'board': {
                'width': board.width,
                'height': board.height
            }
        }), 201
    
    def get(self):
        """Maneja GET /api/board"""
        board = self._board_service.get_board()
        
        if board is None:
            return jsonify({
                'success': False,
                'message': 'No existe un tablero creado'
            }), 404
        
        return jsonify({
            'success': True,
            'width': board.width,
            'height': board.height,
            'walls': [[w.x, w.y] for w in board.walls]
        }), 200
    
    def delete(self):
        """Maneja DELETE /api/board"""
        self._board_service.delete_board()
        
        return jsonify({
            'success': True,
            'message': 'Tablero eliminado exitosamente'
        }), 200
    
    def add_wall(self):

        """Maneja POST /api/board/wall"""
        data = request.get_json()
        
        if not data:
            raise ValueError('Body JSON requerido')
        
        x = data.get('x')
        y = data.get('y')
        
        if x is None or y is None:
            raise ValueError('x e y son requeridos')
        
        # Flask captura WallOutOfBoundsException y WallAlreadyExistsException automáticamente
        wall = Wall(int(x), int(y))
        self._board_service.add_wall(wall)
        
        return jsonify({
            'success': True,
            'message': f'Pared añadida en ({x}, {y})'
        }), 201