#!/usr/bin/env python3
"""
File Utilities Module
Handles file operations including loading quiz questions and saving user responses.
"""

import os
import shutil
import cv2
import numpy as np


def load_questions(file_path):
    """
    Load questions from a file.
    
    Expected format:
    - MCQ questions: keyword "mcq", question, 4 options (A-D), correct answer
    - Drawing questions: keyword "draw", question
    
    Args:
        file_path (str): Path to the quiz file
    
    Returns:
        list: List of question dictionaries
    """
    questions = []
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file.readlines() if line.strip()]
            i = 0
            while i < len(lines):
                keyword = lines[i].lower()
                if keyword == "mcq":
                    question = lines[i + 1]
                    options = [lines[i + 2], lines[i + 3], lines[i + 4], lines[i + 5]]
                    answer = lines[i + 6].upper()
                    questions.append({
                        "keyword": keyword, 
                        "question": question, 
                        "options": options, 
                        "answer": answer
                    })
                    i += 7
                elif keyword == "draw":
                    question = lines[i + 1]
                    questions.append({
                        "keyword": keyword, 
                        "question": question
                    })
                    i += 2
                else:
                    i += 1
    except Exception as e:
        print(f"Error loading questions: {e}")
    return questions


def setup_responses_directory():
    """
    Set up the responses directory, clearing any existing responses.
    
    Returns:
        str: Path to the responses directory
    """
    responses_dir = "responses"
    if os.path.exists(responses_dir):
        try:
            shutil.rmtree(responses_dir)
        except Exception as e:
            print(f"Failed to delete directory '{responses_dir}'. Reason: {e}")
    os.makedirs(responses_dir, exist_ok=True)
    return responses_dir


def save_drawing(drawing_points, responses_dir, question_number, frame_shape):
    """
    Save a drawing as a PNG image.
    
    Args:
        drawing_points (list): List of drawing point coordinates
        responses_dir (str): Directory to save the drawing
        question_number (int): Question number for filename
        frame_shape (tuple): Shape of the video frame
    
    Returns:
        str: Path to the saved drawing file
    """
    if drawing_points:
        canvas = np.zeros((frame_shape[0], frame_shape[1], 3), dtype=np.uint8)
        for i in range(1, len(drawing_points)):
            if drawing_points[i - 1] is not None and drawing_points[i] is not None:
                cv2.line(canvas, drawing_points[i - 1], drawing_points[i], (0, 0, 255), 2)
        image_path = os.path.join(responses_dir, f"drawing_{question_number + 1}.png")
        cv2.imwrite(image_path, canvas)
        return image_path
    return None


def log_responses(log_file, mcq_responses, draw_responses, score, total_mcq):
    """
    Log all responses to a text file.
    
    Args:
        log_file: File object to write to
        mcq_responses (list): List of MCQ responses
        draw_responses (list): List of drawing responses
        score (int): User's score
        total_mcq (int): Total number of MCQ questions
    """
    for response in mcq_responses:
        log_file.write(response + "\n")
    
    if len(mcq_responses) > 0:
        log_file.write(f"\nYour result is {score}/{total_mcq}\n\n")
    
    for response in draw_responses:
        log_file.write(response + "\n") 