from image_processing.object_tracking import ObjectTracker


def main():
    video_path = "./data/videos/ball_roll_matt.mp4"
    tracker = ObjectTracker(video_path)
    tracker.run()


if __name__ == "__main__":
    main()
