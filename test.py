import tkinter as tk
from math import sqrt, cos, sin

cell_size = 50
canvas_width = cell_size * 9
canvas_height = cell_size * 9
root = tk.Tk()
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height)
canvas.pack()

for i in range(8):
    for j in range(8):
        x = cell_size * (i + 1) + (cell_size / 2) if j % 2 == 0 else cell_size * (i + 1)
        y = cell_size * (j + 1) * sqrt(3) / 2

        # Calculate the coordinates of the six vertices of the hexagon
        vertices = []
        for k in range(6):
            angle_deg = 60 * k
            angle_rad = angle_deg * 3.14159 / 180
            vertex_x = x + (cell_size / 2) * cos(angle_rad)
            vertex_y = y + (cell_size / 2) * sin(angle_rad)
            vertices.append(vertex_x)
            vertices.append(vertex_y)

        canvas.create_polygon(vertices, fill='white', outline='black', width=2)

root.mainloop()
