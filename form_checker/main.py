import logging
from cv2 import (
    cvtColor,
    circle,
    putText,
    COLOR_BGR2RGB,
    FONT_HERSHEY_SIMPLEX,
    FILLED,
)
from mediapipe import solutions
from form_checker.video import Video
from form_checker.settings import Config

mpDraw = solutions.drawing_utils
mpPose = solutions.pose
pose = mpPose.Pose()


def process(input_file):
    logging.info(f"Processing input file: {input_file}")
    video = Video(input_file)

    # TODO: Use multi-threading.
    with video:
        for frame in range(len(video)):
            img = video.get_frame(frame)
            if len(img):
                draw_pose(img, frame)
                video.write(img)

    return video.output_filename


def draw_pose(img, frame_number, circle_color=(255, 0, 0), circle_radius=5):
    imgRGB = cvtColor(img, COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        logging.info(f"Drawing pose over frame {frame_number} - {img.size}px")
        mpDraw.draw_landmarks(
            img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
        )
        if circle_radius:
            for i, lm in enumerate(results.pose_landmarks.landmark):
                h, w, _ = img.shape

                cx, cy = int(lm.x * w), int(lm.y * h)
                circle(img, (cx, cy), circle_radius, circle_color, FILLED)

                putText(
                    img,
                    str(frame_number),
                    (50, 50),
                    FONT_HERSHEY_SIMPLEX,
                    1,
                    circle_color,
                    3,
                )
    else:
        logging.warning(
            f"No pose data found for frame {frame_number} - {img.size}px"
        )
