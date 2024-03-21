import os
import json
import re
from process_video import *
import copy
import shutil
import argparse

# Returns number of words in string
def count_words(string):
    OUT = 0
    IN = 1
    state = OUT
    wc = 0

    # Scan all characters one by one
    for i in range(len(string)):

        # If next character is a separator, 
        # set the state as OUT
        if (string[i] == ' ' or string[i] == '\n' or
            string[i] == '\t'):
            state = OUT

        # If next character is not a word 
        # separator and state is OUT, then 
        # set the state as IN and increment 
        # word count
        elif state == OUT:
            state = IN
            wc += 1

    # Return the number of words
    return wc

def parse_bbox(s):
    match = re.match(r"(\d+) x (\d+) @ \((\d+), (\d+)\)", s)
    if match:
        # Convert the matched groups to integers
        A, B, C, D = map(int, match.groups())
        
        # Calculate A+C and B+D
        return [C, D, A+C, B+D]
    else:
        return []

def parse_annotation(indir, outdir):
    slide = cv2.imread(os.path.join(indir, 'slide.jpg'))
    
    # Opening "words" JSON file
    text = open(os.path.join(indir, "text_script.txt")).read()

    text_segments = text.split('\n\n')

    pattern = re.compile(r"\^(.*?)\.")

    f = open(os.path.join(indir, "words.json"))
    data = json.load(f)

    starts = []
    ends = []
    for d in data:
        starts.append(d["start"])
        ends.append(d["end"])

    segments = []
    segment_bboxes = []
    segment_texts = []
    segment_starts = []
    segment_ends = []
    total_words = 0
    print("correct total words: ", len(starts))
    for i in range(len(text_segments)):
        curr_segment = {}

        bboxes = pattern.findall(text_segments[i])
        bboxes = [parse_bbox(m) for m in bboxes]
        print("matched bboxes: ", bboxes)
        curr_segment["bboxes"] = bboxes
    
        text_segment = re.sub(r" +\n", "\n", re.sub(pattern, '', text_segments[i])).replace("\n", ", ")[:-2]
        print("text segment: ", text_segment)
        curr_segment["text"] = text_segment

        segment_num_words = count_words(text_segment)
        curr_segment["start"] = starts[total_words]
        total_words += segment_num_words
        curr_segment["end"] = ends[total_words-1]

        segments.append(curr_segment)

    print("total words: ", total_words)
    if (total_words == len(starts)):
        print("total num words match!")
    else:
        print("total num words don't match, exit")
        exit()

    # dump annotation
    with open(os.path.join(indir, "processed_annotation.json"), 'w') as f:
        json.dump(segments, f, ensure_ascii=False)

    highlighteds = []
    for i in range(len(segments)):
        print("processing segment: ", i)
        slide_copy = copy.deepcopy(slide)
        slide_copy = paint_bboxes(slide_copy, segments[i]["bboxes"])
        highlighteds.append(slide_copy)
    
    create_image_video(indir, indir, slide, highlighteds, [s["start"] for s in segments], [s["end"] for s in segments])
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', type=str, required=True)
    args = parser.parse_args()

    slides_dir = "../slides"
    indir = os.path.join(slides_dir, args.name)
    parse_annotation(indir, indir)