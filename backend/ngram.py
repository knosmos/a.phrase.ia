ILLEGAL_CHARACTERS = {chr(i) for i in range(127)}


"""
emoji1: [emoji2, ]
the lists will be sorted by instances
"""
markov_chain = dict()


def get_n_grams(text, n):
    for ch in ILLEGAL_CHARACTERS:
        text = text.replace(ch, "")
    return [tuple(text[i:i+n]) for i in range(len(text) - n + 1)]


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


with open("emojis.txt", "r") as f:
    for line in f.readlines():
        add_to_markov_chain(line)
    # print(markov_chain)
    print(get_results('🦮', 2))

    # print(*get_n_grams(f.readlines()[0], 2), sep="\n")
    
