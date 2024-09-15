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

    with open("emojis2.txt", "w") as out:
        for row in list(reader)[1000:2000]:
            emojis = run_text(CONVERSION_PROMPT, text=row[2])
            print(f"{row[2]}: {emojis}")
            out.write(emojis)


# x = run_text(CONVERSION_PROMPT, text="hi do you want pizza?")
# print(x)

