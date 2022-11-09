import json
import math
import sys
import time
from collections import defaultdict

words = []

def get_entropy(word):
    patterns = defaultdict(int)
    letters_count = defaultdict(int)
    for l in word:
        letters_count[l] += 1

    for option in words:
        # pattern is the wordle pattern ("clue")
        # 0 = gray, 1 = yellow, 2 = green
        # for example, if YÖPUU was the [word] and MÖMMÖ was the [option],
        # the pattern would be 02000
        pattern = [0] * 5
        used_letters = defaultdict(int)
        # greens (can't do both in one iteration)
        for i in range(len(option)):
            if option[i] is word[i]:
                pattern[i] = 2
                used_letters[option[i]] += 1
        # yellows
        for i in range(len(option)):
            if option[i] in word and used_letters.get(option[i], 0) < letters_count.get(option[i]) and pattern[i] != 2:
                pattern[i] = 1
                used_letters[option[i]] += 1

        pattern_str = "".join(map(str, pattern))
        patterns[pattern_str] += 1

    # calculate entropy
    entropy = 0
    for v in patterns.values():
        p = v / len(words)
        entropy += p * math.log2(1 / p)
    
    return entropy

def calculate(source_file = "words-parsed.txt", dest_file = "entropies.txt"):
    global words

    start_time = time.time()

    print(f"Luetaan sanat tiedostosta {source_file}")
    with open(source_file, "r", encoding="utf-8") as input:
        words = input.read().split("\n")

    entropies = {}
    words_count = len(words)
    for i in range(words_count):
        sys.stdout.write(f"\rLasketaan entropioita... [{i + 1}/{words_count}]")
        sys.stdout.flush()
        entropies[words[i]] = round(get_entropy(words[i]), 2)

    print(f"\Kirjoitetaan tulokset tiedostoon {dest_file}")
    with open(dest_file, "w", encoding="utf-8") as output:
        json.dump(entropies, output, ensure_ascii=False)
    print("Valmista!")
    print(f"Kesto: {round(time.time() - start_time, 2)}s")

if __name__ == "__main__":
    calculate()
