from flask import Flask, jsonify
from flask_cors import CORS
from controllers.BoardController import BoardController
from controllers.RobotController import RobotController
from exceptions import (
    WallOutOfBoundsException,
    WallAlreadyExistsException,
    RobotNotPlacedException,
    WallCollisionException,
    InvalidDirectionException
)

app = Flask(__name__)
CORS(app)  # Permitir peticiones desde el frontend

# Inicializar controladores
board_controller = BoardController()
robot_controller = RobotController()


# ============================================================================
# ERROR HANDLERS GLOBALES
# ============================================================================

@app.errorhandler(ValueError)
def handle_value_error(e):
    """Maneja errores de validación de datos"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(WallOutOfBoundsException)
def handle_wall_out_of_bounds(e):
    """Maneja paredes fuera del tablero"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(WallAlreadyExistsException)
def handle_wall_already_exists(e):
    """Maneja paredes duplicadas"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(WallCollisionException)
def handle_wall_collision(e):
    """Maneja colisiones con paredes"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(RobotNotPlacedException)
def handle_robot_not_placed(e):
    """Maneja robot no colocado"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(InvalidDirectionException)
def handle_invalid_direction(e):
    """Maneja direcciones inválidas"""
    return jsonify({
        'success': False,
        'message': str(e)
    }), 400


@app.errorhandler(404)
def not_found(error):
    """Maneja endpoints no encontrados"""
    return jsonify({
        'success': False,
        'message': 'Endpoint no encontrado'
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    """Maneja métodos HTTP no permitidos"""
    return jsonify({
        'success': False,
        'message': 'Método HTTP no permitido para este endpoint'
    }), 405


@app.errorhandler(Exception)
def handle_generic_error(e):
    """Maneja cualquier error no previsto"""
    return jsonify({
        'success': False,
        'message': f'Error inesperado: {str(e)}'
    }), 500


# ============================================================================
# RUTAS DEL BOARD
# ============================================================================

@app.route('/api/board', methods=['POST'])
def create_board():
    """POST /api/board - Crear tablero"""
    return board_controller.create()


@app.route('/api/board', methods=['GET'])
def get_board():
    """GET /api/board - Obtener tablero"""
    return board_controller.get()


@app.route('/api/board', methods=['DELETE'])
def delete_board():
    """DELETE /api/board - Eliminar tablero"""
    return board_controller.delete()


@app.route('/api/board/wall', methods=['POST'])
def add_wall():
    """POST /api/board/wall - Añadir pared"""
    return board_controller.add_wall()


# ============================================================================
# RUTAS DEL ROBOT
# ============================================================================

@app.route('/api/robot/place', methods=['POST'])
def place_robot():
    """POST /api/robot/place - Colocar robot"""
    return robot_controller.place()


@app.route('/api/robot/move', methods=['POST'])
def move_robot():
    """POST /api/robot/move - Mover robot"""
    return robot_controller.move()


@app.route('/api/robot/left', methods=['POST'])
def turn_left():
    """POST /api/robot/left - Girar izquierda"""
    return robot_controller.left()


@app.route('/api/robot/right', methods=['POST'])
def turn_right():
    """POST /api/robot/right - Girar derecha"""
    return robot_controller.right()


@app.route('/api/robot/report', methods=['GET'])
def report_robot():
    """GET /api/robot/report - Obtener posición"""
    return robot_controller.report()


@app.route('/api/robot', methods=['DELETE'])
def delete_robot():
    """DELETE /api/robot - Eliminar robot"""
    return robot_controller.delete()


# ============================================================================
# ENDPOINT DE SALUD
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """GET /api/health - Health check"""
    return jsonify({
        'status': 'ok',
        'message': 'Robot Game API is running'
    }), 200


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)