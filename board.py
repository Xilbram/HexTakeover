import math
import tkinter as tk


class Board:

    # constants
    HEX_SIDE_LENGTH = 30
    MAP_WIDTH = 30
    MAP_HEIGHT = 10
    COLORS = {
        'player_1': '#4260f5',
        'player_2': '#f55142',
        'inner_adjacent': '#55be4e',
        'outer_adjacent': '#cb7409',
        'outline': '#000000',
        'unselected': '#ffffff',
        'out_of_map': '#303030'
    }

    def __init__(self):
        self.hexagons = []
        self.hexagon_colors = []
        self.selected_hexagon = None
        self.canvas = None

    def run(self):
        root = tk.Tk()
        root.title("Hex Takeover")
        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.pack()

        hexagon_height = (self.HEX_SIDE_LENGTH * math.sqrt(3)) / 2

        for i in range(self.MAP_WIDTH):
            for j in range(self.MAP_HEIGHT):
                x = i * 1.5 * self.HEX_SIDE_LENGTH
                y = j * (hexagon_height * 2) + ((i % 2) * hexagon_height)
                outline_color = self.COLORS['outline']

                condicoes = {
                    (5, 5): self.COLORS['player_2'],
                    (10, 5): self.COLORS['player_1'],
                    (11, 3): self.COLORS['player_1'],
                    (7, 3): self.COLORS['player_1'],
                    (16, 3): self.COLORS['player_1']
                }

                if (i, j) in condicoes:
                    fill_color = condicoes[(i, j)]
                else:
                    fill_color = self.COLORS['unselected']

                # defining map borders
                if i < 3 or i > 16 or j < 2 or j > 6:
                    fill_color = self.COLORS['out_of_map']

                # represent the vertices (start at the left vertex and continue counterclockwise)
                vertices = [
                    x - self.HEX_SIDE_LENGTH, y,
                    x - self.HEX_SIDE_LENGTH / 2, y + hexagon_height,
                    x + self.HEX_SIDE_LENGTH / 2, y + hexagon_height,
                    x + self.HEX_SIDE_LENGTH, y,
                    x + self.HEX_SIDE_LENGTH / 2, y - hexagon_height,
                    x - self.HEX_SIDE_LENGTH / 2, y - hexagon_height
                ]

                hexagon = self.canvas.create_polygon(vertices, fill=fill_color, outline=outline_color)

                self.hexagons.append(hexagon)
                self.hexagon_colors.append(fill_color)

                self.canvas.tag_bind(hexagon, '<Button-1>',
                                     lambda event, hexagon=hexagon: self.on_hexagon_clicked(event, hexagon))

        root.mainloop()

    def on_hexagon_clicked(self, event, hexagon):
        for i in range(len(self.hexagon_colors)):
            if self.hexagon_colors[i] == self.COLORS['inner_adjacent'] or self.hexagon_colors[i] == self.COLORS['outer_adjacent']:
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['unselected'])
                self.hexagon_colors[i] = self.COLORS['unselected']

        hexagon_index = self.hexagons.index(hexagon)

        hexagon_color = self.hexagon_colors[hexagon_index]

        # Change the color of the clicked hexagon to green if it's not already green
        if hexagon_color == self.COLORS['player_1']:

            # Change the color of the adjacent hexagons to green if they are not black and not already green
            adjacent_hexagons = self.get_adjacent_hexagons(hexagon_index)
            for adjacent_hexagon in adjacent_hexagons:
                self.canvas.itemconfig(self.hexagons[adjacent_hexagon], fill=self.COLORS['inner_adjacent'])
                self.hexagon_colors[adjacent_hexagon] = self.COLORS['inner_adjacent']
                if self.hexagon_colors[adjacent_hexagon] is not None and self.hexagon_colors[
                    adjacent_hexagon] != self.COLORS['out_of_map'] and self.hexagon_colors[adjacent_hexagon] != self.COLORS['player_1']:

                    # Change the color of the hexagons adjacent to the adjacent hexagon to yellow if they are not black and not already green or yellow
                    adjacent_adjacent_hexagons = self.get_adjacent_hexagons(adjacent_hexagon)
                    for adjacent_adjacent_hexagon in adjacent_adjacent_hexagons:
                        if self.hexagon_colors[adjacent_adjacent_hexagon] is not None and self.hexagon_colors[
                            adjacent_adjacent_hexagon] != self.COLORS['out_of_map'] and self.hexagon_colors[
                            adjacent_adjacent_hexagon] != self.COLORS['player_1'] and self.hexagon_colors[
                            adjacent_adjacent_hexagon] != self.COLORS['inner_adjacent'] and self.hexagon_colors[
                            adjacent_adjacent_hexagon] != self.COLORS['outer_adjacent']:
                            self.canvas.itemconfig(self.hexagons[adjacent_adjacent_hexagon], fill=self.COLORS['outer_adjacent'])
                            self.hexagon_colors[adjacent_adjacent_hexagon] = self.COLORS['outer_adjacent']

            self.canvas.itemconfig(self.hexagons[hexagon_index], fill=self.COLORS['player_1'])
            # Update the hexagon_colors list with the new color
            self.hexagon_colors[hexagon_index] = self.COLORS['player_1']

    def get_adjacent_hexagons(self, hexagon_index):
        adjacent_hexagons = []

        if hexagon_index // self.MAP_HEIGHT % 2 == 0:

            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 1)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 1)

            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 10)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 10)

            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 11)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 9)
        else:
            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 1)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 1)

            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 10)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 10)

            if hexagon_index - 1 >= 0:
                adjacent_hexagons.append(hexagon_index - 9)
            if hexagon_index + 1 < len(self.hexagons):
                adjacent_hexagons.append(hexagon_index + 11)
        return adjacent_hexagons


board = Board()
board.run()
