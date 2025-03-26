# CODE FOR REAL-TIME VIDEO BASED PATH FINDING

# import cv2
# import numpy as np
# import networkx as nx
# import time  # For frame rate control

# # Global graph to avoid recreation every frame
# G = nx.Graph()

# def preprocess_frame(frame):
#     """Fast denoising with improved clarity for low visibility."""
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
#     return denoised

# def detect_obstacles(frame):
#     """Adaptive threshold for efficient obstacle detection."""
#     obstacle_map = cv2.adaptiveThreshold(
#         frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#         cv2.THRESH_BINARY_INV, 11, 2
#     )
#     return obstacle_map

# def build_graph(obstacle_map):
#     """Builds the navigation graph only once."""
#     global G
#     height, width = obstacle_map.shape
#     G.clear()  # Clear old graph
#     for x in range(height):
#         for y in range(width):
#             if obstacle_map[x, y] == 0:
#                 G.add_node((x, y))

#     for x, y in G.nodes():
#         for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
#             nx_node = (x + dx, y + dy)
#             if nx_node in G:
#                 G.add_edge((x, y), nx_node)

# def find_safe_path(start, end):
#     """Compute the path dynamically if nodes are available."""
#     if start not in G or end not in G:
#         return []
#     try:
#         return nx.astar_path(G, start, end)
#     except nx.NetworkXNoPath:
#         return []

# def visualize_path(frame, path):
#     """Draw the computed path on the frame."""
#     for x, y in path:
#         cv2.circle(frame, (y, x), 2, (0, 255, 0), -1)
#     return frame

# # Start video capture
# # cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture('video.mp4')  # For video file
# build_graph_trigger = True  # Flag to control graph building

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     processed_frame = preprocess_frame(frame)
#     obstacles = detect_obstacles(processed_frame)

#     # Build graph only if obstacles change significantly
#     if build_graph_trigger:
#         build_graph(obstacles)
#         build_graph_trigger = False

#     start = (processed_frame.shape[0] // 2, 0)
#     end = (processed_frame.shape[0] // 2, processed_frame.shape[1] - 1)
#     path = find_safe_path(start, end)

#     frame_with_path = visualize_path(frame, path)
#     cv2.imshow('Safe Path', frame_with_path)

#     # Control frame rate and refresh logic
#     if cv2.waitKey(30) & 0xFF == ord('e'):  # WaitKey(30) limits FPS to ~30
#         break

# cap.release()
# cv2.destroyAllWindows()

#CODE FOR SIMULATION USING STATIC IMAGES

import cv2
import numpy as np
import networkx as nx

# Graph for pathfinding
G = nx.Graph()

def preprocess_frame(frame):
    """Fast denoising with improved clarity for low visibility."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    return denoised

def detect_obstacles(frame):
    """Adaptive threshold for efficient obstacle detection."""
    obstacle_map = cv2.adaptiveThreshold(
        frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
    return obstacle_map

def build_graph(obstacle_map):
    """Builds the navigation graph."""
    global G
    height, width = obstacle_map.shape
    G.clear()
    for x in range(height):
        for y in range(width):
            if obstacle_map[x, y] == 0:  # Add only open spaces
                G.add_node((x, y))

    for x, y in G.nodes():
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # 4-directional movement
            nx_node = (x + dx, y + dy)
            if nx_node in G:
                G.add_edge((x, y), nx_node)

def find_safe_path(start, end):
    """Compute the path dynamically if nodes are available."""
    if start not in G or end not in G:
        return []
    try:
        return nx.astar_path(G, start, end)
    except nx.NetworkXNoPath:
        return []

def visualize_path(frame, path):
    """Draw the computed path on the frame."""
    for x, y in path:
        cv2.circle(frame, (y, x), 2, (0, 255, 0), -1)
    return frame

# Load the smoke-filled room image
image_path = 'smoke img2.jpg'  # Replace with your image path
frame = cv2.imread(image_path)

if frame is None:
    print(f"Error: Unable to load image from {image_path}")
else:
    processed_frame = preprocess_frame(frame)
    obstacles = detect_obstacles(processed_frame)

    # Build the graph once
    build_graph(obstacles)

    start = (processed_frame.shape[0] // 2, 0)  # Mid-left start
    end = (processed_frame.shape[0] // 2, processed_frame.shape[1] - 1)  # Mid-right end

    path = find_safe_path(start, end)

    # Draw the path on the original image
    frame_with_path = visualize_path(frame, path)
    cv2.imshow('Safe Path (Image Simulation)', frame_with_path)

    # Keep window open until key press
    cv2.waitKey(0)
    cv2.destroyAllWindows()
