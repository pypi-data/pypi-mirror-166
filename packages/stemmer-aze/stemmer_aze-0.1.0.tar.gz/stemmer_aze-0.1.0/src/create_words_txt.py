import pandas as pd

WORDS_URL = "https://raw.githubusercontent.com/aznlp/stemmer/master/words.txt"

words = pd.read_csv(WORDS_URL, on_bad_lines="skip", names=["word"])

words = words[(words["word"].str.len() > 1) | (words["word"] == "o")]

print(words[words["word"].str.len() <= 2])

words.to_csv("words.txt", header=False, index=False)