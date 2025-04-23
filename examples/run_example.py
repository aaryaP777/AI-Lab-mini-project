
import sys
import os
import logging
import time
import csv
import cv2
import numpy as np

logging.basicConfig(level=logging.INFO)

# include the library
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from safe_path_lib import (
    preprocess_frame,
    detect_obstacles,
    build_graph,
    find_safe_path,
    visualize_path_perspective,
)

# Initialize
GRAPH_UPDATE_INTERVAL = 5
frame_counter = 0
prev_obstacle = None

# Metrics
frame_times = []
obstacle_densities = []
graph_times = []
path_lengths = []

# Load video
cap = cv2.VideoCapture(r'test inputs\video1.mp4')  # path 

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_start = time.time()  # Start frame timer

    processed_frame = preprocess_frame(frame)
    obstacles = detect_obstacles(processed_frame)

    # Obstacle density (%)
    obstacle_density = np.count_nonzero(obstacles) / obstacles.size * 100
    obstacle_densities.append(obstacle_density)

    # Build graph periodically or if obstacle map changes
    if frame_counter % GRAPH_UPDATE_INTERVAL == 0 or not np.array_equal(obstacles, prev_obstacle):
        graph_start = time.time()
        build_graph(obstacles)
        graph_time = (time.time() - graph_start) * 1000  # in ms
        graph_times.append(graph_time)
        prev_obstacle = obstacles.copy()
    else:
        graph_times.append(0)

    # Pathfinding
    start_point = (processed_frame.shape[0] // 2, 0)
    end_point = (processed_frame.shape[0] // 2, processed_frame.shape[1] - 1)
    path = find_safe_path(start_point, end_point)
    path_lengths.append(len(path) if path else 0)

    # Visualize
    frame_with_path = visualize_path_perspective(frame, path)
    cv2.imshow('Safe Path', frame_with_path)

    frame_end = time.time()
    frame_time = (frame_end - frame_start) * 1000  # in ms
    frame_times.append(frame_time)

    frame_counter += 1
    if cv2.waitKey(30) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()

# Save metrics to CSV
with open('library_metrics.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Frame', 'Frame Time (ms)', 'Obstacle Density (%)', 'Graph Time (ms)', 'Path Length'])
    for i in range(len(frame_times)):
        writer.writerow([
            i + 1,
            frame_times[i],
            obstacle_densities[i],
            graph_times[i],
            path_lengths[i]
        ])

print("Metrics saved to library_metrics.csv")