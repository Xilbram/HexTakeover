import math

class Hexagono():
    def __init__(self):
        self.__side_len = 50
        self.__hexagon_height = (self.__side_len * math.sqrt(3)) / 2


    def get_side_length(self) -> int:
        return self.__side_len

    def get_hex_height(self):
        return self.__hexagon_height

