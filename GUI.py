import tkinter as tk
from tkinter import *
import cv2
from PIL import Image, ImageTk
import numpy as np

global last_frame1                                   
last_frame1 = np.zeros((480, 640, 3), dtype=np.uint8)
global last_frame2                                      
last_frame2 = np.zeros((480, 640, 3), dtype=np.uint8)
global cap1
global cap2
paused = False  # Variable to pause/play video

cap1 = cv2.VideoCapture("C:\\Users\\hegde\\OneDrive\\Desktop\\Road Lane Detection\\vid3.mp4")  # Input video path
cap2 = cv2.VideoCapture("C:\\Users\\hegde\\OneDrive\\Desktop\\Road Lane Detection\\out.mp4")   # Resultant video path

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
            pic = cv2.cvtColor(last_frame1, cv2.COLOR_BGR2RGB)     
            img = Image.fromarray(pic)
            imgtk = ImageTk.PhotoImage(image=img)
            lmain.imgtk = imgtk
            lmain.configure(image=imgtk)
    
    lmain.after(10, show_vid)  # Refresh video every 10ms

def show_vid2():
    if not cap2.isOpened():                             
        print("Cannot open the result video")
        return
    if not paused:
        flag2, frame2 = cap2.read()
        
        if flag2:
            frame2 = cv2.resize(frame2, (400, 500))
            global last_frame2
            last_frame2 = frame2.copy()
            pic2 = cv2.cvtColor(last_frame2, cv2.COLOR_BGR2RGB)
            img2 = Image.fromarray(pic2)
            img2tk = ImageTk.PhotoImage(image=img2)
            lmain2.img2tk = img2tk
            lmain2.configure(image=img2tk)
    
    lmain2.after(10, show_vid2)  # Refresh video every 10ms

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
    show_vid2()

    root.geometry("900x700")  # Set window size
    root.resizable(True, True)  # Allow window to be resizable
    root.mainloop()  # Start GUI loop
    
    cap1.release()
    cap2.release()
