# Face Recognition Attendance System
This project is a Face Recognition Attendance System built using OpenCV, Face Recognition, MTCNN, and Tkinter. It allows you to register individuals using their faces, track check-ins and check-outs, and calculate attendance percentages based on daily attendance.

## Features
- **Face Registration:** Capture and register individuals by their face using the webcam.
- **Face Recognition:** Detect and recognize registered faces in real-time and automatically mark their attendance.
- **Check-In & Check-Out:** Allows users to check-in when recognized, and check-out when prompted.
- **Attendance Tracking:** The system tracks check-in time, check-out time, time spent, and calculates attendance percentages.
- **GUI Interface:** Built with Tkinter, providing an easy-to-use graphical interface for interacting with the system.

## Requirements
Before running the project, make sure you have the following libraries installed:
- **opencv-python** (for video capture and processing)
- **face_recognition** (for face encoding and recognition)
- **mtcnn** (for MTCNN face detection)
- **pandas** (for storing attendance data)
- **tkinter** (for the GUI interface)
- **Pillow** (for image handling with Tkinter)

## You can install them using pip:
``` function test()
pip install opencv-python face_recognition mtcnn pandas pillow
```
## How to Use

### 1. Register a New Face
Click on the "Register Face" button in the Tkinter interface.
Enter the name of the person to register.
A camera window will open where the person must look at the camera to register their face. The system will capture multiple frames to create a face encoding and store it.

### 2. Start Face Recognition
Click on the "Start Face Recognition" button to begin the face recognition process.
The system will continuously capture frames from the webcam, detect faces, and compare them with the registered faces.
If the person is recognized, their attendance will be marked as "Check-In."
After recognizing the face, the system will prompt you with a check-out confirmation message.

### 3. Check-Out
When the check-out prompt appears, you can choose to check out the individual.
The system will log the time spent between check-in and check-out and calculate the attendance percentage accordingly.

### 4. Attendance Data
The attendance data, including check-in time, check-out time, time spent, and attendance percentage, will be stored in a CSV file called attendance.csv.

## File Structure

```
├── face_recognition_attendance.py  # Main Python script
├── attendance.csv                 # Stores attendance data
├── README.md                      # Project description and instructions
└── requirements.txt               # List of required libraries
```
## Attendance Percentage Calculation
The attendance percentage is calculated based on the number of days attended, assuming a year-long period (365 days). Each day attended increases the attendance percentage. The percentage decreases as days are missed.

The formula for attendance percentage is:
```
  Attendance Percentage = (Days Attended / Total Days) * 100
```
## License
This project is open-source and available under the MIT License.

