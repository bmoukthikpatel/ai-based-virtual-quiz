# Project Description: AI-Based Virtual Quiz System with Gesture Control

## 1. High-Level Objective
Build a desktop application in Python that allows a user to take an interactive quiz using hand gestures as the primary input method. The application will use the user's webcam to track their hand and interpret gestures for answering multiple-choice questions, drawing, and navigating the quiz.

## 2. Core Technologies
- **Python 3**: Primary programming language
- **OpenCV**: For webcam capture, video stream processing, and drawing UI elements on the screen
- **MediaPipe**: For real-time, high-fidelity hand tracking and landmark detection
- **NumPy**: For numerical calculations, especially for distance and point averaging

## 3. Key Features & Functionalities

### A. Main Application Flow
- On startup, the application clears any previous session's responses and prepares a responses directory
- It loads questions from an external quiz.txt file
- The application presents questions one by one, starting from the first
- Each question has a 15-second timer
- After the last question, or if the user finishes early, a final results screen is displayed for 3 seconds
- All responses, including those for skipped questions, are saved to the responses directory before the application closes

### B. Hand Tracking & Gesture Recognition
- The system must track a single hand (max_num_hands=1) in real-time
- **Pointing Gesture**: The position of the index finger tip is used for all UI interactions like selecting options or pressing buttons
- **Pinch Gesture**: The system must detect a "pinch" by calculating the Euclidean distance between the thumb tip and the index finger tip. A small distance signifies a pinch

### C. User Interface (UI) & Visual Feedback
- The UI is an overlay on top of the live, flipped webcam feed
- **Question Display**: The current question number and text must be displayed with a colored background
- **MCQ Options**: The four multiple-choice options must be displayed, each within its own colored rectangular box
- **On-Screen Timer**: A countdown timer showing the time left for the current question must be visible
- **Finish Button**: A persistent "Finish" button must be displayed at the bottom of the screen

**Visual Feedback:**
- The color of an MCQ option box changes to a highlight color when the user's index finger hovers over it
- The "Finish" button also changes to a highlight color when hovered over, providing consistent feedback
- Real-time Drawing: The path traced by the user's finger during a pinch gesture must be drawn on the screen in real-time

### D. Interaction Logic & Timers
- **MCQ Selection**: To select an answer, the user must point their index finger at an option and hold it there for 1.5 seconds. Upon successful confirmation, the question immediately ends
- **Drawing**: Drawing occurs only while the pinch gesture is active. Releasing the pinch "lifts the pen"
- **Finish Button**: This button functions identically to an MCQ option; the user must point and hold for 1.5 seconds to activate it. Activation ends the entire quiz immediately
- **Quit Key**: Pressing the 'q' key on the keyboard must terminate the application at any time

### E. Backend & File System
- The application must read from a quiz.txt file formatted with keywords (mcq, draw) to define question types
- All outputs must be saved in a responses directory
- MCQ responses, including the selected option, the correct option, and the final score, must be logged in responses/responses.txt
- Drawings must be saved as individual image files (e.g., drawing_1.png), and the file path is logged in the text file
- If the user finishes early, any unseen questions must be logged as "Not Attempted" to ensure the response file is complete

### F. In-Depth: The Drawing Mechanism
- **The drawing_points List**: At the start of each drawing question, a new, empty list is created to store the drawing path
- When the "Pinch Gesture" is active, the (x, y) coordinates of the index finger are appended to this list on each frame
- When the pinch is released, a None value is appended to the list. This acts as a "pen up" signal, allowing the system to handle multiple, non-connected lines
- **Real-time Drawing on Screen**: During the question, the application iterates through the drawing_points list on every frame. It draws a line (cv2.line) between each consecutive point (i-1 and i). The code must check if either point is None before drawing, which correctly handles the breaks in the drawing. This continuous redrawing creates the illusion of drawing directly on the video feed
- **Saving the Final Image**: After the question ends, the final drawing_points list is used to create the permanent image
- A new, completely black canvas (a NumPy array of zeros) is created with the same dimensions as the video frame
- The application iterates through the drawing_points list one last time, drawing the lines onto this black canvas
- This canvas, now containing only the drawing against a black background, is saved as a PNG image using cv2.imwrite

## 4. Critical Implementation Rule: The "Detect, then Draw" Principle
This is the most critical rule for application stability. To prevent the UI elements from interfering with the hand detection model, every single frame in the main loop must be processed in this exact order:

1. **Capture Frame**: Get a new frame from the webcam and flip it horizontally
2. **DETECT**: Perform hand detection using MediaPipe on this clean, unmodified frame. Store the resulting landmark data
3. **PROCESS & DRAW**: After detection is complete, use the stored landmark data to determine interaction states (e.g., is the finger hovering over a button?). Then, draw all UI elements onto the frame (questions, options, buttons) using the correct colors based on those interaction states. Finally, draw the hand landmarks themselves
4. **DISPLAY**: Show the final, composite frame to the user 