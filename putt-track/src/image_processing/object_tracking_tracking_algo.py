import cv2
import math

import cv2


class BallTracker:
    """Tracks a ball in a video using OpenCV's KCF tracker"""

    def __init__(self, video_path):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(self.video_path)
        self.tracker = None
        self.trail_points = []

    def detect_ball(self, frame):
        """Detects a ball in a frame and returns the bounding box"""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 230, 255, cv2.THRESH_BINARY)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)

        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        filtered_cnts = []
        for c in cnts:
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            area = cv2.contourArea(c)
            perimeter = cv2.arcLength(c, True)
            circularity = (
                4 * math.pi * area / (perimeter * perimeter) if perimeter > 0 else 0
            )
            if radius > 10 and circularity > 0.8:
                filtered_cnts.append(c)

        if filtered_cnts:
            c = max(filtered_cnts, key=cv2.contourArea)
            (x, y), radius = cv2.minEnclosingCircle(c)
            # Convert the circle to a bounding box
            bbox = (int(x - radius), int(y - radius), int(2 * radius), int(2 * radius))
            return bbox

        return None

    def initialize_tracker(self, frame):
        # Let the user select the object to track or automatically detect it
        bbox = self.detect_ball(frame)
        if not bbox:
            bbox = cv2.selectROI("Select Object to Track", frame, False)
        self.tracker.init(frame, bbox)

    def draw_tracer(self, frame, center):
        self.trail_points.append(center)
        max_thickness = 10  # You can adjust this value
        for i in range(1, len(self.trail_points)):
            # Scale the thickness based on the index, but keep it within 1 to max_thickness
            thickness = max(1, min(max_thickness, max_thickness - i))
            cv2.line(
                frame,
                self.trail_points[i - 1],
                self.trail_points[i],
                (0, 0, 255),
                thickness,
            )

    def run(self):
        success, frame = self.cap.read()
        if not success:
            print(f"Error reading video file at {self.video_path}")
            return

        # Initialize KCF tracker
        self.tracker = cv2.TrackerCSRT_create()
        self.initialize_tracker(frame)

        while True:
            success, frame = self.cap.read()
            if not success:
                print("End of video")
                break

            # Update tracker and get new position of the tracked object
            success, bbox = self.tracker.update(frame)
            if success:
                # Draw a bounding box around the tracked object
                x, y, w, h = map(int, bbox)
                radius = (w + h) // 4
                center = (x + w // 2, y + h // 2)
                cv2.circle(frame, (x + radius, y + radius), radius, (0, 255, 0), 2)
                self.draw_tracer(frame, center)
            # Display the frame
            cv2.imshow("Tracking", frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
