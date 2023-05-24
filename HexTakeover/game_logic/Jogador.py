class Jogador:
    def __init__(self, cor,id,cor_selecao):
        self.__cor: str = cor
        self.__cor_selecao: str = cor_selecao
        self.__turno: bool = False
        self.__id: str = id
        self.__total_hexagonos = 0
        self.__vencedor = False

    def reset(self):
        self.__total_hexagonos = 0
        self.__hexagonos = []
        self.__vencedor = False

    def get_total_hexagonos(self):
        return self.__total_hexagonos
    
    def increase_total_hexagonos(self, num):
        self.__total_hexagonos += num

    def get_color(self):
        return self.__cor

    def get_id(self):
        return self.__id
    def get_color_selecao(self):
        return self.__cor_selecao



