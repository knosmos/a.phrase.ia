ILLEGAL_CHARACTERS = {chr(i) for i in range(127)}
MODIFIERS = {"\ufe0f", "\u2642", "\u200d"}

"""
emoji1: [emoji2, ]
the lists will be sorted by instances
"""
markov_chain = {}
freq_table = {}

def get_n_grams(text, n):
    for ch in ILLEGAL_CHARACTERS | MODIFIERS:
        text = text.replace(ch, "")
    return [tuple(text[i:i+n]) for i in range(len(text) - n + 1)]

def add_to_freq_table(text):
    for ch in ILLEGAL_CHARACTERS:
        text = text.replace(ch, "")
    for c in text:
        if c in freq_table:
            freq_table[c] += 1
        else:
            freq_table[c] = 1

def add_to_markov_chain(text):
    bi_grams = get_n_grams(text, 2)
    for c1, c2 in bi_grams:
        if c1 not in markov_chain.keys():
            markov_chain[c1] = []
        if c2 is not None and c2 != "":  # jank
            markov_chain[c1].extend(c2)

        # markov_chain[c1].sort(lambda )
    return markov_chain

def get_results(char: str, n: int) -> set[str]:
    emojis = markov_chain[char]
    return set(emoji for emoji in emojis)

def get_initial(n):
    return sorted(freq_table.keys(), key=lambda x:-freq_table[x])[:n]

def load_lines(lines):
    for line in lines:
        add_to_freq_table(line)
        add_to_markov_chain(line)

with open("emojis.txt", "r", encoding="utf-8") as f:
    for line in f.read().split("\n"):
        add_to_markov_chain(line)
        add_to_freq_table(line)
    print(markov_chain)
    print(get_results('🦮', 2))

    # print(*get_n_grams(f.readlines()[0], 2), sep="\n")
    
