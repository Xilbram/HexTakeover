
class Hexagono:
    def init(self, pos: tuple):
        self.__pos: tuple = pos
        self.__side_lenght = 50


    def getPos(self) -> tuple:
        return self.__pos

    def getSideLen(self):
        return self.__side_lenght

