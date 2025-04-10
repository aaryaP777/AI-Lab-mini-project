import sys
import os
import logging
logging.basicConfig(level=logging.INFO)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cv2
import numpy as np
from safe_path_lib import (
    preprocess_frame,
    detect_obstacles,
    build_graph,
    find_safe_path,
    visualize_path_perspective,
)

GRAPH_UPDATE_INTERVAL = 5
frame_counter = 0
prev_obstacle = None

cap = cv2.VideoCapture(r'test inputs\video1.mp4')

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    processed_frame = preprocess_frame(frame)
    obstacles = detect_obstacles(processed_frame)

    frame_counter += 1
    if frame_counter % GRAPH_UPDATE_INTERVAL == 0 or not np.array_equal(obstacles, prev_obstacle):
        build_graph(obstacles)
        prev_obstacle = obstacles.copy()

    start = (processed_frame.shape[0] // 2, 0)
    end = (processed_frame.shape[0] // 2, processed_frame.shape[1] - 1)
    path = find_safe_path(start, end)

    frame_with_path = visualize_path_perspective(frame, path)
    cv2.imshow('Safe Path', frame_with_path)

    if cv2.waitKey(30) & 0xFF == ord('e'):
        break

cap.release()
cv2.destroyAllWindows()
