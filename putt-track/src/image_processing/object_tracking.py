import numpy as np
import argparse
import cv2
import imutils
import time
import os
import math

from imutils.video import VideoStream
from collections import defaultdict


# List of colors in BGR format
COLORS = [
    (0, 0, 255),  # Red
    (0, 255, 0),  # Green
    (255, 0, 0),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
]


class ObjectTracker:
    def __init__(self, video_path):
        self.video_path = video_path
        self.validate_path()

    def validate_path(self):
        if os.path.exists(self.video_path):
            self.cap = cv2.VideoCapture(self.video_path)
        else:
            print(f"File not found at {self.video_path}")
            exit()

    def process_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        THRESHOLD_VALUE = 230
        _, mask = cv2.threshold(gray, THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)

        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(
            mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )[-2]

        # Iterate through all contours and process each one
        for idx, c in enumerate(cnts):
            color = COLORS[
                idx % len(COLORS)
            ]  # Cycle through colors if more objects than colors
            ((x, y), radius) = cv2.minEnclosingCircle(c)

            # Calculate circularity
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            circularity = (
                4 * math.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            )

            # Set a circularity threshold (e.g., 0.8) to filter non-round objects
            if radius > 10 and circularity > 0.8:
                cv2.circle(frame, (int(x), int(y)), int(radius), color, 2)

        return frame, mask

    def run(self):
        while self.cap.isOpened():
            success, frame = self.cap.read()
            if success:
                frame, mask = self.process_frame(frame)
                cv2.imshow("Frame", frame)
                cv2.imshow("Mask", mask)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
            else:
                print(f"Error reading video file at {self.video_path}")
                break

        self.cap.release()
        cv2.destroyAllWindows()
