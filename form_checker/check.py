from pathlib import Path
import time
import imageio
import cv2
import mediapipe as mp


class Video:
    def __init__(self, file_path):

        if not (Path(file_path).is_file()):
            raise FileNotFoundError(f"Could not find associated video file {file_path}")

        self.vidcap = cv2.VideoCapture(file_path)
        self.width = int(self.vidcap.get(3))
        self.height = int(self.vidcap.get(4))
        self.fps = self.vidcap.get(cv2.CAP_PROP_FPS)

    def set_desired_frames(self):
        self.frame_step = 1
        return self

    def get_frame(self, frame):
        self.vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success, image = self.vidcap.read()
        return image if success else []

    def release(self):
        self.vidcap.release()

    def write(self, img):
        self.output.write(img)

    def __len__(self):
        return int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT))

    def __call__(self, filename):
        self.output_filename = filename
        return self

    def __enter__(self):
        print(f"Writing out file: {self.output_filename} - {self.width} x {self.height}")
        mp4_fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        self.output = cv2.VideoWriter(
            self.output_filename, fourcc=mp4_fourcc, fps=self.fps / 4, frameSize=(self.width, self.height)
        )
        return self

    def __exit__(self, *args, **kwargs):
        self.release()
        self.output.release()
        cv2.destroyAllWindows()


video_file_path = "tests/test2.mp4"


def run():
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    video = Video(video_file_path)

    pTime = 0
    images = []

    with video("output3.mp4") as output:
        for frame in range(len(video)):
            print(f"Writing frame {frame}/{len(video)}")
            img = video.get_frame(frame)
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            if results.pose_landmarks:
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape

                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                    cTime = time.time()
                    fps = 1 / (cTime - pTime)
                    pTime = cTime

                    cv2.putText(img, str(int(fps)), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)
            images.append(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            output.write(img)

    imageio.mimsave("video.gif", images, fps=video.fps / 3)
