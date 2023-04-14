import math
import tkinter as tk

from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener

class Board:

    # constants
    HEX_SIDE_LENGTH = 50
    MAP_WIDTH = 20
    MAP_HEIGHT = 10
    COLORS = {
        'player_1': '#4260f5',
        'player_1_selected': '#4290f5',
        'player_2': '#f55142',
        'player_2_selected': '#4260f5',
        'inner_adjacent': '#55be4e',
        'outer_adjacent': '#cb7409',
        'outline': '#303030',
        'unselected': '#ffffff',
        'out_of_map': '#303030'
    }

    def __init__(self):
        self.hexagons = []
        self.hexagon_colors = []
        self.selected_hexagon = None
        self.canvas = None
        self.run()
        

    def run(self):
        
        root = tk.Tk()
        root.title("Hex Takeover")

        # criando o menu
        menu_bar = tk.Menu(root)
        connect_menu = tk.Menu(menu_bar, tearoff=0)
        connect_menu.add_command(label="Conectar ao servidor")
        connect_menu.add_command(label="Desconectar do servidor")
        menu_bar.add_cascade(label="Conectar", menu=connect_menu)

        game_menu = tk.Menu(menu_bar, tearoff=0)
        game_menu.add_command(label="Iniciar jogo")
        game_menu.add_command(label="Abandonar partida")
        menu_bar.add_cascade(label="Jogo", menu=game_menu)

        root.config(menu=menu_bar)

        self.canvas = tk.Canvas(root, width=1400, height=800)
        self.canvas.pack()

        hexagon_height = (self.HEX_SIDE_LENGTH * math.sqrt(3)) / 2

        for i in range(self.MAP_WIDTH):
            for j in range(self.MAP_HEIGHT):
                x = i * 1.5 * self.HEX_SIDE_LENGTH
                y = j * (hexagon_height * 2) + ((i % 2) * hexagon_height)
                outline_color = self.COLORS['outline']

                player_positions = {
                    (3, 3): self.COLORS['player_2'],
                    (3, 4): self.COLORS['player_2'],
                    (4, 3): self.COLORS['player_2'],
                    (4, 4): self.COLORS['player_2'],
                    (4, 5): self.COLORS['player_2'],
                    (5, 3): self.COLORS['player_2'],
                    (5, 4): self.COLORS['player_2'],
                    (13, 3): self.COLORS['player_1'],
                    (13, 4): self.COLORS['player_1'],
                    (14, 3): self.COLORS['player_1'],
                    (14, 4): self.COLORS['player_1'],
                    (14, 5): self.COLORS['player_1'],
                    (15, 3): self.COLORS['player_1'],
                    (15, 4): self.COLORS['player_1']
                }

                if (i, j) in player_positions:
                    fill_color = player_positions[(i, j)]
                else:
                    fill_color = self.COLORS['unselected']

                # defining map borders
                if i < 2 or i > 16 or j < 2 or j > 6:
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

                self.canvas.tag_bind(hexagon, '<Button-1>', lambda e, place=hexagon: self.on_hexagon_clicked(place))

        self.add_listener()	# Pyng use case "add listener"
        self.send_connect()	# Pyng use case "send connect"
        root.mainloop()


    def on_hexagon_clicked(self, hexagon):

        cor = self.canvas.itemcget(hexagon, 'fill')
        if cor == self.COLORS['player_1'] or self.COLORS['player_1_selected'] or self.COLORS['player_2'] or self.COLORS['player_2_selected'] :
            self.select_hexagon(hexagon)
        if cor == self.COLORS['inner_adjacent'] :
            self.clone(hexagon)
        if cor == self.COLORS['outer_adjacent'] :
            self.jump(hexagon)
            

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
    
    def select_hexagon(self, hexagon):
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
    
                    if self.hexagon_colors[i] != self.COLORS['player_1'] and self.hexagon_colors[i] != self.COLORS['player_2']:
                        self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['inner_adjacent'])
                        self.hexagon_colors[i] = self.COLORS['inner_adjacent']

                    outer_adjacent_hexagons = self.get_adjacent_hexagons(i)
                    valid_colors = [self.COLORS['out_of_map'],
                                    self.COLORS['player_1'],
                                    self.COLORS['player_2'],
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


    def clone(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.canvas.itemconfig(hexagon, fill=self.COLORS['player_1'])
        self.hexagon_colors[hexagon_index] = self.COLORS['player_1']

    def jump(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.canvas.itemconfig(hexagon, fill=self.COLORS['player_1'])
        self.hexagon_colors[hexagon_index] = self.COLORS['player_1']
        for k in range(len(self.hexagon_colors)):
            if self.hexagon_colors[k] == self.COLORS['player_1_selected']:
                self.canvas.itemconfig(self.hexagons[k], fill=self.COLORS['unselected'])
                self.hexagon_colors[k] = self.COLORS['unselected']

#----------------------- Pynetgames ----------------------------------

    def add_listener(self):		# Pyng use case "add listener"
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connect(self):	# Pyng use case "send connect"
        self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def send_match(self):	# Pyng use case "send match"
        self.server_proxy.send_match(2)

    def receive_connection_success(self):	# Pyng use case "receive connection"
        print('*************** CONECTADO *******************')
        self.send_match()

    def receive_disconnect(self):	# Pyng use case "receive disconnect"
        pass
		
    def receive_error(self, error):	# Pyng use case "receive error"
        pass

    def receive_match(self, match):	# Pyng use case "receive match"
        print('*************** PARTIDA INICIADA *******************')
        print('*************** ORDEM: ', match.position)
        print('*************** match_id: ', match.match_id)

    def receive_move(self, move):	# Pyng use case "receive move"
        pass

    def receive_match_requested_success(self):
        pass