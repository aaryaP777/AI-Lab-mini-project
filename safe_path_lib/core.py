import networkx as nx

G = nx.Graph()

def build_graph(obstacle_map):
    global G
    height, width = obstacle_map.shape
    G.clear()
    for x in range(height):
        for y in range(width):
            if obstacle_map[x, y] == 0:
                G.add_node((x, y))

    for x, y in G.nodes():
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (x + dx, y + dy)
            if neighbor in G:
                G.add_edge((x, y), neighbor)

def find_safe_path(start, end):
    if start not in G or end not in G:
        return []
    try:
        return nx.astar_path(G, start, end)
    except nx.NetworkXNoPath:
        return []
