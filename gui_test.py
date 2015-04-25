from tkinter import *
from data_gen import get_point_list
import random

def draw_content(c, width, height):
    points = get_point_list()
    random.shuffle(points)

    edge_list = generate_edge_list(points)

    mst_edges = find_MST_edges(edge_list, len(points))

    r = 1
    for i in range(len(points)-1):
        x_c = points[i][0]-800
        y_c = points[i][1]
        c.create_oval(x_c-r, y_c-r, x_c+r, y_c+r, fill="#000000")

    for i in range(len(mst_edges)):
        c.create_line(mst_edges[i][1][0]-800, mst_edges[i][1][1], mst_edges[i][2][0]-800, mst_edges[i][2][1])

def generate_edge_list(point_list):
    edge_list = []
    # Generate the list of all possible edges
    for i in range(len(point_list)):
        # Avoid duplicates since edges are symmetric
        for j in range(i+1, len(point_list)):
            weight = calc_square_distance(point_list[i], point_list[j])
            edge = (weight, point_list[i], point_list[j])
            edge_list.append(edge)

    return edge_list

def find_MST_edges(edge_list, num_nodes):
    # Sort the list by the first value (distance)
    edge_list.sort(key=lambda x:x[0])

    mst_edges = []

    # Use dictionary for O(1) lookups
    visited = {}

    # Mark first node as read
    visited[edge_list[0][1]] = True

    # Continue until all nodes have been visited
    while len(visited) != num_nodes:
        # Iterate through all edges
        for i in range(len(edge_list)):
            u = edge_list[i][1]
            v = edge_list[i][2]

            if (u in visited and v not in visited) or (u not in visited and v in visited):
                visited[u] = True
                visited[v] = True
                mst_edges.append(edge_list[i])
                break

    return mst_edges

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