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
from form_checker.utils.video import Video

mpDraw = solutions.drawing_utils
mpPose = solutions.pose
pose = mpPose.Pose()


def ui():
    import tkinter
    from tkinter.filedialog import askopenfilename

    root = tkinter.Tk()
    root.wm_withdraw()
    filename = askopenfilename()
    run(filename, True)


def run(input_file):
    logging.info(f"Processing input file: {input_file}")
    video = Video(input_file)
    logging.info(f"Wrapped video in internal Video class.")
    output_name = video.p.name.replace(
        video.p.suffix, f"_processed{video.p.suffix}"
    )

    with video(output_name) as output:
        for frame in range(len(video)):
            logging.info(f"Writing frame {frame}/{len(video)}")
            img = video.get_frame(frame)
            overlay_pose_on_frame(img, frame)
            output.write(img)
        output_name = output.compressed_filename

    return output_name


def overlay_pose_on_frame(
    img, frame_number, circle_color=(255, 0, 0), circle_radius=5
):
    imgRGB = cvtColor(img, COLOR_BGR2RGB)
    results = pose.process(imgRGB)

    if results.pose_landmarks:
        mpDraw.draw_landmarks(
            img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
        )
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape

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
