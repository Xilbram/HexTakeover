class jogada:
    def on_hexagon_clicked(self, hexagon):
        for i in range(len(self.hexagon_colors)):
            if self.hexagon_colors[i] == self.COLORS['inner_adjacent'] or self.hexagon_colors[i] == self.COLORS['outer_adjacent']:
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['unselected'])
                self.hexagon_colors[i] = self.COLORS['unselected']

        hexagon_index = self.hexagons.index(hexagon)
        hexagon_color = self.hexagon_colors[hexagon_index]

        if hexagon_color == self.COLORS['player_1']:

            inner_adjacent_hexagons = self.get_adjacent_hexagons(hexagon_index)

            for i in inner_adjacent_hexagons:

                if self.hexagon_colors[i] != self.COLORS['out_of_map']:

                    if self.hexagon_colors[i] != self.COLORS['player_1']:
                        self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['inner_adjacent'])
                        self.hexagon_colors[i] = self.COLORS['inner_adjacent']

                    outer_adjacent_hexagons = self.get_adjacent_hexagons(i)

                    valid_colors = [self.COLORS['out_of_map'],
                                    self.COLORS['player_1'],
                                    self.COLORS['inner_adjacent'],
                                    self.COLORS['outer_adjacent']]

                    for j in outer_adjacent_hexagons:
                        if self.hexagon_colors[j] not in valid_colors:
                            self.canvas.itemconfig(self.hexagons[j], fill=self.COLORS['outer_adjacent'])
                            self.hexagon_colors[j] = self.COLORS['outer_adjacent']

            if self.selected_hexagon is not None:
                self.canvas.itemconfig(self.hexagons[self.selected_hexagon], fill=self.COLORS['player_1'])
                self.hexagon_colors[self.selected_hexagon] = self.COLORS['player_1']

            self.canvas.itemconfig(self.hexagons[hexagon_index], fill=self.COLORS['player_1_selected'])
            self.hexagon_colors[hexagon_index] = self.COLORS['player_1_selected']

            self.selected_hexagon = hexagon_index

        elif hexagon_color == self.COLORS['player_1_selected']:
            if self.selected_hexagon is not None:
                self.canvas.itemconfig(self.hexagons[self.selected_hexagon], fill=self.COLORS['player_1'])
                self.hexagon_colors[self.selected_hexagon] = self.COLORS['player_1']

            self.canvas.itemconfig(self.hexagons[hexagon_index], fill=self.COLORS['player_1'])

            self.selected_hexagon = hexagon_index

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

        return adjacent_hexagons