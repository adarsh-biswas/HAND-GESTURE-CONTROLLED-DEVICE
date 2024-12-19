# Hand Gesture Controlled Mouse

This project demonstrates a hand gesture-controlled mouse using Python, OpenCV, MediaPipe, and PyAutoGUI. By tracking hand movements through a webcam, users can control their computer mouse, perform drag actions, and execute left-clicks based on hand gestures.

## Features
- **Mouse Movement**: Move the cursor by pointing with the index finger.
- **Drag Action**: Simulate a mouse drag using a pinching gesture (thumb and index finger).
- **Left-Click**: Perform a left-click by raising both the index and middle fingers.

## Prerequisites
Ensure the following are installed:

- Python 3.7 or later
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy

Install the required libraries using pip:
```bash
pip install opencv-python mediapipe pyautogui numpy
```

## How It Works
1. **Hand Detection**: Utilizes MediaPipe Hands to detect hand landmarks in real-time.
2. **Landmark Mapping**: Maps the index finger's position to the screen coordinates.
3. **Gestures**:
   - Cursor movement is based on the index finger's position.
   - Drag is initiated when the distance between the thumb tip and index finger tip is below a threshold.
   - A left-click is performed when the index finger is above the middle finger.

## Usage
1. Connect a webcam to your computer.
2. Run the Python script:
   ```bash
   main.py
   ```
3. Control the mouse cursor by moving your hand in front of the camera.
4. Use gestures for additional mouse actions:
   - **Drag**: Pinch the thumb and index finger.
   - **Left-Click**: Raise the index and middle fingers.
5. Press the 'q' key to exit.

## Code Overview
The script is structured as follows:

1. **Initialization**:
   - Sets up MediaPipe Hands and webcam.
   - Configures PyAutoGUI for screen interaction.

2. **Main Loop**:
   - Reads frames from the webcam.
   - Processes frames to detect hand landmarks.
   - Maps hand positions to cursor movements and interprets gestures.

3. **Gestures**:
   - Cursor movement is smoothed using interpolation.
   - Mouse actions (drag and click) are performed based on specific conditions.

4. **Cleanup**:
   - Releases the webcam and closes OpenCV windows.

## Troubleshooting
- If the script fails to detect the camera, ensure the webcam is connected and accessible.
- Adjust thresholds (e.g., pinching distance) to suit your hand size and gestures.

## Limitations
- Works best in a well-lit environment.
- Gestures may not be recognized if the hand moves too quickly or is partially obscured.
- Limited to controlling one hand at a time.

## Future Improvements
- Add support for more gestures (e.g., right-click, double-click).
- Enhance detection accuracy for diverse lighting conditions.
- Incorporate multi-hand support.

## Acknowledgments
- [MediaPipe](https://google.github.io/mediapipe/) for real-time hand tracking.
- [PyAutoGUI](https://pyautogui.readthedocs.io/) for automating GUI interactions.
- [OpenCV](https://opencv.org/) for image processing.

## License
This project is open-source and available under the MIT License.
