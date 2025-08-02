#!/usr/bin/env python3
"""
AI-Based Quiz System - Main Entry Point
A hand gesture-controlled quiz application using computer vision and MediaPipe.

Author: [Your Name]
Date: [Current Date]
"""

from quiz_engine import QuizEngine


def main():
    """
    Main function to run the AI-based quiz system.
    """
    try:
        print("Starting AI-Based Quiz System...")
        print("Make sure your webcam is connected and accessible.")
        print("Press 'q' to quit the application.")
        print("-" * 50)
        
        # Initialize and run the quiz engine
        quiz = QuizEngine("quiz.txt")
        quiz.run()
        
    except RuntimeError as e:
        print(f"Camera Error: {e}")
        print("Please check if your webcam is connected and not being used by another application.")
    except FileNotFoundError:
        print("Error: quiz.txt file not found!")
        print("Please make sure the quiz file exists in the same directory.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        print("Please check your setup and try again.")


if __name__ == "__main__":
    main() 