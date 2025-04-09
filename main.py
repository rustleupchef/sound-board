import os
from playsound import playsound
from time import sleep
from pynput import keyboard
import time

last_played = 0.0
chain = []
display = False

def on_press(key):
    global last_played, display, chain

    chain.append(key)

    if len(chain) < 1:
        return
    
    if time.time() - last_played < 0.2:
        if keyboard.Key.ctrl in chain or keyboard.KeyCode.from_char('u') in chain:
            display = not display
            print(display)
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