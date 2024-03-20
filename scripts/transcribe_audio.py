import os
from openai import OpenAI
import json

def audio_to_words(indir, outdir):
  client = OpenAI()

  # open audio file
  audio_file = open(os.path.join(indir, "audio.mp3"), "rb")

  # use whisper to generate transcription
  transcript = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format="verbose_json",
    timestamp_granularities=["word"]
  )

  # dump transcription
  with open(os.path.join(outdir, "words.json"), 'w') as f:
    json.dump(transcript.words, f, ensure_ascii=False)

if __name__ == "__main__":
    slides_dir = "../slides"
    print("\n")
    for name in os.listdir(slides_dir):
        if name[0] == ".": # .DS_Store
            continue
        print("___Processing: ", name, "___\n")
        indir = os.path.join(slides_dir, name)
        if os.path.isfile(os.path.join(indir, "words.json")):
            print("file alredy exists")
        else:
            print("file doesn't exist")
            audio_to_words(indir, indir)

