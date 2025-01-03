import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np

global last_frame1
last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
global cap1
paused = False  # Variable to pause/play video

cap1 = cv2.VideoCapture("C:\\Users\\hegde\\OneDrive\\Desktop\\Road Lane Detection\\vid1.mp4")  # Input video path

def lane_detection(image):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian Blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Perform Canny edge detection with dynamic thresholds
    median_val = np.median(blurred)
    lower_threshold = int(max(0, 0.7 * median_val))
    upper_threshold = int(min(255, 1.3 * median_val))
    edges = cv2.Canny(blurred, lower_threshold, upper_threshold)
    
    # Define the Region of Interest (ROI)
    height, width = edges.shape
    roi_vertices = np.array([[
        (width * 0.1, height), 
        (width * 0.45, height * 0.6),
        (width * 0.55, height * 0.6), 
        (width * 0.9, height)
    ]], np.int32)

    mask = np.zeros_like(edges)
    cv2.fillPoly(mask, roi_vertices, 255)
    masked_edges = cv2.bitwise_and(edges, mask)
    
    # Use Hough Line Transform to detect lines
    lines = cv2.HoughLinesP(masked_edges, 1, np.pi / 180, threshold=50, minLineLength=50, maxLineGap=100)
    
    # Draw the detected lines on the image
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 5)
    
    return image

def show_vid():                                       
    if not cap1.isOpened():                             
        print("Cannot open the input video")
        return
    if not paused:
        flag1, frame1 = cap1.read()
        
        if flag1:
            frame1 = cv2.resize(frame1, (400, 500))
            global last_frame1
            last_frame1 = frame1.copy()
            
            # Apply lane detection on the original frame
            detected_frame = lane_detection(last_frame1.copy())

            # Convert both original and detected frames for display
            pic = cv2.cvtColor(last_frame1, cv2.COLOR_BGR2RGB)     
            img = Image.fromarray(pic)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
            
            pic2 = cv2.cvtColor(detected_frame, cv2.COLOR_BGR2RGB)     
            img2 = Image.fromarray(pic2)
            img2tk = ImageTk.PhotoImage(image=img2)
            lmain2.img2tk = img2tk
            lmain2.configure(image=img2tk)
    
    lmain.after(10, show_vid)  # Refresh video every 10ms

# Function to pause or play the videos
def toggle_pause():
    global paused
    paused = not paused

if __name__ == '__main__':
    root = tk.Tk()                                     
    root.title("Lane Line Detection")
    
    # Add Title Label
    title = tk.Label(root, text="Road Lane Detection System", font=("Helvetica", 16, "bold"))
    title.pack(pady=10)
    
    # Video Stream Labels
    label_input = tk.Label(root, text="Original Video", font=("Helvetica", 12))
    label_input.pack(side=LEFT, padx=10)
    
    label_result = tk.Label(root, text="Detected Lane", font=("Helvetica", 12))
    label_result.pack(side=RIGHT, padx=10)
    
    # Left video stream (Original video)
    lmain = tk.Label(master=root, borderwidth=2, relief="solid")
    lmain.pack(side=LEFT, padx=10)
    
    # Right video stream (Detected lanes)
    lmain2 = tk.Label(master=root, borderwidth=2, relief="solid")
    lmain2.pack(side=RIGHT, padx=10)
    
    # Bottom controls
    button_frame = tk.Frame(root)
    button_frame.pack(side=BOTTOM, pady=20)
    
    # Play/Pause Button
    pause_button = Button(button_frame, text="Play/Pause", width=10, font=("Helvetica", 12), command=toggle_pause)
    pause_button.pack(side=LEFT, padx=10)
    
    # Quit Button
    exit_button = Button(button_frame, text="Quit", width=10, font=("Helvetica", 12), fg="red", command=root.destroy)
    exit_button.pack(side=LEFT, padx=10)

    # Start showing videos
    show_vid()

    root.geometry("900x700")  # Set window size
    root.resizable(True, True)  # Allow window to be resizable
    root.mainloop()  # Start GUI loop
    
    cap1.release()
