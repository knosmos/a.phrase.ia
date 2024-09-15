ILLEGAL_CHARACTERS = {chr(i) for i in range(127)}
MODIFIERS = {
    # Skin Tone Modifiers
    "\U0001F3FB",  # Light Skin Tone
    "\U0001F3FC",  # Medium-Light Skin Tone
    "\U0001F3FD",  # Medium Skin Tone
    "\U0001F3FE",  # Medium-Dark Skin Tone
    "\U0001F3FF",  # Dark Skin Tone

    # Gender Modifiers
    "\u2640",  # Female Sign
    "\u2642",  # Male Sign
    "\u26A7",  # Gender Inclusive Sign

    # Zero Width Joiner
    "\u200D",  # Zero Width Joiner (ZWJ)

    # Emoji Variation Selectors
    "\uFE0E",  # Variation Selector-15 (text presentation)
    "\uFE0F",  # Variation Selector-16 (emoji presentation)

    # Regional Indicator Symbols (A-Z)
    "\U0001F1E6",  # Regional Indicator Symbol A
    "\U0001F1E7",  # Regional Indicator Symbol B
    "\U0001F1E8",  # Regional Indicator Symbol C
    "\U0001F1E9",  # Regional Indicator Symbol D
    "\U0001F1EA",  # Regional Indicator Symbol E
    "\U0001F1EB",  # Regional Indicator Symbol F
    "\U0001F1EC",  # Regional Indicator Symbol G
    "\U0001F1ED",  # Regional Indicator Symbol H
    "\U0001F1EE",  # Regional Indicator Symbol I
    "\U0001F1EF",  # Regional Indicator Symbol J
    "\U0001F1F0",  # Regional Indicator Symbol K
    "\U0001F1F1",  # Regional Indicator Symbol L
    "\U0001F1F2",  # Regional Indicator Symbol M
    "\U0001F1F3",  # Regional Indicator Symbol N
    "\U0001F1F4",  # Regional Indicator Symbol O
    "\U0001F1F5",  # Regional Indicator Symbol P
    "\U0001F1F6",  # Regional Indicator Symbol Q
    "\U0001F1F7",  # Regional Indicator Symbol R
    "\U0001F1F8",  # Regional Indicator Symbol S
    "\U0001F1F9",  # Regional Indicator Symbol T
    "\U0001F1FA",  # Regional Indicator Symbol U
    "\U0001F1FB",  # Regional Indicator Symbol V
    "\U0001F1FC",  # Regional Indicator Symbol W
    "\U0001F1FD",  # Regional Indicator Symbol X
    "\U0001F1FE",  # Regional Indicator Symbol Y
    "\U0001F1FF",  # Regional Indicator Symbol Z

    # Tag Characters
    "\U000E0000",  # Language Tag
    "\U000E007F",  # Cancel Tag
    "\U000E0061",  # Tag Latin Small Letter A
    "\U000E0062",  # Tag Latin Small Letter B
    "\U000E0063",  # Tag Latin Small Letter C
    "\U000E0064",  # Tag Latin Small Letter D
    "\U000E0065",  # Tag Latin Small Letter E
    "\U000E0066",  # Tag Latin Small Letter F
    "\U000E0067",  # Tag Latin Small Letter G
    "\U000E0068",  # Tag Latin Small Letter H
    "\U000E0069",  # Tag Latin Small Letter I
    "\U000E006A",  # Tag Latin Small Letter J
    "\U000E006B",  # Tag Latin Small Letter K
    "\U000E006C",  # Tag Latin Small Letter L
    "\U000E006D",  # Tag Latin Small Letter M
    "\U000E006E",  # Tag Latin Small Letter N
    "\U000E006F",  # Tag Latin Small Letter O
    "\U000E0070",  # Tag Latin Small Letter P
    "\U000E0071",  # Tag Latin Small Letter Q
    "\U000E0072",  # Tag Latin Small Letter R
    "\U000E0073",  # Tag Latin Small Letter S
    "\U000E0074",  # Tag Latin Small Letter T
    "\U000E0075",  # Tag Latin Small Letter U
    "\U000E0076",  # Tag Latin Small Letter V
    "\U000E0077",  # Tag Latin Small Letter W
    "\U000E0078",  # Tag Latin Small Letter X
    "\U000E0079",  # Tag Latin Small Letter Y
    "\U000E007A",  # Tag Latin Small Letter Z
}

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
    for ch in ILLEGAL_CHARACTERS | MODIFIERS:
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
    emojis = markov_chain[char] if char in markov_chain else ()
    return set(emoji for emoji in emojis)


def get_initial(n):
    return sorted(freq_table.keys(), key=lambda x:-freq_table[x])[:n]


def load_lines(lines):
    for line in lines:
        add_to_freq_table(line)
        add_to_markov_chain(line)


with open("emojis.txt", "r", encoding="utf-8") as f:
    load_lines(f.readlines()[1:])

with open("emojis2.txt", "r", encoding="utf-8") as f:
    load_lines(f.readlines()[1:])

print(markov_chain)
print(get_results('🦮', 2))

    # print(*get_n_grams(f.readlines()[0], 2), sep="\n")
    
