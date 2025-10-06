class GameException(Exception):
    """Excepción base del juego"""
    pass


# Excepciones del Board
class WallOutOfBoundsException(GameException):
    """La pared está fuera de los límites del tablero"""
    pass


class WallAlreadyExistsException(GameException):
    """Ya existe una pared en esa posición"""
    pass


# Excepciones del Robot
class RobotNotPlacedException(GameException):
    """El robot no ha sido colocado en el tablero"""
    pass


class InvalidPositionException(GameException):
    """La posición especificada no es válida"""
    pass


class InvalidDirectionException(GameException):
    """La dirección especificada no es válida"""
    pass


class RobotOutOfBoundsException(GameException):
    """El robot está fuera de los límites del tablero"""
    pass


class WallCollisionException(GameException):
    """El robot colisionaría con una pared"""
    pass