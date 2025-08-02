#!/usr/bin/env python3
"""
UI Components Module
Handles all user interface elements, text rendering, and visual feedback for the quiz system.
"""

import cv2
import numpy as np


def add_colored_text_background(frame, text, position, font, font_scale, font_thickness, bg_color, alpha=0.6):
    """
    Draw text with a colored background and return bounding box coordinates.
    """
    (text_width, text_height), _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    x, y = position
    overlay = frame.copy()
    cv2.rectangle(overlay, (x - 10, y - text_height - 10), (x + text_width + 10, y + 10), bg_color, -1)
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)
    cv2.putText(frame, text, (x, y), font, font_scale, (255, 255, 255), font_thickness)
    return (x - 10, y - text_height - 10, x + text_width + 10, y + 10)


def display_question(frame, question_data, time_left, question_number, total_questions, selected_option=None):
    """
    Display the current question and its options (if it's an MCQ).
    """
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    font_thickness = 2
    colors = [(173, 216, 230), (144, 238, 144), (255, 182, 193), (255, 182, 249)]
    highlight_color = (173, 216, 230)

    add_colored_text_background(frame, f"Question {question_number}/{total_questions}",
                               (20, 40), font, font_scale, font_thickness, colors[3])

    add_colored_text_background(frame, question_data["question"],
                               (20, 80), font, font_scale, font_thickness, colors[3])

    if question_data["keyword"] == "mcq":
        option_boxes = []
        for idx, option in enumerate(question_data["options"]):
            option_bg_color = highlight_color if selected_option == chr(65 + idx) else colors[1]
            box = add_colored_text_background(frame, f" {option}",
                                            (20, 130 + idx * 50), font, font_scale,
                                            font_thickness, option_bg_color)
            option_boxes.append(box)
        return option_boxes
    return None


def display_timer(frame, time_left):
    """
    Display the countdown timer.
    """
    add_colored_text_background(frame, f"Time Left: {time_left} sec",
                               (20, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2, (255, 182, 193))


def create_finish_button(frame, is_hovering=False):
    """
    Create and display the finish button with a dynamic hover color.
    """
    frame_height, frame_width, _ = frame.shape
    default_color = (152, 251, 152)  # Pale Green
    highlight_color = (173, 216, 230) # Light Blue (same as MCQ hover)

    button_color = highlight_color if is_hovering else default_color

    finish_button_box = add_colored_text_background(
        frame, "Finish", (frame_width // 2 - 70, frame_height - 60),
        cv2.FONT_HERSHEY_SIMPLEX, 0.9, 2, button_color
    )
    return finish_button_box


def draw_drawing_points(frame, drawing_points):
    """
    Draw the user's drawing on the frame.
    """
    for i in range(1, len(drawing_points)):
        if drawing_points[i - 1] is not None and drawing_points[i] is not None:
            cv2.line(frame, drawing_points[i - 1], drawing_points[i], (0, 0, 255), 2)


def display_result(result_text):
    """
    Display the final result screen.
    """
    result_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    add_colored_text_background(result_frame, result_text,
                               (100, 240), cv2.FONT_HERSHEY_SIMPLEX, 1, 2, (255, 182, 193))
    cv2.imshow("Result", result_frame)
    cv2.waitKey(3000)