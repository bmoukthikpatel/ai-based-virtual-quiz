#!/usr/bin/env python3
"""
Quiz Engine Module
Core quiz logic and game loop for the AI-based quiz system.
"""

import cv2
import time
import os
from collections import deque
import numpy as np
import mediapipe as mp

from hand_detection import (
    detect_hands,
    draw_hand_landmarks,
    get_finger_position,
    check_finger_in_box,
    check_selected_option,
    is_pinch_gesture
)
from ui_components import (
    display_question,
    display_timer,
    create_finish_button,
    draw_drawing_points,
    display_result
)
from file_utils import (
    load_questions,
    setup_responses_directory,
    save_drawing,
    log_responses
)


class QuizEngine:
    """Main quiz engine class that handles the quiz flow and logic."""

    def __init__(self, quiz_file="quiz.txt"):
        self.quiz_file = quiz_file
        self.questions = load_questions(quiz_file)
        self.responses_dir = setup_responses_directory()
        self.total_questions = len(self.questions)
        self.score = 0
        self.current_question = 0
        self.mcq_responses = []
        self.draw_responses = []
        self.quiz_finished_by_button = False

        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise RuntimeError("Could not open camera")

    def run(self):
        """Run the main quiz loop."""
        if not self.questions:
            print("No questions found or error reading quiz.txt")
            return

        while self.current_question < self.total_questions:
            self._run_question_loop()
            if self.quiz_finished_by_button:
                break
            self.current_question += 1

        # --- Corrected Logic Block ---
        # If the quiz was finished early, log the remaining UNSEEN questions as not attempted.
        # It checks if we finished before the last question.
        if self.quiz_finished_by_button and self.current_question < self.total_questions - 1:
            # The loop now correctly starts from the NEXT question's index.
            for i in range(self.current_question + 1, self.total_questions):
                question_data = self.questions[i]
                if question_data["keyword"] == "mcq":
                    correct_option = question_data["answer"]
                    response_text = f"Not Attempted(correct option is {correct_option})"
                    self.mcq_responses.append(f"Question {i + 1}: {response_text}")
                else: # 'draw' question
                    self.draw_responses.append(f"Question {i + 1}: Not Attempted")


        self._display_final_results()
        self.cap.release()
        cv2.destroyAllWindows()

    def _run_question_loop(self):
        """Runs the loop for a single question with corrected logic."""
        start_time = time.time()
        option_selected = None
        confirmation_start_time = None
        finish_confirmation_start_time = None
        drawing_points = []
        smoothing_window = deque(maxlen=10)
        distance_window = deque(maxlen=5)
        frame_shape = None

        while time.time() - start_time < 15:
            ret, frame = self.cap.read()
            if not ret: break

            flipped_frame = cv2.flip(frame, 1)
            if frame_shape is None: frame_shape = flipped_frame.shape
            
            hand_results = detect_hands(flipped_frame)
            
            is_hovering_finish = False
            if hand_results and hand_results.multi_hand_landmarks:
                # Temporarily create the box to check for hover state
                temp_finish_box = create_finish_button(flipped_frame.copy(), is_hovering=False)
                index_tip_coords = get_finger_position(hand_results.multi_hand_landmarks[0], frame_shape)
                if check_finger_in_box(index_tip_coords[0], index_tip_coords[1], temp_finish_box):
                    is_hovering_finish = True

            question_data = self.questions[self.current_question]
            time_left = int(15 - (time.time() - start_time))
            option_boxes = display_question(
                flipped_frame, question_data, time_left,
                self.current_question + 1, self.total_questions, option_selected
            )
            finish_button_box = create_finish_button(flipped_frame, is_hovering=is_hovering_finish)

            if hand_results and hand_results.multi_hand_landmarks:
                hand_landmarks = hand_results.multi_hand_landmarks[0]
                draw_hand_landmarks(flipped_frame, hand_landmarks)
                index_tip_coords = get_finger_position(hand_landmarks, frame_shape)

                if check_finger_in_box(index_tip_coords[0], index_tip_coords[1], finish_button_box):
                    if finish_confirmation_start_time is None: finish_confirmation_start_time = time.time()
                    elif time.time() - finish_confirmation_start_time >= 1.5:
                        self.quiz_finished_by_button = True; break
                else:
                    finish_confirmation_start_time = None

                if question_data["keyword"] == "mcq":
                    selection = check_selected_option(index_tip_coords[0], index_tip_coords[1], option_boxes)
                    if selection:
                        if option_selected == selection:
                            if confirmation_start_time and time.time() - confirmation_start_time >= 1.5:
                                if selection == question_data["answer"]: self.score += 1
                                break
                        else:
                            option_selected = selection
                            confirmation_start_time = time.time()
                    else:
                        option_selected = None
                        confirmation_start_time = None
                
                elif question_data["keyword"] == "draw":
                    if is_pinch_gesture(hand_landmarks, frame_shape, distance_window):
                        smoothing_window.append(index_tip_coords)
                        if len(smoothing_window) == smoothing_window.maxlen:
                            smoothed_point = tuple(np.mean(smoothing_window, axis=0).astype(int))
                            drawing_points.append(smoothed_point)
                    else:
                        smoothing_window.clear()
                        if drawing_points and drawing_points[-1] is not None: drawing_points.append(None)
            
            draw_drawing_points(flipped_frame, drawing_points)
            display_timer(flipped_frame, time_left)
            cv2.imshow("AI-Based Quiz", flipped_frame)
            
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.quiz_finished_by_button = True; break

        self._log_current_question_response(drawing_points, option_selected, frame_shape)

    def _log_current_question_response(self, drawing_points, option_selected, frame_shape):
        if frame_shape is None: frame_shape = (480, 640, 3)
            
        question_data = self.questions[self.current_question]
        if question_data["keyword"] == "mcq":
            correct_option = question_data["answer"]
            if option_selected:
                response_text = f"{option_selected} (correct option is {correct_option})"
            else:
                response_text = f"Not Attempted(correct option is {correct_option})"
            self.mcq_responses.append(f"Question {self.current_question + 1}: {response_text}")
        else:
            if drawing_points and any(p is not None for p in drawing_points):
                image_path = save_drawing(drawing_points, self.responses_dir, self.current_question, frame_shape)
                self.draw_responses.append(f"Question {self.current_question + 1}: {image_path}")
            else:
                self.draw_responses.append(f"Question {self.current_question + 1}: Not Attempted")

    def _display_final_results(self):
        with open(os.path.join(self.responses_dir, "responses.txt"), "w") as log_file:
            total_mcqs = len([q for q in self.questions if q['keyword'] == 'mcq'])
            log_responses(log_file, self.mcq_responses, self.draw_responses, self.score, total_mcqs)
            
            result_text = ""
            if not self.mcq_responses and not self.draw_responses:
                result_text = "No responses recorded."
            elif total_mcqs > 0:
                result_text = f"Your result is {self.score}/{len(self.mcq_responses)}"
            else:
                result_text = "Quiz Finished! Responses saved."

            display_result(result_text)