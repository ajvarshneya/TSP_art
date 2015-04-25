from tkinter import *
from data_gen import get_point_list
import random

def draw_content(c, width, height):
    r = 1
    points = get_point_list()
    #random.shuffle(points)
    for i in range(len(points)-1):
        x_c = points[i][0]-800
        y_c = points[i][1]
        c.create_oval(x_c-r, y_c-r, x_c+r, y_c+r, fill="#000000")
        #c.create_line(x_c, y_c, points[i+1][0]-800, points[i+1][1])

def run_program():
    # Create the program frame
    frame = Tk()

    # Create the canvas
    canvas_width = 1600
    canvas_height = 800
    c = Canvas(frame, width=canvas_width, height=canvas_height)
    c.pack()

    draw_content(c, canvas_width, canvas_height)

    # Display the frame
    frame.mainloop()


if __name__ == "__main__":
    run_program()