import whisper
import sys
import re
from time import time

model = whisper.load_model("small")

def classify(audio_path: str) -> str:
    result: str = model.transcribe(audio=audio_path) # Can take wav file or path as input
    print(result["text"])
    return result

if __name__ == '__main__':
    args = sys.argv
    classify(args[1])
