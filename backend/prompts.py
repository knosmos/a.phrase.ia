SENTENCE_GEN_PROMPT = """
    # Task Description
    Provided is a comma separated list of phrases representing a sentence written in emoji, where
    each phrase symbolizes one emoji. Build a grammatically correct English sentence that captures
    the meaning of the emoji sentence. Be concise.

    # Task Input
    {emoji_seq}

    # Output:
"""