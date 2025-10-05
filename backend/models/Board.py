from models.Wall import Wall

class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls : list[Wall] = None


    def is_valid_position(self, x, y)->bool:
        # Funcion que comprueba si la posicion esta dentro del tablero y si la posicion ya tiene una pared
        if x < 1 or y < 1 or x > self.width or y > self.height:
            return False
        
        for wall in self.walls:
            if (wall.x, wall.y) == (x,y):
                return False
            
        return True
    
    def is_inside(self,x ,y)->bool:
        if x < 1 or y < 1 or x > self.width or y > self.height:
            return False
        
        return True
    
    def add_wall(self, wall):
        if self.is_inside(wall.get_x(), wall.get_y()):
            self.walls.append(wall)
            return True
        return False