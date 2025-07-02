import requests
import os
from tkinter import Tk, filedialog
import subprocess
import asyncio
import sys
import edge_tts
import pygame
from contextlib import contextmanager

@contextmanager
def suppress_output():
    with open(os.devnull, 'w') as devnull:
        old_stdout, old_stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = devnull, devnull
        yield
        sys.stdout, sys.stderr = old_stdout, old_stderr

async def generate_tts(text, output_file):
    VOICE = 'en-GB-LibbyNeural'
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(output_file)

def speak(text):
    OUTPUT_FILE = "output.mp3"

    with suppress_output():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(generate_tts(text, OUTPUT_FILE))
        finally:
            loop.close()

    pygame.mixer.init()
    pygame.mixer.music.load(OUTPUT_FILE)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.quit()

def open_file_dialog(title):
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(title=title, filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.destroy()  # Destroy the root window after file selection
    return file_path

def save_file_dialog(title):
    root = Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.asksaveasfilename(title=title, defaultextension=".png", filetypes=[("Image files", "*.jpg;*.jpeg;*.png")])
    root.destroy()  # Destroy the root window after file selection
    return file_path

def remove_background():
    api_key = "UjDVLBDzWuaJqQSK7i4DqTnL"
    url = "https://api.remove.bg/v1.0/removebg"
    headers = {
        "X-Api-Key": api_key
    }

    speak("Please choose the image, Sir")
    
    # Open file dialog after prompting the user
    image_path = open_file_dialog("Select The Image")
    if not image_path:
        speak("Sir!, You didn't choose any image...Please try again")
        return

    data = {
        "image_file": open(image_path, "rb")
    }
    response = requests.post(url, headers=headers, files=data)
    if response.status_code == 200:
        output_path = save_file_dialog("Where to Save the Edited Image")
        if not output_path:
            speak("Sir!, You didn't choose a save location... Please try again")
            return
        try:
            with open(output_path, "wb") as f:
                f.write(response.content)
            print("Background removed successfully.")
            speak("Done sir, I've removed the background. Here is the edited image.")
            subprocess.Popen(["explorer", output_path])  # Opens the folder containing the image
        except PermissionError:
            print("Permission denied. Please provide a valid output file path.")
            speak("Sorry sir, I can't save the image due to permission issues.")
    else:
        print(f"Failed to remove background: {response.status_code} - {response.text}")
        speak("Sorry sir, I couldn't remove the background.")

# Call the remove_background function
remove_background()
