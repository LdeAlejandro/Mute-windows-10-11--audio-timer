import time
import subprocess
import tkinter as tk
from tkinter import messagebox

# Initialize variables
timer_running = False
remaining_seconds = 0

# Function to mute the audio
def mute_system_audio():
    command = 'powershell -Command "(New-Object -ComObject WScript.Shell).SendKeys([char]173)"'
    subprocess.call(command, shell=True)

# Function to start the countdown and mute audio after specified time
def start_mute():
    global timer_running, remaining_seconds
    
    # Get hours and minutes from input fields
    try:
        hours = int(hours_entry.get())
        minutes = int(minutes_entry.get())
        
        if hours < 0 or minutes < 0:
            raise ValueError("Hours and minutes must be positive integers.")
        
        # Convert hours and minutes to total seconds
        remaining_seconds = (hours * 3600) + (minutes * 60)
        
        if remaining_seconds == 0:
            messagebox.showerror("Invalid Input", "Please set a non-zero timer.")
            return
        
        # Start the countdown
        timer_running = True
        update_countdown()
        
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid positive integers for hours and minutes.")

# Function to update the countdown timer
def update_countdown():
    global remaining_seconds, timer_running
    
    if remaining_seconds > 0 and timer_running:
        # Calculate hours, minutes, and seconds left
        hrs, secs = divmod(remaining_seconds, 3600)
        mins, secs = divmod(secs, 60)
        
        # Update the countdown label
        countdown_label.config(text=f"{hrs:02}:{mins:02}:{secs:02}")
        
        # Reduce remaining seconds by one
        remaining_seconds -= 1
        
        # Schedule the next update in 1 second
        root.after(1000, update_countdown)
        
    elif remaining_seconds == 0 and timer_running:
        # Mute the audio when countdown ends
        mute_system_audio()
        messagebox.showinfo("Muted", "System audio has been muted.")
        countdown_label.config(text="00:00:00")
        timer_running = False

# Function to cancel the timer
def cancel_timer():
    global timer_running
    timer_running = False
    countdown_label.config(text="Timer canceled")

# Set up the GUI
root = tk.Tk()
root.title("Mute Timer")
root.geometry("250x150")  # Set window width to 400 pixels and height to 250 pixels


# Label and entry for setting hours and minutes
tk.Label(root, text="Set timer to mute audio:").pack(pady=10)
time_frame = tk.Frame(root)
time_frame.pack(pady=5)

tk.Label(time_frame, text="Hours:").grid(row=0, column=0)
hours_entry = tk.Entry(time_frame, width=5)
hours_entry.grid(row=0, column=1)
hours_entry.insert(0, "0")  # Default value for hours

tk.Label(time_frame, text="Minutes:").grid(row=0, column=2)
minutes_entry = tk.Entry(time_frame, width=5)
minutes_entry.grid(row=0, column=3)
minutes_entry.insert(0, "1")  # Default value for minutes

# Countdown label
countdown_label = tk.Label(root, text="00:00:00", font=("Helvetica", 16))
countdown_label.pack(pady=10)

# Start and Cancel buttons
start_button = tk.Button(root, text="Set Timer", command=start_mute)
start_button.pack(side="left", padx=10)

cancel_button = tk.Button(root, text="Cancel", command=cancel_timer)
cancel_button.pack(side="right", padx=10)

root.mainloop()
