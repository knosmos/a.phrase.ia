# generating emojis from twitter text, feeding them into n-gram / markov chain
# recommendation algorithm

from llm import run_text
import csv

CONVERSION_PROMPT = """
    # Task Description
    Provided is series of text representing a statement in english. Build a
    sequence of emojis with equivalent meaning to the text. Output ONLY emojis.
    Be concise.

    # Task Input
    {text}
"""

with open("twitter_dataset.csv", "r") as f:
    reader = csv.reader(f, delimiter=",", quotechar='"')
    for row in list(reader)[1:]:
        print(row)

# x = run_text(CONVERSION_PROMPT, text="fuck you")
# print(x)

