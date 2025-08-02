# AI-Based Virtual Quiz System

A hand gesture-controlled quiz application using computer vision and MediaPipe. Users can answer multiple-choice questions and draw responses using hand gestures captured through their webcam.

## Features

- **Hand Gesture Recognition**: Real-time hand tracking using MediaPipe
- **Multiple Question Types**: Supports both MCQ and drawing questions
- **Interactive UI**: Visual feedback with colored backgrounds and highlighting
- **Timer System**: 15-second countdown timer for each question
- **Response Logging**: Automatically saves all responses and drawings
- **Score Calculation**: Automatic scoring for MCQ questions
- **Early Finish**: Option to finish quiz early using hand gestures
- **Modular Architecture**: Well-organized code structure with separate modules
- **Cross-Platform**: Works on Windows, macOS, and Linux

## File Structure

```
ai-based-virtual-quiz/
├── main.py                 # Entry point
├── quiz_engine.py          # Core quiz logic and game loop
├── hand_detection.py       # MediaPipe hand tracking and gesture recognition
├── ui_components.py        # UI rendering and visual feedback
├── file_utils.py           # File operations (loading questions, saving responses)
├── quiz.txt               # Quiz questions file
├── requirements.txt        # Python dependencies
└── README.md              # Documentation
```


## Requirements

- Python 3.7 or higher
- Webcam
- Good lighting conditions

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bmoukthikpatel/ai-based-virtual-quiz
   cd ai-based-virtual-quiz
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Application
```bash
python main.py
```

### Interaction Guide

**MCQ Questions**:
1. Point your index finger at the option you want to select (A, B, C, or D)
2. Hold for 1.5 seconds to confirm your selection
3. The selected option will be highlighted in light blue

**Drawing Questions**:
1. Pinch your thumb and index finger together
2. Move your hand to draw on the screen
3. Your drawing will be saved as a PNG file

**Navigation**:
- Use the "Finish" button at the bottom to end the quiz early
- Press 'q' to quit the application

### Quiz File Format

Create a `quiz.txt` file with the following format:

```
draw
Write integer 4 in binary?

mcq
What is the capital of India?
A) Mumbai
B) Kolkata
C) New Delhi
D) Chennai
C

mcq
Which river is considered the holiest in India?
A) Ganges
B) Yamuna
C) Brahmaputra
D) Godavari
A
```

**Format Rules**:
- **MCQ Questions**: Use keyword "mcq", followed by question, 4 options (A-D), and correct answer
- **Drawing Questions**: Use keyword "draw", followed by question
- Each question should be separated by blank lines

## Architecture

### System Overview
The application uses a modular architecture with separate components for different functionalities:

- **QuizEngine**: Main controller that manages quiz flow and coordinates between modules
- **Hand Detection**: MediaPipe-based hand tracking and gesture recognition
- **UI Components**: Visual rendering and user interface elements
- **File Utilities**: Data persistence and file operations

### Data Flow
1. **Initialization**: Load questions → Setup camera → Initialize MediaPipe
2. **Question Loop**: Display question → Capture hand gestures → Process interactions
3. **Response Handling**: Log answers → Save drawings → Calculate scores
4. **Results**: Display final score → Save all responses

### Key Components

**QuizEngine** (`quiz_engine.py`):
- Main controller class that manages quiz flow and state
- Handles question transitions and user interactions
- Coordinates between all modules

**Hand Detection** (`hand_detection.py`):
- MediaPipe hand tracking initialization
- Gesture recognition (pinch, pointing)
- Finger position calculation and distance measurements

**UI Components** (`ui_components.py`):
- Text rendering with colored backgrounds
- Question and option display
- Timer visualization and drawing overlay

**File Utilities** (`file_utils.py`):
- Quiz file parsing and validation
- Response logging and drawing image saving
- Directory management

## Output

### Generated Files
- `responses/responses.txt`: Text log of all responses
- `responses/drawing_X.png`: Saved drawing images

### Response Format
```
Question 1: responses\drawing_1.png
Question 2: B (correct option is C)
Question 3: A (correct option is A)

Your result is 1/2
```

## Customization

### Adding New Questions
1. Edit `quiz.txt` following the format above
2. Add MCQ or drawing questions as needed
3. Restart the application

### Modifying Timer
- Change the `15` second timer in `quiz_engine.py` line 67
- Adjust confirmation time (1.5 seconds) in gesture detection

### UI Customization
- Modify colors in `ui_components.py`
- Change font sizes and positions
- Adjust drawing sensitivity in `hand_detection.py`

## Troubleshooting

**Camera not detected**:
- Check if webcam is connected
- Ensure no other application is using the camera
- Try restarting the application

**Hand tracking issues**:
- Improve lighting conditions
- Keep hands clearly visible to camera
- Ensure good contrast between hand and background

**Performance issues**:
- Close other applications using the camera
- Reduce camera resolution if needed
- Check system resources

## Dependencies

- opencv-python==4.8.1.78
- mediapipe==0.10.7
- numpy==1.24.3

## License

This project is open source and available under the MIT License.

## Acknowledgments

- **MediaPipe**: Hand tracking and gesture recognition
- **OpenCV**: Computer vision and image processing
- **NumPy**: Numerical computations 