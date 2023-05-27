from typing import Dict

class Tabuleiro:
    # constants
    MAP_HEIGHT = 10

    def __init__(self):
        self.hexagons = []
        self.hexagon_colors = []
        self.selected_hexagon = None
        self.game_state = 1
        self.COLORS = {
            'player_1': '#4260f5',
            'player_1_selected': '#4290f5',
            'player_0': '#f55142',
            'player_0_selected': '#f54290',
            'inner_adjacent': '#55be4e',
            'outer_adjacent': '#cb7409',
            'outline': '#303030',
            'unselected': '#ffffff',
            'out_of_map': '#303030'
        }

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
        self.cont_hex_j0 = 0
        self.cont_hex_j1 = 0
        self.cont_jogadas_j0 = 0
        self.cont_jogadas_j1 = 0
        for k in range(20, 170):
            possibles = self.get_possible(self.hexagons[k])
            if self.hexagon_colors[k] == corRemoto:
                self.cont_hex_j0 += 1
                self.cont_jogadas_j0 += len(possibles[k])
            if self.hexagon_colors[k] == corLocal:
                self.cont_hex_j1 += 1
                self.cont_jogadas_j1 += len(possibles[k])

        if self.cont_jogadas_j1 == 0 or self.cont_jogadas_j0 == 0:
            self.game_state = 4
            if self.cont_hex_j0 < self.cont_hex_j1:
                return ("Vermelho", self.cont_hex_j1)
            else:
                return ("Azul", self.cont_hex_j0)
        return None


