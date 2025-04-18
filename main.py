import os
from playsound import playsound
from pynput import keyboard
import time
from threading import Thread
import tkinter as tk
from dotenv import load_dotenv, find_dotenv
import sounddevice as sd
import soundfile as sf

last_played = 0.0
chain = []

windowThread = Thread()
sound_files: list[str]
soundthreads: list[Thread] = []
size = 0

backgroundColor: str
btnBackgroundColor: str
btnForegroundColor: str

virtualMic: str

def handleSoundThread(sound_path: str) -> None:
    global soundthreads
    soundThread = Thread(target=psound, args=(sound_path,))
    soundthreads.append(soundThread)
    soundThread.start()

def psound(path: str) -> None:
    if virtualMic == "" or virtualMic is None:
        playsound(path)
        return
    try:
        data, rate = sf.read(path)
        sd.play(data, rate, device=virtualMic)
        sd.wait()
    except:
        pass

def window() -> None:
    global size, sound_files, soundthreads
    root = tk.Tk()
    root.title("Overlay UI")
    root.overrideredirect(True)
    root.attributes('-topmost', True)
    root.attributes('-alpha', 1.0)
    root.configure(bg=backgroundColor)
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    for row in range(size):
        root.grid_rowconfigure(row, weight=1)

        hasBroken = False
        for column in range(size):
            root.grid_columnconfigure(column, weight=1)
            index = row * size + column
            if index >= len(sound_files):
                button = tk.Button(
                root, 
                text="Close", 
                command= lambda: root.destroy(), 
                bg=btnBackgroundColor, 
                fg=btnForegroundColor)
                button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
                hasBroken = True
                break
            sound_path = sound_files[index]
            button = tk.Button(
                root, 
                text=os.path.basename(sound_path).split(".")[0], 
                command=lambda path=sound_path: handleSoundThread(path), 
                bg=btnBackgroundColor, 
                fg=btnForegroundColor)
            button.grid(row=row, column=column, padx=5, pady=5, sticky="nsew")
        if hasBroken:
            break

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
            for thread in soundthreads:
                if thread.is_alive():
                    thread.join()
            return False
    
    chain.clear()
    last_played = time.time()

def getSoundPaths(directory = "") -> list[str]:
    sound_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav") or file.endswith(".mp3"):
            sound_files.append(os.path.join(directory, file))
    return sound_files

def main() -> None:
    global size, sound_files, backgroundColor, btnBackgroundColor, btnForegroundColor, virtualMic
    load_dotenv(find_dotenv())
    path = os.getenv("SOUND_PATH")
    backgroundColor = os.getenv("BACKGROUND_COLOR")
    btnForegroundColor = os.getenv("BTN_FOREGROUND_COLOR")
    btnBackgroundColor = os.getenv("BTN_BACKGROUND_COLOR")
    virtualMic = os.getenv("VIRTUAL_MIC")

    sound_files = getSoundPaths(path)
    if len(sound_files) == 0:
        print("No files found.")
        return
    
    for i in range(1, len(sound_files) + 2):
        if pow(i, 2) > len(sound_files):
            size = i
            break    

    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()
        
if __name__ == "__main__":
    main()