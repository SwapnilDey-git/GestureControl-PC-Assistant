# AI-Powered Gesture Control for Chrome Tabs

This project uses Python, OpenCV, MediaPipe, and pynput to create an AI-powered gesture control system that allows you to switch between tabs in Google Chrome by using hand gestures detected via a webcam. The system detects when two fingers are raised (✌️) and based on the movement of the fingers, it will simulate left and right swipe actions in the browser.

## Features

- **Gesture Detection**: Uses MediaPipe to track and detect finger movements.
- **Tab Navigation**: Switch between browser tabs by swiping left or right with two fingers.
- **Real-time Feedback**: Visual feedback displayed with OpenCV to show finger positions and swipe actions.
- **No physical interaction with the keyboard**: All actions are done using hand gestures.

## Requirements

To run the project, you will need the following Python libraries:

- OpenCV
- MediaPipe
- pynput

### Install Dependencies

Install the required libraries using pip:

```bash
pip install opencv-python mediapipe pynput
