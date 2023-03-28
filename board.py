import math
import tkinter as tk


class Board():
    def __init__(self):
        self.hex_size = 50
        self.hexagons = []
        self.hexagon_colors = []
        self.canvas = None
        self.selected_hexagon = None

    def run(self):
        root = tk.Tk()
        root.title("HexTakeover")
        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.pack()

        for i in range(20):
            for j in range(10):
                x = i * 1.5 * self.hex_size
                y = j * math.sqrt(3) * self.hex_size + ((i % 2) * math.sqrt(3) / 2 * self.hex_size)
                fill_color = 'white'
                outline_color = 'black'

                if i == 5 and j == 5:
                    fill_color = 'red'
                elif i == 10 and j == 5:
                    fill_color = 'blue'

                elif i == 11 and j == 3:
                    fill_color = 'blue'
                elif i == 7 and j == 3:
                    fill_color = 'blue'
                elif i == 4 and j == 3:
                    fill_color = 'blue'
                else:
                    fill_color = 'white'

                if i==1 or i ==0 or i==17 or i ==18 or j==0 or j ==9 or j== 8 or j==7 :
                    fill_color = None
                    outline_color = None

                coords = [
                    x - self.hex_size, y,
                    x - self.hex_size / 2, y + math.sqrt(3) / 2 * self.hex_size,
                    x + self.hex_size / 2, y + math.sqrt(3) / 2 * self.hex_size,
                    x + self.hex_size, y,
                    x + self.hex_size / 2, y - math.sqrt(3) / 2 * self.hex_size,
                    x - self.hex_size / 2, y - math.sqrt(3) / 2 * self.hex_size
                ]

                hexagon = self.canvas.create_polygon(coords, fill=fill_color, outline=outline_color)
                self.hexagons.append(hexagon)
                self.hexagon_colors.append(fill_color)

                self.canvas.tag_bind(hexagon, '<Button-1>', lambda event, hexagon=hexagon: self.on_hexagon_clicked(event, hexagon))

        root.mainloop()

    def on_hexagon_clicked(self, event, hexagon):
        # Change the color of all green and yellow hexagons to white
        for i in range(len(self.hexagon_colors)):
            if self.hexagon_colors[i] == 'green' or self.hexagon_colors[i] == 'yellow':
                self.canvas.itemconfig(self.hexagons[i], fill='white')
                self.hexagon_colors[i] = 'white'

        hexagon_index = self.hexagons.index(hexagon)

        hexagon_color = self.hexagon_colors[hexagon_index]

        # Change the color of the clicked hexagon to green if it's not already green
        if hexagon_color == 'blue':


            

            # Change the color of the adjacent hexagons to green if they are not black and not already green
            adjacent_hexagons = self.get_adjacent_hexagons(hexagon_index)
            for adjacent_hexagon in adjacent_hexagons:
                self.canvas.itemconfig(self.hexagons[adjacent_hexagon], fill='green')
                self.hexagon_colors[adjacent_hexagon] = 'green'
                if self.hexagon_colors[adjacent_hexagon] is not None and self.hexagon_colors[adjacent_hexagon] != 'black' and self.hexagon_colors[adjacent_hexagon] != 'blue' :

                    # Change the color of the hexagons adjacent to the adjacent hexagon to yellow if they are not black and not already green or yellow
                    adjacent_adjacent_hexagons = self.get_adjacent_hexagons(adjacent_hexagon)
                    for adjacent_adjacent_hexagon in adjacent_adjacent_hexagons:
                        if self.hexagon_colors[adjacent_adjacent_hexagon] is not None and self.hexagon_colors[adjacent_adjacent_hexagon] != 'black' and self.hexagon_colors[adjacent_adjacent_hexagon] != 'blue'  and self.hexagon_colors[adjacent_adjacent_hexagon] != 'green' and self.hexagon_colors[adjacent_adjacent_hexagon] != 'yellow':
                            self.canvas.itemconfig(self.hexagons[adjacent_adjacent_hexagon], fill='yellow')
                            self.hexagon_colors[adjacent_adjacent_hexagon] = 'yellow'

            
            self.canvas.itemconfig(self.hexagons[hexagon_index], fill='blue')
            # Update the hexagon_colors list with the new color
            self.hexagon_colors[hexagon_index] = 'blue'



    def get_adjacent_hexagons(self, hexagon_index):
        adjacent_hexagons = []

        if hexagon_index // 10 %2== 0:
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
