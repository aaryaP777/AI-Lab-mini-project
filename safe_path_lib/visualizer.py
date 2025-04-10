import cv2
import numpy as np

def visualize_path_perspective(frame, path):
    height, width = frame.shape[:2]
    vanishing_point = (width // 2, 0)

    overlay = frame.copy()
    for x, y in path:
        dist = np.sqrt((y - vanishing_point[0])**2 + (x - vanishing_point[1])**2)
        thickness = max(1, int(10 - dist / 50))
        color_intensity = max(100, 255 - int(dist / 2))
        color = (0, color_intensity, color_intensity)
        cv2.circle(overlay, (y, x), thickness, color, -1)

    gradient = np.zeros_like(frame, dtype=np.uint8)
    for i in range(height):
        alpha = max(0, 1 - i / height)
        cv2.line(gradient, (0, i), (width, i), (255, 255, 255), 1)
        gradient[i] = (gradient[i] * alpha).astype(np.uint8)

    blended = cv2.addWeighted(overlay, 0.8, gradient, 0.2, 0)
    cv2.circle(blended, vanishing_point, 10, (255, 255, 255), -1)
    return blended
