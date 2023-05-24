class Jogador:
    def __init__(self, cor,id,cor_selecao ):
        self.__cor: str = cor
        self.__cor_selecao: str = cor_selecao
        self.__turno: bool = False
        self.__id: str = id
        self.__hexagonos = []
        self.__totalHexagonos = 0
        self.__vencedor = False

    def reset(self):
        self.__totalHexagonos = 0
        self.__hexagonos = []
        self.__vencedor = False

    def getTotalHexagonos(self):
        return self.__totalHexagonos
    def increaseTotalHexagonos(self, num):
        self.__totalHexagonos += num

    def getColor(self):
        return self.__cor

    def getId(self):
        return self.__id
    def getColorSelecao(self):
        return self.__cor_selecao
    def getHexagonos(self) -> []:
        return self.__hexagonos

    def setHexagonos(self, newArr):
        self.__hexagonos = newArr

    def getHexLen(self):
        self.__hexagonos[0].getSideLenght()