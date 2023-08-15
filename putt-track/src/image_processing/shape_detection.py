import cv2
import numpy as np


class SurfaceDetector:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def detect_rectangle(self, frame):
        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Thresholding
        _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)

        # Find contours
        contours, _ = cv2.findContours(
            thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        # Iterate through contours and find rectangles
        for contour in contours:
            approx = cv2.approxPolyDP(
                contour, 0.04 * cv2.arcLength(contour, True), True
            )
            if len(approx) == 4:
                return approx

        return None

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Could not read frame.")
                break

            rectangle = self.detect_rectangle(frame)
            if rectangle is not None:
                cv2.drawContours(frame, [rectangle], -1, (0, 255, 0), 2)
            else:
                cv2.putText(
                    frame,
                    "Rectangle not found",
                    (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                )

            cv2.imshow("Rectangle Detection", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        cv2.destroyAllWindows()
