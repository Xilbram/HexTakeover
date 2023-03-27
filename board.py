import tkinter as tk
from tkinter import ttk

class Board():
    def __init__(self):

        self.cell_w = 50
        self.cell_h = 50

    def run1(self):
        root = tk.Tk()
        root.title="HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'

                if i == 1 and j == 6:
                    fill_color = 'red'

                if i == 2 and j == 7:
                    fill_color = 'red'

                if i == 3 and j == 6:
                    fill_color = 'red'

                if i == 5 and j == 1:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'


                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline='black')
        root.mainloop()

    def run2(self):
        root = tk.Tk()
        root.title = "HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'
                outline_w = 1
                outline_color = 'black'

                if i == 1 and j == 6:
                    fill_color = 'red'

                if i == 2 and j == 7:
                    fill_color = 'red'

                if i == 3 and j == 6:
                    fill_color = 'red'
                    outline_color = 'black'
                    outline_w = 5



                if i == 5 and j == 1:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'




                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=outline_w)


        canvas.itemconfigure((4*8)+6, fill='#8FED8F')
        canvas.itemconfigure((3*8)+6, fill='#8FED8F')
        canvas.itemconfigure((2*8)+6, fill='#8FED8F')
        canvas.itemconfigure((4*8)+7, fill='#8FED8F')
        canvas.itemconfigure((4*8)+8, fill='#8FED8F')
        canvas.itemconfigure((2*8)+7, fill='#8FED8F')
        canvas.itemconfigure((3*8)+8, fill='#8FED8F')

        canvas.itemconfigure((2*8)+5, fill='#FFC878')
        canvas.itemconfigure((3*8)+5, fill='#FFC878')
        canvas.itemconfigure((4*8)+5, fill='#FFC878')
        canvas.itemconfigure((1*8)+6, fill='#FFC878')
        canvas.itemconfigure((5*8)+6, fill='#FFC878')
        canvas.itemconfigure((5*8)+7, fill='#FFC878')
        canvas.itemconfigure((5*8)+8, fill='#FFC878')

        root.mainloop()


    def run3(self):
        root = tk.Tk()
        root.title = "HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'

                if i == 1 and j == 6:
                    fill_color = 'red'
                if i == 2 and j == 7:
                    fill_color = 'red'
                if i == 3 and j == 6:
                    fill_color = 'red'
                if i == 4 and j == 5:
                    fill_color = 'red'


                if i == 5 and j == 1:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'



                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline='black')
        root.mainloop()

    def run4(self):
        root = tk.Tk()
        root.title = "HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'

                if i == 1 and j == 6:
                    fill_color = 'red'
                if i == 2 and j == 7:
                    fill_color = 'red'
                if i == 3 and j == 6:
                    fill_color = 'white'
                if i == 4 and j == 4:
                    fill_color = 'red'


                if i == 5 and j == 1:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'



                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline='black')
        root.mainloop()

    def run5(self):
        root = tk.Tk()
        root.title = "HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'
                outline_w = 1
                outline_color = 'black'

                if i == 1 and j == 6:
                    fill_color = 'red'

                if i == 2 and j == 7:
                    fill_color = 'red'


                if i == 4 and j == 4:
                    fill_color = 'red'



                if i == 5 and j == 1:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'




                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline=outline_color, width=outline_w)


        canvas.itemconfigure((5*8)+1, fill='#8FED8F')
        canvas.itemconfigure((4*8)+2, fill='#8FED8F')
        canvas.itemconfigure((6*8)+2, fill='#8FED8F')
        canvas.itemconfigure((4*8)+3, fill='#8FED8F')
        canvas.itemconfigure((5*8)+3, fill='#8FED8F')
        canvas.itemconfigure((6*8)+3, fill='#8FED8F')

        canvas.itemconfigure((3*8)+1, fill='#FFC878')
        canvas.itemconfigure((3*8)+2, fill='#FFC878')
        canvas.itemconfigure((3*8)+3, fill='#FFC878')
        canvas.itemconfigure((4*8)+4, fill='#FFC878')
        canvas.itemconfigure((5*8)+4, fill='#FFC878')
        canvas.itemconfigure((6*8)+4, fill='#FFC878')
        canvas.itemconfigure((7 * 8) + 1, fill='#FFC878')
        canvas.itemconfigure((7 * 8) + 2, fill='#FFC878')
        canvas.itemconfigure((7 * 8) + 3, fill='#FFC878')

        root.mainloop()

    def run6(self):
        root = tk.Tk()
        root.title = "HexTakeover"
        # Create a canvas widget
        canvas = tk.Canvas(root, width=400, height=400)
        canvas.pack()
        # Define the size of each cell in the matrix
        cell_width = 50
        cell_height = 50

        for i in range(8):
            for j in range(8):
                x1 = i * cell_width
                y1 = j * cell_height
                x2 = x1 + cell_width
                y2 = y1 + cell_height
                fill_color = 'white'

                if i == 1 and j == 6:
                    fill_color = 'red'
                if i == 2 and j == 7:
                    fill_color = 'red'

                if i == 4 and j == 4:
                    fill_color = 'blue'


                if i == 4 and j == 3:
                    fill_color = 'blue'
                if i == 4 and j == 0:
                    fill_color = 'blue'
                if i == 6 and j == 0:
                    fill_color = 'blue'



                canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline='black')
        root.mainloop()

test = Board()
test.run1()
test.run2()
test.run3()
test.run4()
test.run5()
test.run6()