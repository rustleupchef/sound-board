import os
from playsound import playsound
from time import sleep
from pynput import keyboard
import time
from threading import Thread, Event
import tkinter as tk

last_played = 0.0
chain = []
windowThread = Thread()

def window() -> None:
    root = tk.Tk()
    root.title("Overlay UI")
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 0.7)
    root.configure(bg='white')
    root.geometry("200x100+100+100")  # width x height + x + y
    root.bind("<Button-1>", lambda e: root.destroy())
    root.bind("<Button-2>", lambda e: playsound("sounds/random-mp3.mp3"))
    root.mainloop()


def on_press(key) -> None:
    global last_played, chain, windowThread

    chain.append(key)
    if len(chain) < 1:
        return
    
    if time.time() - last_played < 0.2:
        if keyboard.Key.ctrl in chain or keyboard.KeyCode.from_char('u') in chain:
            if not windowThread.is_alive():
                windowThread = Thread(target=window)
                windowThread.start()
            
        elif keyboard.Key.ctrl in chain or keyboard.KeyCode.from_char('m') in chain:
            return False
    
    chain.clear()
    last_played = time.time()

def getSoundPaths(directory = "") -> list:
    sound_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav") or file.endswith(".mp3"):
            sound_files.append(os.path.join(directory, file))
    return sound_files

def main() -> None:
    sound_files: list = getSoundPaths("sounds")
    if len(sound_files) == 0:
        print("No files found.")
        return
    
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
        
if __name__ == "__main__":
    main()