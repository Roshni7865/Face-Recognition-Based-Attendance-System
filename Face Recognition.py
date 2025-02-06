#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import cv2
import face_recognition
import pandas as pd
from datetime import datetime, timedelta
from mtcnn import MTCNN
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

# Initialize video capture
video_capture = cv2.VideoCapture(0)

# Initialize lists for storing known face encodings and names
known_faces = []
known_names = []
face_data = pd.DataFrame(columns=["Name", "Check-In Time", "Check-Out Time", "Time Spent (H:M)", "Days Attended", "Attendance Percentage"])

# Initialize MTCNN detector
detector = MTCNN()

# Function to mark face attendance (check-in or check-out)
def mark_face(name, check_in=True):
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if check_in:
        # Mark check-in time
        print(f"Check-in for {name} at {current_time}")  # Debugging line
        face_data.loc[len(face_data)] = [name, current_time, "", "", 0, 100.0]  # Mark check-in time
    else:
        # Find and mark check-out time
        index = face_data[face_data["Name"] == name].index[-1]  # Get last check-in index
        check_in_time = datetime.strptime(face_data.at[index, "Check-In Time"], '%Y-%m-%d %H:%M:%S')
        check_out_time = datetime.now()
        face_data.at[index, "Check-Out Time"] = current_time  # Mark check-out time
        
        # Calculate the time spent
        time_spent = check_out_time - check_in_time
        face_data.at[index, "Time Spent (H:M)"] = str(time_spent).split(".")[0]
        
        # Increment the attended days
        face_data.at[index, "Days Attended"] = 1
        
        # Calculate attendance percentage
        calculate_attendance_percentage(name)

        print(f"Check-out for {name} at {current_time}")
        
    # Save the attendance to CSV
    face_data.to_csv("attendance.csv", index=False)

# Function to calculate attendance percentage
def calculate_attendance_percentage(name):
    total_days = 365  # assuming one year
    attended_days = len(face_data[face_data['Name'] == name]['Check-In Time'].dropna())
    
    # Adjusting attendance based on missed days
    attendance_percentage = (attended_days / total_days) * 100
    print(f"{name}'s current attendance percentage: {attendance_percentage}%")
    
    # Update the attendance percentage in the CSV file
    # Find the index of the latest attendance for this person
    index = face_data[face_data["Name"] == name].index[-1]
    face_data.at[index, "Attendance Percentage"] = attendance_percentage

    # Save the attendance with updated percentage to CSV
    face_data.to_csv("attendance.csv", index=False)

# Function to register a new face (capturing and storing face encoding)
def register_face(name):
    print(f"Please look at the camera for registration, {name}...")
    for _ in range(5):  # Capture multiple frames for better face encoding
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            continue

        # Detect faces using MTCNN
        results = detector.detect_faces(frame)
        
        if results:
            # Assume we are working with the first detected face
            x, y, w, h = results[0]['box']
            face = frame[y:y+h, x:x+w]

            # Convert the frame to RGB (OpenCV uses BGR)
            rgb_frame = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face_encoding = face_recognition.face_encodings(rgb_frame)
            
            if face_encoding:
                encoding = face_encoding[0]
                known_faces.append(encoding)
                known_names.append(name)
                print(f"{name} has been registered successfully!")
                break
        else:
            print("No face detected, please try again.")

# Function to handle face recognition and attendance marking
def start_face_recognition():
    recognized_faces = []
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        # Detect faces using MTCNN
        results = detector.detect_faces(frame)

        for result in results:
            x, y, w, h = result['box']
            face = frame[y:y+h, x:x+w]

            # Convert the frame to RGB (OpenCV uses BGR)
            rgb_frame = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)

            # Find face encodings
            face_encodings = face_recognition.face_encodings(rgb_frame)

            if face_encodings:
                face_encoding = face_encodings[0]
                matches = face_recognition.compare_faces(known_faces, face_encoding)
                name = "Unknown"

                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_names[first_match_index]

                    # Check if the person is already recognized and check-in
                    if name not in recognized_faces:
                        if name not in face_data['Name'].values:
                            mark_face(name, check_in=True)
                        recognized_faces.append(name)

                        # Ask user for check-out
                        check_out_response = messagebox.askyesno("Check-Out", f"Do you want to check-out, {name}?")
                        if check_out_response:
                            mark_face(name, check_in=False)

                # Draw a rectangle around the face with green color (BGR: (0, 255, 0))
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                # Display the name below the face
                cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert frame to ImageTk format for displaying in Tkinter
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb_frame)
        imgtk = ImageTk.PhotoImage(image=img)
        
        # Update the GUI window with the new frame
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)
        
        # Add a delay to simulate real-time video
        root.update_idletasks()
        root.update()

# Function to handle registration mode
def register_face_gui():
    name = simpledialog.askstring("Register Face", "Enter the name to register:")
    if name:
        register_face(name)
        messagebox.showinfo("Registration", f"{name} has been registered!")

# Function to exit the application
def exit_application():
    video_capture.release()  # Release the video capture object
    cv2.destroyAllWindows()  # Close any OpenCV windows
    root.quit()  # Exit the Tkinter event loop and close the window

# Initialize Tkinter window
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Set the window background color
root.configure(bg='#f0f0f0')

# Add a label to show the video stream
video_label = tk.Label(root, bg='#f0f0f0')
video_label.pack(padx=10, pady=10)

# Add some space between components
frame = tk.Frame(root, bg='#f0f0f0')
frame.pack(pady=20)

# Add buttons for registering a face, starting face recognition, and exiting
register_button = tk.Button(frame, text="Register Face", command=register_face_gui, 
                             font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", padx=20, pady=10)
register_button.pack(side=tk.LEFT, padx=10)

start_button = tk.Button(frame, text="Start Face Recognition", command=start_face_recognition, 
                         font=("Arial", 12, "bold"), bg="#2196F3", fg="white", padx=20, pady=10)
start_button.pack(side=tk.LEFT, padx=10)

exit_button = tk.Button(frame, text="Exit", command=exit_application, 
                         font=("Arial", 12, "bold"), bg="#f44336", fg="white", padx=20, pady=10)
exit_button.pack(side=tk.LEFT, padx=10)

# Set a stylish header label
header_label = tk.Label(root, text="Face Recognition Attendance System", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
header_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()

# Release the camera when the window is closed
video_capture.release()
cv2.destroyAllWindows()


# In[ ]:




