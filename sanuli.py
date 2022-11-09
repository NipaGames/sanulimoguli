import json
import os

entropies_file = "entropies.txt"
if not os.path.exists(entropies_file):
    import entropies
    entropies.calculate(dest_file=entropies_file)
    print()

print("- YHTEENVETO -")
data = {}
with open(entropies_file, "r", encoding="utf-8") as f:
    data = json.load(f)

data_sorted = sorted(data.items(), key=lambda item: item[1])
data_max = len(data_sorted) - 1
print("5 parasta sanaa:")
for i in range(5):
    word = data_sorted[data_max - i]
    print(f"  {i + 1}. {word[0]}: {word[1]}")

print("5 huonointa sanaa:")
for i in range(5):
    word = data_sorted[i]
    print(f"  {i + 1}. {word[0]}: {word[1]}")

print("\nSanahaku: (Ctrl+C lopettaaksesi)")
while(True):
    try:
        word = input().upper()
    except KeyboardInterrupt:
        quit()
    if word in data:
        print(f"Entropia {data[word]} (sija {len(data_sorted) - [w[0] for w in data_sorted].index(word)})")
    else:
        print("Ei ole oikea sana")
