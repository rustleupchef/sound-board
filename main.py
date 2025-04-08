import os

def getSoundPaths(directory = "") -> list:
    sound_files = []
    for file in os.listdir(directory):
        if file.endswith(".wav") or file.endswith(".mp3"):
            sound_files.append(os.path.join(directory, file))
    return sound_files

def main():
    sound_files: list = getSoundPaths("sounds")
    if len(sound_files) == 0:
        print("No files found.")
        return


if __name__ == "__main__":
    main()