import math
import tkinter as tk
from typing import Dict
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage

class Board:
    # constants
    HEX_SIDE_LENGTH = 50
    MAP_WIDTH = 20
    MAP_HEIGHT = 10
    

    def __init__(self):
        self.hexagons = []
        self.hexagon_colors = []
        self.selected_hexagon = None
        self.canvas = None
        self.message_label = None
        self.message = "Iniciando o Jogo"
        self.local_player_id = None
        self.remote_player_id = None
        self.current_player_id = 0
        self.game_running = False
        self.end_game = False
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
        self.create_interface()
        

    def create_interface(self):
        root = tk.Tk()
        root.title("Hex Takeover")
        # criando o menu
        menu_bar = tk.Menu(root)
        # variável de controle para mostrar ou ocultar os botões
        self.show_buttons = tk.BooleanVar()
        self.show_buttons.set(True)  # Definir como True para mostrar os botões inicialmente
        # Adicionar os botões ao menu e definir o estado com base na variável de controle
        menu_bar.add_cascade(label="Conectar ao servidor", command=self.send_connect, state='normal' if not self.game_running else 'disabled')
        menu_bar.add_cascade(label="Desconectar", command=self.send_disconnect, state='normal' if  not self.game_running else 'disabled')
        root.config(menu=menu_bar)
        self.frame_game = tk.Frame(root, width=1400, height=800)
        self.frame_game.pack()
        self.canvas = tk.Canvas(self.frame_game, width=1400, height=800)
        self.canvas.pack()
        self.hexagon_height = (self.HEX_SIDE_LENGTH * math.sqrt(3)) / 2

        # Criando widget Label para exibir mensagens
        self.message_label = tk.Label(root, text=self.message, font=("Arial", 30), bg='#303030', fg='white')
        self.message_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.init_positions()
        self.add_listener()	# Pyng use case "add listener"
        self.send_connect()	# Pyng use case "send connect"
        root.mainloop()
        

    def init_positions(self):
        for i in range(self.MAP_WIDTH):
            for j in range(self.MAP_HEIGHT):
                x = i * 1.5 * self.HEX_SIDE_LENGTH
                y = j * (self.hexagon_height * 2) + ((i % 2) * self.hexagon_height)
                outline_color = self.COLORS['outline']
                player_positions = {
                    (3, 3): self.COLORS['player_0'],
                    (3, 4): self.COLORS['player_0'],
                    (4, 3): self.COLORS['player_0'],
                    (4, 4): self.COLORS['player_0'],
                    (4, 5): self.COLORS['player_0'],
                    (5, 3): self.COLORS['player_0'],
                    (5, 4): self.COLORS['player_0'],
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
                    x - self.HEX_SIDE_LENGTH / 2, y + self.hexagon_height,
                    x + self.HEX_SIDE_LENGTH / 2, y + self.hexagon_height,
                    x + self.HEX_SIDE_LENGTH, y,
                    x + self.HEX_SIDE_LENGTH / 2, y - self.hexagon_height,
                    x - self.HEX_SIDE_LENGTH / 2, y - self.hexagon_height
                ]
                hexagon = self.canvas.create_polygon(vertices, fill=fill_color, outline=outline_color)
                self.hexagons.append(hexagon)
                self.hexagon_colors.append(fill_color)
                self.init_hexagons = self.hexagons
                self.init_hexagon_colors = self.hexagon_colors
                self.canvas.tag_bind(hexagon, '<Button-1>', lambda e, place=hexagon: self.on_hexagon_clicked(place))

    def on_hexagon_clicked(self, hexagon):
        if self.game_state==1:
            self.message_label.config(text="Aguarde o início da partida")
        elif self.game_state==2:
            cor = self.canvas.itemcget(hexagon, 'fill')
            if cor == self.COLORS[f'player_{self.local_player_id}'] or self.COLORS[f'player_{self.local_player_id}_selected']:
                self.select_hexagon(hexagon)
            if cor == self.COLORS['inner_adjacent'] or cor == self.COLORS['outer_adjacent']:
                if cor == self.COLORS['inner_adjacent'] :
                    self.clone(hexagon)
                elif cor == self.COLORS['outer_adjacent'] :
                    self.jump(hexagon)
                self.flip(hexagon)
                self.send_move()
        elif self.game_state==3:
            self.message_label.config(text="Aguarde a jogada do adversário")


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
                    if self.hexagon_colors[j]  == self.COLORS['unselected']:
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
        return adjacent_hexagons
    
    def clean_map(self):
        for i in range(len(self.hexagon_colors)):
            if self.hexagon_colors[i] == self.COLORS['inner_adjacent'] or self.hexagon_colors[i] == self.COLORS['outer_adjacent']:
                self.hexagon_colors[i] = self.COLORS['unselected']
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['unselected'])
                
            if self.hexagon_colors[i] == self.COLORS[f'player_{self.local_player_id}_selected']:
                self.hexagon_colors[i] = self.COLORS[f'player_{self.local_player_id}']
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS[f'player_{self.local_player_id}'])
                
            if self.hexagon_colors[i] == self.COLORS[f'player_{self.remote_player_id}_selected']:
                self.hexagon_colors[i] = self.COLORS[f'player_{self.remote_player_id}']

                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS[f'player_{self.remote_player_id}'])
                
    def select_hexagon(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        hexagon_color = self.hexagon_colors[hexagon_index]
        if hexagon_color == self.COLORS[f'player_{self.local_player_id}']:
            self.clean_map()
            possibles = self.get_possible(hexagon_index)
            for d in range (len(possibles[1])):
                
                self.hexagon_colors[possibles[1][d]] = self.COLORS['outer_adjacent']
                self.canvas.itemconfig(self.hexagons[possibles[1][d]], fill=self.COLORS['outer_adjacent'])
                
            for c in range (len(possibles[0])):
                self.hexagon_colors[possibles[0][c]] = self.COLORS['inner_adjacent']
                self.canvas.itemconfig(self.hexagons[possibles[0][c]], fill=self.COLORS['inner_adjacent'])
                
            self.hexagon_colors[hexagon_index] = self.COLORS[f'player_{self.local_player_id}_selected']
            self.canvas.itemconfig(self.hexagons[hexagon_index], fill=self.COLORS[f'player_{self.local_player_id}_selected'])
            
            self.selected_hexagon = hexagon_index
        elif hexagon_color == self.COLORS[f'player_{self.local_player_id}_selected']:
            self.selected_hexagon = None
            self.clean_map()

    def clone(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.hexagon_colors[hexagon_index] = self.COLORS[f'player_{self.local_player_id}']
        self.canvas.itemconfig(hexagon, fill=self.COLORS[f'player_{self.local_player_id}'])

    def jump(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.hexagon_colors[hexagon_index] = self.COLORS[f'player_{self.local_player_id}']
        self.canvas.itemconfig(hexagon, fill=self.COLORS[f'player_{self.local_player_id}'])
        self.hexagon_colors[self.selected_hexagon] = self.COLORS['unselected']
        self.canvas.itemconfig(self.hexagons[self.selected_hexagon], fill=self.COLORS['unselected'])

    def flip(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        inner_adjacent_hexagons = self.get_adjacent_hexagons(hexagon_index)
        for i in inner_adjacent_hexagons:
            if self.hexagon_colors[i] == self.COLORS[f'player_{self.remote_player_id}']:          
                self.hexagon_colors[i] = self.COLORS[f'player_{self.local_player_id}']
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS[f'player_{self.local_player_id}'])
                

    def check_game_over(self):
        self.clean_map()
        self.cont_j0 = 0
        self.cont_j1 = 0
        self.cont_jog_j0 = 0
        self.cont_jog_j1 = 0
        for k in range(20,170):
            possibles = self.get_possible(self.hexagons[k])
            if self.hexagon_colors[k] == self.COLORS['player_1']:
                self.cont_j0 +=1
                if self.cont_jog_j0 == 0:
                    self.cont_jog_j0=len(possibles[0])+len(possibles[1])
            if self.hexagon_colors[k] == self.COLORS['player_0']:
                self.cont_j1 +=1
                if self.cont_jog_j1 == 0:
                    self.cont_jog_j1=len(possibles[0])+len(possibles[1])
        if self.cont_j0+self.cont_j1==75:
            if self.cont_j0<self.cont_j1:
                message = f"Jogador Vermelho venceu com {self.cont_j1} pontos"
                self.message_label.config(text=message)
                self.end_game =True
            else:
                message = f"Jogador Azul venceu com {self.cont_j0} pontos"
                self.message_label.config(text=message)
                self.end_game =True
        if self.cont_j0 == 0 or self.cont_jog_j0==0:
            message = f"Jogador Vermelho venceu com {self.cont_j1} pontos"
            self.message_label.config(text=message)
            self.end_game =True
        elif self.cont_j1 == 0 or self.cont_jog_j1==0:
            message = f"Jogador Azul venceu com {self.cont_j0} pontos"
            self.message_label.config(text=message)
            self.end_game =True
        if self.end_game==True:
            self.game_state=4

    def toggle_player(self):
        if self.current_player_id == 0:
            self.current_player_id = 1
        else:
            self.current_player_id = 0
        if self.current_player_id == self.local_player_id:
            self.game_state = 2
        else:
            self.game_state = 3

#----------------------- Pynetgames ----------------------------------

    def add_listener(self):		# Pyng use case "add listener"
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connect(self):	# Pyng use case "send connect"
        if self.game_state == 1:
            self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def send_disconnect(self):	# Pyng use case "send connect"
        if self.game_state == 1:
            self.server_proxy.send_disconnect()


    def send_match(self):	# Pyng use case "send match"
        self.server_proxy.send_match(2)

    def receive_connection_success(self):	# Pyng use case "receive connection"
        self.message_label.config(text="Conectado")
        self.send_match()

    def receive_disconnect(self):	# Pyng use case "receive disconnect"
        self.message_label.config(text="desconectado")
        self.send_connect()
        pass
		
    def receive_error(self, error):	# Pyng use case "receive error"
        self.message_label.config(text="Erro no sistema")
        self.send_disconnect()
        pass

    def receive_match(self, match):	# Pyng use case "receive match"
        print('*************** PARTIDA INICIADA *******************')
        print('*************** ORDEM: ', match.position)
        print('*************** match_id: ', match.match_id)
        self.game_running = True
        self.local_player_id = match.position
        self.match_id = match.match_id
        if self.local_player_id==0:
            self.message_label.config(text="Você começa")
            self.remote_player_id=1
            self.game_state = 2
        else:
            self.message_label.config(text="O adversário começa")
            self.remote_player_id=0
            self.game_state = 3


    def receive_move(self, message):
        for i in range(len(self.hexagon_colors)):
            self.hexagon_colors[i] = message.payload['board'][i]
            self.canvas.itemconfig(self.hexagons[i], fill=message.payload['board'][i])
            
        self.check_game_over()
        if self.end_game == False:
            self.toggle_player()
            self.message_label.config(text="É a sua vez de jogar")

    def receive_move_sent_success(self):
        pass

    def receive_match_requested_success(self):
        pass

    def send_move(self):
        self.clean_map()
        self.check_game_over()
        if self.end_game: 
            self.server_proxy.send_move(self.match_id, {"board":self.hexagon_colors})
        else:
            self.message_label.config(text="enviando movimento")
            self.server_proxy.send_move(self.match_id, {"board":self.hexagon_colors})
            self.toggle_player()
            if self.game_state==3:
                self.message_label.config(text="Vez do adversário")
            


