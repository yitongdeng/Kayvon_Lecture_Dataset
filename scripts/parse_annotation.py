import os
import json
import re

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
        return [A, B, A+C, B+D]
    else:
        return []

def parse_annotation(indir, outdir):
    
    # Opening "words" JSON file
    text = open(os.path.join(outdir, "text_script.txt")).read()

    text_segments = text.split('\n\n')

    pattern = re.compile(r"\^(.*?)\.")

    f = open(os.path.join(outdir, "words.json"))
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
    for i in range(len(text_segments)):
        curr_segment = {}

        bboxes = pattern.findall(text_segments[i])
        bboxes = [parse_bbox(m) for m in bboxes]
        print("matched bboxes: ", bboxes)
        curr_segment["bboxes"] = bboxes
    
        text_segment = re.sub(pattern, '', text_segments[i]).replace("\n", ", ")[:-2]
        print("text segment: ", text_segment)
        curr_segment["text"] = text_segment

        segment_num_words = count_words(text_segment)
        curr_segment["start"] = starts[total_words]
        total_words += segment_num_words
        curr_segment["end"] = ends[total_words-1]

        segments.append(curr_segment)


        
    # total_words = 0
    # segment_starts = []
    # segment_ends = []
    # for i in range(len(matches)):
    #     segment_starts.append(starts[total_words])
    #     total_words += len(matches[i])
    #     segment_ends.append(ends[total_words-1])
        


if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == "." or name != "149_1_31": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        parse_annotation(indir, indir)