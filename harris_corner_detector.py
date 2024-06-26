

# Import Libraries
import numpy as np
import matplotlib.pyplot as plt
import cv2
import torch
import os

# Define functions

def harris_corner_detection(image, window_size=3, k=0.04, threshold=0.1):
    # Convert image to grayscale
    if len(image.shape) == 3:
        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        image_gray = image.copy()

    # Compute gradients
    dx = cv2.Sobel(image_gray, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(image_gray, cv2.CV_64F, 0, 1, ksize=3)

    # Compute components of the Harris matrix
    Ixx = dx ** 2
    Ixy = dx * dy
    Iyy = dy ** 2

    # Compute sums of the Harris matrix components using a window
    Sxx = cv2.boxFilter(Ixx, -1, (window_size, window_size))
    Sxy = cv2.boxFilter(Ixy, -1, (window_size, window_size))
    Syy = cv2.boxFilter(Iyy, -1, (window_size, window_size))

    # Compute determinant and trace of the Harris matrix
    det = Sxx * Syy - Sxy ** 2
    trace = Sxx + Syy

    # Compute corner response function R
    R = det - k * (trace ** 2)

    # Apply thresholding to obtain corner points
    corners = np.zeros_like(R)
    corners[R > threshold * R.max()] = 255

    return corners.astype(np.uint8)

# Load Images

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

# Comparision

def compare_with_opencv(images_folder, window_size=3, k=0.04, threshold=0.1):
    images = load_images_from_folder(images_folder)

    for img in images:
        # Run Harris corner detection using custom implementation
        custom_corners = harris_corner_detection(img, window_size, k, threshold)

        # Run Harris corner detection using OpenCV
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        opencv_corners = cv2.cornerHarris(gray_img, window_size, 3, k)

        # Visualize results
        fig, axs = plt.subplots(1, 3, figsize=(15, 15))
        axs[1].imshow(custom_corners, cmap='cubehelix')
        axs[1].set_title('Custom Harris Corner Detection')
        axs[1].axis('off')

        axs[2].imshow(opencv_corners, cmap='flag')
        axs[2].set_title('OpenCV CornerHarris')
        axs[2].axis('off')

        axs[0].imshow(img, cmap='flag')
        axs[0].set_title('Orignal')
        axs[0].axis('off')

        plt.show()

# Define parameters
images_folder = '/content/DATA_1'
window_size = 3
k = 0.04
threshold = 0.1

# Compare custom implementation with OpenCV
compare_with_opencv(images_folder, window_size, k, threshold)
