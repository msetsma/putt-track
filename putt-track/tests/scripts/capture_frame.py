import cv2
import os
from datetime import datetime

def main():
    # Create the 'img' directory inside the test folder if it doesn't exist
    output_path = "tests/img"
    os.makedirs(output_path, exist_ok=True)

    # Open the camera (camera index 0)
    cap = cv2.VideoCapture(0)

    # Check if the camera opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        exit()

    # Main loop to display the camera feed
    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Check if the frame was captured successfully
        if not ret:
            print("Error: Could not read frame.")
            break

        # Display the frame in a window
        cv2.imshow('Press "c" to Capture', frame)

        # Wait for a key press
        key = cv2.waitKey(1) & 0xFF

        # If the 'c' key is pressed, capture and save the image
        if key == ord('c'):
            # Generate a unique timestamp string
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Generate the output file path with the timestamp
            filename = os.path.join(output_path, f"captured_image_{timestamp}.png")
            
            # Save the image
            cv2.imwrite(filename, frame)
            print(f"Image captured and saved to {filename}")

        # If the 'q' key is pressed, exit the loop
        if key == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

