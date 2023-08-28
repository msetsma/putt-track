from image_processing.object_tracking import ObjectTracker
from image_processing.object_tracking_tracking_algo import BallTracker


def main():
    video_path = "./data/videos/ball_roll_matt.mp4"
    # tracker = ObjectTracker(video_path)
    tracker = BallTracker(video_path)
    tracker.run()


if __name__ == "__main__":
    main()
