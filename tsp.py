from tkinter import *
import random
import re
import math
import sys
import time

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
    filename = 'images/stippled/earth_1k_stip.svg'
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
    print("Acquiring points...")
    points = acquire_points()
    # random.shuffle(points)

    print("Points acquired. Finding NN path...")
    path = get_nearest_neighbors_path(points)

    print("Path found. Running 2-opt...")
    start = time.time()
    path = two_opt(path)
    end = time.time()
    print(end-start)

    print("Finished 2-opt.")
    num_path_points = len(path)
    for i in range(len(path)):
        c.create_line(path[i][0]-800, path[i][1], path[(i+1)%num_path_points][0]-800, path[(i+1)%num_path_points][1])

    """
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
    """

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

def get_nearest_neighbors_path(point_list):
    path = []
    cur_point = point_list[0]
    path.append(cur_point)
    # Loop until every point has been added to the path
    while len(path) != len(point_list):
        best_point = None
        min_dist = sys.maxsize
        for j in range(len(point_list)):
            # Check if the node is unvisited and nearest neighbor
            dist = calc_square_distance(cur_point, point_list[j])
            if  dist < min_dist and point_list[j] not in path:
                min_dist = dist
                best_point = point_list[j]

        # Add the new node to the path and repeat
        path.append(best_point)
        cur_point = best_point

    #path.append(cur_point)
    return path

def two_opt(path):
    num_path_points = len(path)
    # for n in range(num_path_points):
    for n in range(20):                     # Use a smaller value of n for testing optimizations
        for i in range(num_path_points):
            a1 = path[i]
            a2 = path[(i+1)%num_path_points]
            for j in range(i+1, num_path_points):
                b1 = path[j]
                b2 = path[(j+1)%num_path_points]
                if calc_distance(a1, b1) + calc_distance(a2, b2) < calc_distance(a1, a2) + calc_distance(b1, b2):
                    new_path = []
                    # Copy beginning of path
                    for idx in range(i+1):      # idx < i+1
                        new_path.append(path[idx])

                    # Reverse middle of path
                    for t in range((j-i)):    # i+1 <= idx <= j
                        idx = j-t
                        new_path.append(path[idx])        # Append in reverse order

                    # Copy end of path
                    for idx in range(j+1, num_path_points):
                        new_path.append(path[idx])

                    # Set the current path to the new path
                    # print("Swapping", i, j)
                    path = new_path
    return path

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
    canvas_width = 1400
    canvas_height = 800
    c = Canvas(frame, width=canvas_width, height=canvas_height)
    c.pack()

    draw_content(c, canvas_width, canvas_height)

    # Display the frame
    frame.mainloop()

if __name__ == "__main__":
    run_program()