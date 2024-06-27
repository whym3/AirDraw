# Air Drawing with Hand Tracking

![Air Drawing](https://img.shields.io/badge/Python-3.7%2B-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.5.5.64-green)
![NumPy](https://img.shields.io/badge/NumPy-1.21.6-yellow)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.8.9.1-orange)

## Introduction

Welcome to the **Air Drawing with Hand Tracking** project! This engaging application allows you to draw in the air using your index finger, change colors by raising both your index and middle fingers, and erase by opening all five fingers. Powered by OpenCV and MediaPipe, it leverages advanced hand tracking technology to provide an interactive and fun drawing experience.

## Features

- **Air Drawing**: Use your index finger to draw in real-time.
- **Color Changing**: Raise both your index and middle fingers to cycle through different colors.
- **Erasing**: Open all five fingers to erase points within the area of your hand.

## Demo

![Demo GIF](demo.gif)

## Getting Started

### Prerequisites

Make sure you have Python 3.7 or higher installed. You'll also need the following packages:

- OpenCV
- NumPy
- MediaPipe

### Installation

1. **Clone the Repository**

   ```sh
   git clone https://github.com/yourusername/air-drawing.git
   cd air-drawing

2. **Install the required packages**:

    Make sure you have Python installed. Then, install the dependencies using:

    ```sh
    pip install -r requirements.txt
    ```

## Usage

Run the application with:

```sh
python air_drawing.py
```

## How It Works

1. **Hand Detection**: The application uses MediaPipe to detect and track your hand in real-time.
2. **Finger State Detection**: The application checks the state of your fingers to determine actions:
    - If all five fingers are up, it erases points within the area of your hand.
    - If the index and middle fingers are up, it changes the drawing color.
    - Otherwise, it draws using the index finger.
3. **Drawing and Erasing**: Points are drawn or erased based on the detected finger states and positions.

## Contributing

We welcome contributions to enhance this project! To contribute, follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

