import pyautogui
import pyscreenshot as ImageGrab
import time
import imageio
import numpy as np
import cv2

# Set the region to capture (coordinates of the top-left and bottom-right corners)
top_left = (100, 100)
bottom_right = (500, 500)

# Set the duration (in seconds) for capturing the screen
duration = 5

# Create a list to store captured frames
frames = []

# Calculate the number of frames based on the desired duration
num_frames = duration * 10  # Assuming 30 frames per second

# Capture each frame and add it to the frames list
for _ in range(num_frames):
    # Capture the screen region
    screenshot = ImageGrab.grab(bbox=(
        top_left[0], top_left[1], bottom_right[0], bottom_right[1]))

    # Capture the mouse cursor position
    cursor_position = pyautogui.position()
    cursor_x, cursor_y = cursor_position[0] - top_left[0], cursor_position[1] - top_left[1]

    # Convert the screenshot to a numpy array
    frame = np.array(screenshot)

    # Draw a rectangle indicating the capture region
    cv2.rectangle(frame, top_left, bottom_right, (0, 0, 255), 2)
    # Draw the mouse cursor on the screenshot
    cv2.circle(frame, (cursor_x, cursor_y), 10, (255, 0, 0), -1)

    # Append the frame to the frames list
    frames.append(frame)

    # Pause for a short time before capturing the next frame
    time.sleep(0.033)  # Adjust this value to control the frame rate

# Save the frames as an animated GIF with a duration of 0.033 seconds per frame
imageio.mimsave('captured_screen.gif', frames, 'GIF', duration=0.025, loop=0)
