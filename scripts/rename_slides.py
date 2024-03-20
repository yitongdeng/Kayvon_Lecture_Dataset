import os

if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == ".": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        for image in os.listdir(indir):
            # check if the image ends with jpg
            if (image.endswith(".jpg")):
                print("name before: ", image)
                os.rename(os.path.join(indir, image), os.path.join(indir,'slide.jpg'))
