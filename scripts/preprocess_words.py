import os
import json

def group_words(indir, outdir):
    
    # Opening "words" JSON file
    f = open(os.path.join(outdir, "words.json"))
    data = json.load(f)

    aggregate_words = "" 
    starts = []
    ends = []
    words = []

    for d in data:
        word = d["word"]
        if word == "": 
            word = "percent" # because the percent sign gets lost
        words.append(word.lower())
        starts.append(d["start"])
        ends.append(d["end"])
    
    for i in range(len(words)):
        word = words[i]

        if i+1 < len(words):
            if starts[i+1] - ends[i] > 0.5:
                aggregate_words += word + "\n\n"
                capital_next = True
            elif starts[i+1] - ends[i] > 0.1:
                aggregate_words += word + "\n"
            else:
                aggregate_words += word + " "
        else:
            aggregate_words += word
        
    with open(os.path.join(outdir, "text_script.txt"), "w") as file:
        file.write(aggregate_words)


if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == ".": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        group_words(indir, indir)