import cv2

# Prepares a video frame for further processing by converting it to grayscale and reducing noise.

def preprocess_frame(frame):
    
    # Converts the input frame from a color image (BGR format) to a grayscale image.
    # Grayscale simplifies processing by reducing the number of channels.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Denoising algorithm to the grayscale image to remove noise.
    denoised = cv2.fastNlMeansDenoising(gray, None, 30, 7, 21)
    return denoised

#  Identifies obstacles in the preprocessed frame by applying adaptive thresholding

def detect_obstacles(frame):
    
    # Converts the input frame into a binary image (black and white) using adaptive thresholding.
    return cv2.adaptiveThreshold(
        frame, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV, 11, 2
    )
