import os

if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == ".": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        os.system(f'ffmpeg -y -i {indir}/video.mp4 -ab 160k -ac 2 -ar 44100 -vn {indir}/audio.mp3')




