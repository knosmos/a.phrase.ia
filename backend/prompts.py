SENTENCE_GEN_PROMPT = """
    # Task Description
    Provided is a comma separated list of phrases representing a sentence written in emoji, where
    each phrase symbolizes one emoji. Build a grammatically correct English sentence that captures
    the meaning of the emoji sentence. Output ONLY the sentence. Be concise.

    # Task Input
    {emoji_seq}
"""

PICTURE_TO_TEXT_PROMPT = """
    # Task Description
    Provided is an image of an object. Create a short description of the object (1-2 words),
    as well as a longer description (1 sentence). Ignore all items in the background
    of the image. Output in JSON format.

    # Output Format
    {{
        "short":<short description>,
        "long":<long description>
    }}
"""