from tkinter import *
from data_gen import get_point_list
import random

def draw_content(c, width, height):
    r = 1
    points = get_point_list()
    #random.shuffle(points)

    edge_list = generate_edge_list(points)

    mst = find_MST(edge_list, len(points))

    for i in range(len(points)-1):
        x_c = points[i][0]-800
        y_c = points[i][1]
        c.create_oval(x_c-r, y_c-r, x_c+r, y_c+r, fill="#000000")
        #c.create_line(x_c, y_c, points[i+1][0]-800, points[i+1][1])

    print(mst[0])
    print(mst[0][1][0])

    for i in range(len(mst)):
        c.create_line(mst[i][1][0]-800, mst[i][1][1], mst[i][2][0]-800, mst[i][2][1])

def generate_edge_list(point_list):
    edge_list = []
    # Generate the list of all possible edges
    print("Generating edge list...", len(point_list))
    for i in range(len(point_list)):
        # Avoid duplicates since edges are symmetric
        for j in range(i+1, len(point_list)):
            weight = calc_square_distance(point_list[i], point_list[j])
            edge = (weight, point_list[i], point_list[j])
            edge_list.append(edge)
    print("Edge list complete", len(edge_list))

    return edge_list

def find_MST(edge_list, num_nodes):
    # Sort the list by the first value (distance)
    edge_list.sort(key=lambda x:x[0])

    # Use dictionary to have O(1) lookups on average
    visited = {}
    MST_edges = []
    for i in range(len(edge_list)):
        if edge_list[i][1] not in visited or edge_list[i][2] not in visited:
            MST_edges.append(edge_list[i])
            visited[edge_list[i][1]] = True
            visited[edge_list[i][2]] = True

    print(len(MST_edges))

    return MST_edges

def calc_square_distance(p1, p2):
    dx = p1[0]-p2[0]
    dy = p1[1]-p2[1]

    return dx*dx + dy*dy

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