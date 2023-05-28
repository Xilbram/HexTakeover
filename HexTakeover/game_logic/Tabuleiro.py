from typing import Dict
from .Hexagono import Hexagono
from .Jogador import Jogador

class Tabuleiro:
    # constants
    MAP_HEIGHT = 10

    def __init__(self):
        self.hexagons = []
        self.hexagon_colors = []
        self.genHexagon = Hexagono()
        self.selected_hexagon = None

        self.game_state = 1

        self.local_player_id = None
        self.remote_player_id = None
        self.local_player = Jogador('#f55142', self.local_player_id, '#f54290')
        self.remote_player = Jogador('#4260f5', self.remote_player_id, '#4290f5')
        self.current_player_id = 0

        self.COLORS = {
            'inner_adjacent': '#55be4e',
            'outer_adjacent': '#cb7409',
            'outline': '#303030',
            'unselected': '#ffffff',
            'out_of_map': '#303030'
        }

    def get_cor_jogador_vez(self, swap=False):
        if swap:
            if self.local_player_id == 0:
                return self.remote_player.get_color()
            else:
                return self.local_player.get_color()
        else:
            if self.local_player_id == 0:
                return self.local_player.get_color()
            else:
                return self.remote_player.get_color()

    def get_cor_selecionada_jogador_vez(self, swap=False):
        if swap:
            if self.local_player_id == 0:
                return self.remote_player.get_color_selecao()
            else:
                return self.local_player.get_color_selecao()
        else:
            if self.local_player_id == 0:
                return self.local_player.get_color_selecao()
            else:
                return self.remote_player.get_color_selecao()

    def get_game_state(self):
        return self.game_state

    def set_game_state(self, state):
        self.game_state = state

    def get_possible(self, hexagon_index):
        clone_possible = []
        jump_possible = []
        inner_adjacent_hexagons = self.get_adjacent_hexagons(hexagon_index)
        for i in inner_adjacent_hexagons:
            if self.hexagon_colors[i] != self.COLORS['out_of_map']:
                if self.hexagon_colors[i] == self.COLORS['unselected']:
                    clone_possible.append(i)
                outer_adjacent_hexagons = self.get_adjacent_hexagons(i)
                for j in outer_adjacent_hexagons:
                    if self.hexagon_colors[j] == self.COLORS['unselected']:
                        jump_possible.append(j)
        return [clone_possible, jump_possible]

    def get_adjacent_hexagons(self, hexagon_index):
        adjacent_hexagons = []
        if hexagon_index // self.MAP_HEIGHT % 2 == 0:
                adjacent_hexagons.append(hexagon_index - 1)
                adjacent_hexagons.append(hexagon_index - self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index + 1)
                adjacent_hexagons.append(hexagon_index + self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index - (self.MAP_HEIGHT + 1))
                adjacent_hexagons.append(hexagon_index + (self.MAP_HEIGHT - 1))
        else:
                adjacent_hexagons.append(hexagon_index - 1)
                adjacent_hexagons.append(hexagon_index - self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index + 1)
                adjacent_hexagons.append(hexagon_index + self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index - (self.MAP_HEIGHT - 1))
                adjacent_hexagons.append(hexagon_index + (self.MAP_HEIGHT + 1))
        return adjacent_hexagons

    def check_game_over(self, corRemoto, corLocal):
        self.cont_hex_j0 = 7
        self.cont_hex_j1 = 7
        self.cont_jogadas_j0 = 0
        self.cont_jogadas_j1 = 0
        for k in range(20, 170):
            possibles = self.get_possible(self.hexagons[k])
            if self.hexagon_colors[k] == corRemoto:
                self.cont_hex_j0 += 1
                self.cont_jogadas_j0 += (len(possibles[0])+len(possibles[1]))
            if self.hexagon_colors[k] == corLocal:
                self.cont_hex_j1 += 1
                self.cont_jogadas_j1 += (len(possibles[0])+len(possibles[1]))
        print(self.cont_jogadas_j1,self.cont_jogadas_j0)
        if self.cont_jogadas_j1 == 0 or self.cont_jogadas_j0 == 0:
            self.game_state = 4
            if self.cont_hex_j0 < self.cont_hex_j1:
                return ("Vermelho", self.cont_hex_j1)
            else:
                return ("Azul", self.cont_hex_j0)


    def toggle_player(self):
        if self.current_player_id == 0:
            self.current_player_id = 1
        else:
            self.current_player_id = 0
        if self.current_player_id == self.local_player_id:
            self.set_game_state(2)
        else:
            self.set_game_state(3)

