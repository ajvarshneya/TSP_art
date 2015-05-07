from tkinter import *
import re
import math
import sys

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
    # check for filename in args, or get it as input
    filename = None
    for arg in sys.argv:
        if arg.endswith('.svg'):
            filename = arg
    if filename == None:
        filename = input("Please enter the filename: ")
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

    # ==================================================
    #   MST implementation
    # ==================================================
    print("Finding edges...")
    edge_list = generate_edge_list(points)

    print("Finding mst...")
    mst_edges = find_MST_edges(edge_list, len(points))

    # Make a graph for the MST
    print("Generating graph...")
    graph = make_graph_from_edges(mst_edges)
    # Traverse the tree to find an approximate path
    path = []
    start_node = graph.get_nodes()[0]
    # Add the start_node since the DFS traversal will put it at the end
    # path.append(start_node)
    print("Finding path...")
    traverse_tree(start_node, graph, path, [])

    # Draw the initial lines
    if '-d' in sys.argv:
        num_path_points = len(path)
        for i in range(len(path)):
            c.create_line(path[i][0]-800, path[i][1], path[(i+1)%num_path_points][0]-800, path[(i+1)%num_path_points][1])
        c.update()

    print("Running 2-opt...")
    path = two_opt(path, c)

    print("Done.")

    c.delete(ALL)
    num_path_points = len(path)
    for i in range(len(path)):
        c.create_line(path[i][0]-800, path[i][1], path[(i+1)%num_path_points][0]-800, path[(i+1)%num_path_points][1])
    c.update()
    # ==================================================
    #   Nearest Neighbors implementation
    # ==================================================
    # print("Points acquired. Finding NN path...")
    # path = get_nearest_neighbors_path(points)
    #
    # print("Path found. Running 2-opt...")
    # start = time.time()
    # path = two_opt(path)
    # end = time.time()
    # print(end-start)
    #
    # print("Finished 2-opt.")
    # num_path_points = len(path)
    # for i in range(len(path)):
    #     c.create_line(path[i][0]-800, path[i][1], path[(i+1)%num_path_points][0]-800, path[(i+1)%num_path_points][1])

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

def two_opt(path, c):
    draw_flag = '-d' in sys.argv

    color = "#33ccbb"
    for arg in sys.argv:
        if arg.startswith('#') and len(arg) == 7:
            color = arg

    num_path_points = len(path)
    for n in range(20):
        for i in range(num_path_points):
            a1 = path[i]
            a2 = path[(i+1)%num_path_points]
            for j in range(i+1, num_path_points):
                b1 = path[j]
                b2 = path[(j+1)%num_path_points]
                if calc_distance(a1, b1) + calc_distance(a2, b2) < calc_distance(a1, a2) + calc_distance(b1, b2):
                    # Reverse the middle values to change the path
                    mid_range = int((j-i)/2)
                    for k in range(mid_range):
                        temp = path[i+1+k]
                        path[i+1+k] = path[j-k]
                        path[j-k] = temp

                    if draw_flag:
                        c.create_line(a1[0]-800, a1[1], b1[0]-800, b1[1], fill=color)
                        c.create_line(a2[0]-800, a2[1], b2[0]-800, b2[1], fill=color)
                        c.update()

        # Redraw the path
        if draw_flag:
            c.delete(ALL)
            num_path_points = len(path)
            for i in range(len(path)):
                c.create_line(path[i][0]-800, path[i][1], path[(i+1)%num_path_points][0]-800, path[(i+1)%num_path_points][1])
            c.update()
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

    frame.after(0, draw_content(c, canvas_width, canvas_height))

    # Display the frame
    frame.mainloop()

if __name__ == "__main__":
    run_program()