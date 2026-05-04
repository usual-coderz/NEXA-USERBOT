import os

BASE = os.path.dirname(__file__)
WORD_FILE = os.path.join(BASE, "..", "word.txt")

def load_words():
    with open(WORD_FILE, "r", encoding="utf-8") as f:
        return [x.strip() for x in f if x.strip()]