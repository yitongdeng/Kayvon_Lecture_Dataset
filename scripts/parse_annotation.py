import os
import json
import re

def parse_bbox(s):
    match = re.match(r"(\d+) x (\d+) @ \((\d+), (\d+)\)", s)
    if match:
        # Convert the matched groups to integers
        A, B, C, D = map(int, match.groups())
        
        # Calculate A+C and B+D
        return [A, B, A+C, B+D]
    else:
        return []

def parse_annotation(indir, outdir):
    
    # Opening "words" JSON file
    text = open(os.path.join(outdir, "text_script.txt")).read()

    text_segments = text.split('\n\n')


    pattern = re.compile(r"\^(.*?)\.")

    for i in range(len(text_segments)):
        matches = pattern.findall(text_segments[i])
        matches = [parse_bbox(m) for m in matches]
        print("matches: ", matches)
        


if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == "." or name != "149_1_31": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        parse_annotation(indir, indir)