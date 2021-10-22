import mediapipe as mp
import cv2
import minecraft_controls as mc
import pose_detection as pd

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose_video = mp_pose.Pose(static_image_mode = False, min_detection_confidence = 0.5, model_complexity = 2)
video = cv2.VideoCapture(0)

while video.isOpened():
    ok, frame = video.read()
    if not ok:
        break
    k = cv2.waitKey(1)
    if(k == 27):
        break
    
    frame = cv2.flip(frame, 1)
    frame_height, frame_width, _ =  frame.shape
    frame = cv2.resize(frame, (int (frame_width * (640 / frame_height)), 640))
    frame, _ = pd.detectPose(frame, pose_video, display = False)
    frame, landmarks = pd.detectPose(frame, pose_video, display = False)
    cv2.imshow('Video Feed', frame)

    print(pd.classifyPose(landmarks))
    mc.minecraft(pd.classifyPose(landmarks))

video.release()
cv2.destroyAllWindows()