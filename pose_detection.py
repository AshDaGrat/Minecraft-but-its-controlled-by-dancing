import cv2
import numpy as np
import mediapipe as mp
import matplotlib.pyplot as plt

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def calculateAngle(p, q, r):
    pq = np.array(p) - np.array(q)
    rq = np.array(r) - np.array(q)
    cosine_angle = np.dot(pq, rq) / (np.linalg.norm(pq) * np.linalg.norm(rq))
    angle = np.arccos(cosine_angle)
    return np.degrees(angle)

def detectPose(image, pose, display = True):
    output_image = image.copy()
    results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    height, width, _ = image.shape
    landmarks = []

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image = output_image, landmark_list = results.pose_landmarks, connections = mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x * width), int(landmark.y * height), (landmark.z * width)))

    if display:
        plt.figure(figsize = [22,22])
        mp_drawing.plot_landmarks(results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

    else:
        return output_image, landmarks

def classifyPose(landmarks):
    left_elbow_angle     = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value]) 
    right_elbow_angle    = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])   
    left_shoulder_angle  = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])
    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                          landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value])     

    label = 'Neutral'
    if left_shoulder_angle > 75 and left_shoulder_angle < 110 and right_shoulder_angle > 75 and right_shoulder_angle < 110:
        label = "T pose" 
    elif left_shoulder_angle > 120 and left_shoulder_angle < 160 and right_shoulder_angle > 120 and right_shoulder_angle < 160 and right_elbow_angle > 110 and right_elbow_angle < 150:
        label = "Heart"
    elif left_shoulder_angle > 100 and left_shoulder_angle < 140 and right_shoulder_angle > 100 and right_shoulder_angle < 140 and right_elbow_angle > 150 and right_elbow_angle < 180:
        label = "Dab"
    elif left_shoulder_angle > 140 and left_shoulder_angle < 180 and right_shoulder_angle > 15 and right_shoulder_angle < 50:
        label = "Right_hand_up"
    elif right_shoulder_angle > 140 and right_shoulder_angle < 180 and left_shoulder_angle > 15 and left_shoulder_angle < 50:
        label = "Left_hand_up"
    elif left_shoulder_angle > 75 and left_shoulder_angle < 110:
        label = "Right_hand_side"  
    elif right_shoulder_angle > 75 and right_shoulder_angle < 110: 
        label = "Left_hand_side"
        
    return label