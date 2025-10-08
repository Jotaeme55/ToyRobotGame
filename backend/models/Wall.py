from typing import Optional

class Wall:
    def __init__(self,x, y):
        self.x = x
        self.y = y

    def get_x(self)->Optional[int]:
        return self.x
    
    def get_y(self)->Optional[int]:
        return self.y