import math
import tkinter as tk
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

    def getGameState(self):
        return self.game_state

    def setGameState(self, state):
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
            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 1)
                adjacent_hexagons.append(hexagon_index - self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index - (self.MAP_HEIGHT + 1))
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 1)
                adjacent_hexagons.append(hexagon_index + self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index + (self.MAP_HEIGHT - 1))
        else:
            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 1)
                adjacent_hexagons.append(hexagon_index - self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index - (self.MAP_HEIGHT - 1))
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 1)
                adjacent_hexagons.append(hexagon_index + self.MAP_HEIGHT)
                adjacent_hexagons.append(hexagon_index + (self.MAP_HEIGHT + 1))

        print(adjacent_hexagons)
        return adjacent_hexagons

    def checkGameOver(self, corRemoto, corLocal) -> (str, int):
        self.cont_j0 = 0
        self.cont_j1 = 0
        self.cont_jog_j0 = 0
        self.cont_jog_j1 = 0
        for k in range(20, 170):
            possibles = self.get_possible(self.hexagons[k])
            if self.hexagon_colors[k] == corRemoto:
                self.cont_j0 += 1
                if self.cont_jog_j0 == 0:
                    self.cont_jog_j0 = len(possibles[0]) + len(possibles[1])
            if self.hexagon_colors[k] == corLocal:
                self.cont_j1 += 1
                if self.cont_jog_j1 == 0:
                    self.cont_jog_j1 = len(possibles[0]) + len(possibles[1])
        if self.cont_j0 + self.cont_j1 == 75:
            if self.cont_j0 < self.cont_j1:
                return ("Vermelho", self.cont_j1)

            else:
                return ("Azul", self.cont_j0)

        if self.cont_j0 == 0 or self.cont_jog_j0 == 0:
            return ("Vermelho", self.cont_j1)

        elif self.cont_j1 == 0 or self.cont_jog_j1 == 0:
            return ("Azul", self.cont_j0)


        return None


