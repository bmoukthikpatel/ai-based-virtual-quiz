#!/usr/bin/env python3
"""
Hand Detection Module
Handles MediaPipe hand tracking and gesture recognition for the AI-based quiz system.
"""

import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_drawing = mp.solutions.drawing_utils


def detect_hands(frame):
    """
    Detects hands in a frame without drawing.
    Returns the processed results.
    """
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    return results


def draw_hand_landmarks(frame, hand_landmarks):
    """
    Draws the landmarks for a single hand on a frame.
    """
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


def calculate_distance(point1, point2):
    """
    Calculate Euclidean distance between two points.
    """
    return np.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)


def get_finger_position(hand_landmarks, frame_shape):
    """
    Get the index finger tip position in pixel coordinates.
    """
    index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
    height, width, _ = frame_shape
    return int(index_finger_tip.x * width), int(index_finger_tip.y * height)


def check_finger_in_box(x, y, box):
    """
    Check if finger is in a specific box (for UI interactions).
    """
    x1, y1, x2, y2 = box
    return x1 <= x <= x2 and y1 <= y <= y2


def check_selected_option(x, y, option_boxes):
    """
    Check whether the finger position falls within any option bounding box.
    """
    if not option_boxes:
        return None
    for idx, box in enumerate(option_boxes):
        x1, y1, x2, y2 = box
        if x1 <= x <= x2 and y1 <= y <= y2:
            return chr(65 + idx)
    return None


def is_pinch_gesture(hand_landmarks, frame_shape, distance_window):
    """
    Detects if the user is making a pinch gesture for drawing.
    """
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

    height, width, _ = frame_shape
    thumb_tip_coords = (int(thumb_tip.x * width), int(thumb_tip.y * height))
    index_tip_coords = (int(index_tip.x * width), int(index_tip.y * height))

    distance = calculate_distance(thumb_tip_coords, index_tip_coords)
    distance_window.append(distance)
    avg_distance = np.mean(distance_window)
    threshold = 30

    return avg_distance < threshold