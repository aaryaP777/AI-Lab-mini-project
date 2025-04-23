import networkx as nx  # Import the NetworkX library for graph creation and pathfinding

# Initialize an empty undirected graph
G = nx.Graph()

def build_graph(obstacle_map):
    """
    Constructs a graph representation of the environment based on the obstacle map.
    Nodes represent open spaces, and edges connect adjacent nodes.
    """
    global G  # Use the global graph variable
    height, width = obstacle_map.shape  # Get the dimensions of the obstacle map
    G.clear()  # Clear any existing nodes and edges in the graph

    # Add nodes for all open spaces (cells with value 0) in the obstacle map
    for x in range(height):
        for y in range(width):
            if obstacle_map[x, y] == 0:  # Check if the cell is not an obstacle
                G.add_node((x, y))  # Add the cell as a node in the graph

    # Add edges between adjacent nodes (up, down, left, right)
    for x, y in G.nodes():  # Iterate through all nodes in the graph
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Neighboring directions
            neighbor = (x + dx, y + dy)  # Calculate the neighbor's coordinates
            if neighbor in G:  # Check if the neighbor is a valid node
                G.add_edge((x, y), neighbor)  # Add an edge between the current node and the neighbor

def find_safe_path(start, end):
    """
    Finds the shortest path between the start and end nodes using the A* algorithm.
    Returns an empty list if no path exists.
    """
    if start not in G or end not in G:  # Check if both start and end nodes exist in the graph
        return []  # Return an empty list if either node is missing
    try:
        # Use the A* algorithm to find the shortest path
        return nx.astar_path(G, start, end)
    except nx.NetworkXNoPath:
        # Handle the case where no path exists between the nodes
        return []