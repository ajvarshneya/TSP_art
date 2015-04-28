from tkinter import *
import random
import re
import math

class Graph:
    def __init__(self):
        self.graph = {}

    def get_adj_list(self, node):
        return self.graph.get(node, None)

    def get_nodes(self):
        return list(self.graph.keys())

    def add_node(self, node):
        if node in self.graph:
            return False
        else:
            self.graph[node] = []
            return True

    def link_nodes(self, u, v):
        if u not in self.graph or v not in self.graph or u == v:
            return False
        else:
            # Link nodes both ways
            self.graph[u].append(v)
            self.graph[v].append(u)
            return True

    def unlink_nodes(self, u, v):
        if u not in self.graph or v not in self.graph or u == v:
            return False
        else:
            self.graph[u].remove(v)
            self.graph[v].remove(u)
            return True

    def __str__(self):
        return str(self.graph)

def acquire_points():
    # filename i/o
    # filename = 'images/stippled/earth_5kstip.svg'
    filename = 'images/stippled/test.svg'
    f = open(filename, 'r')

    result = []

    # get points from .svg
    for line in f:
        if line.startswith('<circle'):
            # gets x and y coords as string
            x_s = re.search('cx="(.*)" cy="', line).group(1)
            y_s = re.search('cy="(.*)" r="', line).group(1)
            # converts x and y coords to floats, then ints
            point = (int(float(x_s)), int(float(y_s)))
            # adds point to list
            result.append(point)

    return result

def traverse_tree(cur_node, graph, path, visited):
    # Modified DFS traversal of the tree
    visited.append(cur_node)

    # Go through all edges
    for node in graph.get_adj_list(cur_node):
        if node not in visited:
            traverse_tree(node, graph, path, visited)

    # Add the current node (after processing all adj nodes)
    path.append(cur_node)

def make_graph_from_edges(mst_edges):
    g = Graph()
    for edge in mst_edges:
        g.add_node(edge[1])
        g.add_node(edge[2])
        g.link_nodes(edge[1], edge[2])
    return g

def draw_content(c, width, height):
    points = acquire_points()
    # random.shuffle(points)

    edge_list = generate_edge_list(points)

    mst_edges = find_MST_edges(edge_list, len(points))

    # Make a graph for the MST
    graph = make_graph_from_edges(mst_edges)

    # Traverse the tree to find an approximate path
    path = []
    start_node = graph.get_nodes()[0]
    # Add the start_node since the DFS traversal will put it at the end
    path.append(start_node)
    traverse_tree(start_node, graph, path, [])

    r = 1
    # for i in range(len(points)-1):
    #     x_c = points[i][0]-800
    #     y_c = points[i][1]
    #     c.create_oval(x_c-r, y_c-r, x_c+r, y_c+r, fill="#000000")

    # for i in range(len(mst_edges)):
    #     c.create_line(mst_edges[i][1][0]-800, mst_edges[i][1][1], mst_edges[i][2][0]-800, mst_edges[i][2][1])

    print(path)
    print(path[0][0])
    for i in range(len(path)-1):
        c.create_line(path[i][0]-800, path[i][1], path[i+1][0]-800, path[i+1][1])

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

def calc_distance(p1, p2):
    return math.sqrt(calc_square_distance(p1, p2))

def run_program():
    # Create the program frame
    frame = Tk()

    # Create the canvas
    canvas_width = 400
    canvas_height = 400
    c = Canvas(frame, width=canvas_width, height=canvas_height)
    c.pack()

    draw_content(c, canvas_width, canvas_height)

    # Display the frame
    frame.mainloop()

if __name__ == "__main__":
    run_program()