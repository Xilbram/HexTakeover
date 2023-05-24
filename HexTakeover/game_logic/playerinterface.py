import tkinter as tk
from typing import Dict
from py_netgames_client.tkinter_client.PyNetgamesServerProxy import PyNetgamesServerProxy
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_client.tkinter_client.PyNetgamesServerListener import PyNetgamesServerListener
from py_netgames_model.messaging.message import MatchStartedMessage, MoveMessage
from .Tabuleiro import Tabuleiro
from .Hexagono import Hexagono
from .Jogador import Jogador


class PlayerInterface(PyNetgamesServerListener):
    # constants
    MAP_WIDTH = 20
    MAP_HEIGHT = 10

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hex Takeover")
        self.show_buttons = tk.BooleanVar()
        self.frame_game = tk.Frame(self.root, width=1400, height=800)
        self.message_label = None
        self.message = "Iniciando o Jogo"
        self.board = Tabuleiro()
        self.genHexagon = Hexagono()
        self.hexagons = []
        self.hexagon_colors = []
        self.debug = True
        self.selected_hexagon = None
        self.canvas = None
        self.local_player_id = None
        self.remote_player_id = None
        self.current_player_id = 0
        self.game_running = False
        self.end_game = False
        self.local_player = Jogador('#f55142', self.local_player_id, '#f54290')
        self.remote_player = Jogador('#4260f5', self.remote_player_id, '#4290f5')
        self.COLORS = {
            'inner_adjacent': '#55be4e',
            'outer_adjacent': '#cb7409',
            'outline': '#303030',
            'unselected': '#ffffff',
            'out_of_map': '#303030'
        }
        self.initialize()


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

    
    def get_cor_selecionadajogador_vez(self, swap=False):
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


    def initialize(self):
        # Criando widget Label para exibir mensagens
        self.message_label = tk.Label(self.root, text=self.message, font=("Arial", 30), bg='#303030', fg='white')
        self.message_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        self.init_positions()
        self.add_listener()  # Pyng use case "add listener"
        self.send_connect()  # Pyng use case "send connect"
        self.root.mainloop()

    def menu_bar(self, state):
        menu_bar = tk.Menu(self.root)
        # Adicionar os botões ao menu e definir o estado com base na variável de controle
        menu_bar.add_cascade(label="Conectar ao servidor", command=self.send_connect, state='normal' if state else 'disabled')
        menu_bar.add_cascade(label="Desconectar", command=self.send_disconnect, state='normal' if state else 'disabled')
        self.root.config(menu=menu_bar)
        self.frame_game.pack()

        self.canvas = tk.Canvas(self.frame_game, width=1400, height=800)
        self.canvas.pack()

    def init_positions(self):
        for i in range(self.MAP_WIDTH):
            for j in range(self.MAP_HEIGHT):
                x = i * 1.5 * self.genHexagon.getSideLenght()
                y = j * (self.genHexagon.getHexHeight() * 2) + ((i % 2) * self.genHexagon.getHexHeight())
                outline_color = self.COLORS['outline']
                player_positions = {
                    (3, 3): self.local_player.getColor(),
                    (3, 4): self.local_player.getColor(),
                    (4, 3): self.local_player.getColor(),
                    (4, 4): self.local_player.getColor(),
                    (4, 5): self.local_player.getColor(),
                    (5, 3): self.local_player.getColor(),
                    (5, 4): self.local_player.getColor(),
                    (13, 3): self.remote_player.getColor(),
                    (13, 4): self.remote_player.getColor(),
                    (14, 3): self.remote_player.getColor(),
                    (14, 4): self.remote_player.getColor(),
                    (14, 5): self.remote_player.getColor(),
                    (15, 3): self.remote_player.getColor(),
                    (15, 4): self.remote_player.getColor()
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
                    x - self.genHexagon.getSideLenght(), y,
                    x - self.genHexagon.getSideLenght() / 2, y + self.genHexagon.getHexHeight(),
                    x + self.genHexagon.getSideLenght() / 2, y + self.genHexagon.getHexHeight(),
                    x + self.genHexagon.getSideLenght(), y,
                    x + self.genHexagon.getSideLenght() / 2, y - self.genHexagon.getHexHeight(),
                    x - self.genHexagon.getSideLenght() / 2, y - self.genHexagon.getHexHeight()
                ]
                hexagon = self.canvas.create_polygon(vertices, fill=fill_color, outline=outline_color)
                self.hexagons.append(hexagon)
                self.board.hexagons.append(hexagon)
                self.hexagon_colors.append(fill_color)
                self.board.hexagon_colors.append(fill_color)
                self.canvas.tag_bind(hexagon, '<Button-1>', lambda e, place=hexagon: self.on_hexagon_clicked(place))

    def on_hexagon_clicked(self, hexagon):
        if self.board.get_game_state() == 1:
            self.message_label.config(text="Aguarde o início da partida")

        elif self.board.get_game_state() == 2:
            cor = self.canvas.itemcget(hexagon, 'fill')
            if cor == self.get_cor_jogador_vez() or self.get_cor_selecionada_jogador_vez():
                self.select_hexagon(hexagon)
            if cor == self.COLORS['inner_adjacent'] or cor == self.COLORS['outer_adjacent']:
                if cor == self.COLORS['inner_adjacent']:
                    self.clone(hexagon)
                elif cor == self.COLORS['outer_adjacent']:
                    self.jump(hexagon)
                self.flip(hexagon)
                self.send_move()

                if self.debug:
                    print(self.hexagon_colors)
                    self.clean_map()
                    print("--------------------")
                    print(self.hexagon_colors)
        elif self.board.get_game_state() == 3:
            self.message_label.config(text="Aguarde a jogada do adversário")

    def clean_map(self):
        for i in range(len(self.hexagon_colors)):
            if self.hexagon_colors[i] == self.COLORS['inner_adjacent'] or self.hexagon_colors[i] == self.COLORS['outer_adjacent']:
                self.hexagon_colors[i] = self.COLORS['unselected']
                self.board.hexagon_colors[i] = self.COLORS['unselected']
                self.canvas.itemconfig(self.hexagons[i], fill=self.COLORS['unselected'])

            if self.hexagon_colors[i] == self.get_cor_selecionada_jogador_vez():
                self.hexagon_colors[i] = self.get_cor_jogador_vez()
                self.board.hexagon_colors[i] = self.get_cor_jogador_vez()
                self.canvas.itemconfig(self.hexagons[i], fill=self.get_cor_jogador_vez())

            if self.hexagon_colors[i] == self.get_cor_selecionada_jogador_vez(True):
                self.hexagon_colors[i] = self.get_cor_jogador_vez(True)
                self.board.hexagon_colors[i] = self.get_cor_jogador_vez(True)
                self.canvas.itemconfig(self.hexagons[i], fill=self.get_cor_jogador_vez(True))

    def select_hexagon(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        hexagon_color = self.hexagon_colors[hexagon_index]
        if hexagon_color == self.get_cor_jogador_vez():
            self.clean_map()
            possibles = self.board.get_possible(hexagon_index)
            for d in range(len(possibles[1])):
                self.hexagon_colors[possibles[1][d]] = self.COLORS['outer_adjacent']
                self.board.hexagon_colors[possibles[1][d]] = self.COLORS['outer_adjacent']
                self.canvas.itemconfig(self.hexagons[possibles[1][d]], fill=self.COLORS['outer_adjacent'])

            for c in range(len(possibles[0])):
                self.hexagon_colors[possibles[0][c]] = self.COLORS['inner_adjacent']
                self.board.hexagon_colors[possibles[0][c]] = self.COLORS['inner_adjacent']
                self.canvas.itemconfig(self.hexagons[possibles[0][c]], fill=self.COLORS['inner_adjacent'])

            self.hexagon_colors[hexagon_index] = self.get_cor_selecionada_jogador_vez()
            self.board.hexagon_colors[hexagon_index] = self.get_cor_selecionada_jogador_vez()

            self.canvas.itemconfig(self.hexagons[hexagon_index], fill=self.get_cor_selecionada_jogador_vez())

            self.selected_hexagon = hexagon_index
        elif hexagon_color == self.get_cor_selecionada_jogador_vez():
            self.selected_hexagon = None
            self.clean_map()

    def clone(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.hexagon_colors[hexagon_index] = self.get_cor_jogador_vez()
        self.board.hexagon_colors[hexagon_index] = self.get_cor_jogador_vez()
        self.canvas.itemconfig(hexagon, fill=self.get_cor_jogador_vez())

    def jump(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        self.hexagon_colors[hexagon_index] = self.get_cor_jogador_vez()
        self.board.hexagon_colors[hexagon_index] = self.get_cor_jogador_vez()

        self.canvas.itemconfig(hexagon, fill=self.get_cor_jogador_vez())
        self.hexagon_colors[self.selected_hexagon] = self.COLORS['unselected']
        self.board.hexagon_colors[self.selected_hexagon] = self.COLORS['unselected']

        self.canvas.itemconfig(self.hexagons[self.selected_hexagon], fill=self.COLORS['unselected'])

    def flip(self, hexagon):
        hexagon_index = self.hexagons.index(hexagon)
        inner_adjacent_hexagons = self.board.get_adjacent_hexagons(hexagon_index)
        for i in inner_adjacent_hexagons:
            if self.hexagon_colors[i] == self.get_cor_jogador_vez(True):
                self.hexagon_colors[i] = self.get_cor_jogador_vez()
                self.board.hexagon_colors[i] = self.get_cor_jogador_vez()
                self.canvas.itemconfig(self.hexagons[i], fill=self.get_cor_jogador_vez())


    def avaliar_encerramento(self):
        self.clean_map()
        # resultado é uma tupla str int
        resultado = self.board.check_game_over(self.remote_player.getColor(), self.local_player.getColor())
        if resultado != None:
            message = "Jogador {} venceu com {} pontos".format(resultado[0], resultado[1])
            self.message_label.config(text=message)
            self.end_game = True
            self.board.set_game_state(4)


    def toggle_player(self):
        if self.current_player_id == 0:
            self.current_player_id = 1
        else:
            self.current_player_id = 0
        if self.current_player_id == self.local_player_id:
            self.board.set_game_state(2)
        else:
            self.board.set_game_state(3)

    # ----------------------- Pynetgames ----------------------------------

    def add_listener(self):  # Pyng use case "add listener"
        self.server_proxy = PyNetgamesServerProxy()
        self.server_proxy.add_listener(self)

    def send_connect(self):  # Pyng use case "send connect"
        self.server_proxy.send_connect("wss://py-netgames-server.fly.dev")

    def send_disconnect(self):  # Pyng use case "send connect"
        self.server_proxy.send_disconnect()

    def send_match(self):  # Pyng use case "send match"
        self.server_proxy.send_match(2)

    def receive_connection_success(self):  # Pyng use case "receive connection"
        self.message_label.config(text="Conectado")
        self.send_match()

    def receive_disconnect(self):  # Pyng use case "receive disconnect"
        self.message_label.config(text="desconectado")

    def receive_error(self, error):  # Pyng use case "receive error"
        self.message_label.config(text="Erro no sistema")

    def receive_match(self, match):  # Pyng use case "receive match"
        print('*************** PARTIDA INICIADA *******************')
        print('*************** ORDEM: ', match.position)
        print('*************** match_id: ', match.match_id)
        self.game_running = True
        self.menu_bar(False)
        self.local_player_id = match.position
        self.match_id = match.match_id
        if self.local_player_id == 0:
            self.message_label.config(text="Você começa")
            self.remote_player_id = 1
            self.board.set_game_state(2)
        else:
            self.message_label.config(text="O adversário começa")
            self.remote_player_id = 0
            self.board.set_game_state(3)

    def receive_move(self, message):
        for i in range(len(self.hexagon_colors)):
            self.hexagon_colors[i] = message.payload['board'][i]
            self.board.hexagon_colors[i] = message.payload['board'][i]

            self.canvas.itemconfig(self.hexagons[i], fill=message.payload['board'][i])

        self.avaliar_encerramento()
        if self.end_game == False:
            self.toggle_player()
            self.message_label.config(text="É a sua vez de jogar")

    def receive_move_sent_success(self):
        pass

    def receive_match_requested_success(self):
        pass

    def send_move(self):
        self.clean_map()
        self.avaliar_encerramento()
        if self.end_game:
            self.server_proxy.send_move(self.match_id, {"board": self.hexagon_colors})
        else:
            self.message_label.config(text="enviando movimento")
            self.server_proxy.send_move(self.match_id, {"board": self.hexagon_colors})
            self.toggle_player()
            if self.board.get_game_state() == 3:
                self.message_label.config(text="Vez do adversário")


